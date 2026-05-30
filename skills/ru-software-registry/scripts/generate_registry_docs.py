#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

DOCS = {
    "01_карточка_ПО.md": """# Карточка программного обеспечения

Название ПО: {software_name}

Версия: {version}

Правообладатель: {rightsholder_name}

Сайт продукта: {product_url}

Репозиторий исходного кода: {source_repo}

Лицензия: {license}

Модель распространения: {distribution}

Краткое описание: {short_description}
""",
    "02_описание_функциональных_характеристик.md": """# Описание функциональных характеристик

{software_name} предназначено для {purpose}.

Основные функции:

- {feature_1}
- {feature_2}
- {feature_3}

ПО распространяется {distribution}. Поддержка оказывается: {support}.
""",
    "03_инструкция_по_установке.md": """# Инструкция по установке

## Требования

- Сервер или виртуальная машина под управлением Linux/совместимой ОС.
- Доступ к исходному коду: {source_repo}.
- Переменные окружения и секреты задаются вне репозитория.

## Установка

1. Получить исходный код.
2. Установить зависимости согласно README проекта.
3. Заполнить переменные окружения.
4. Запустить приложение штатным способом проекта.
5. Проверить доступность сервиса.
""",
    "06_описание_жизненного_цикла.md": """# Описание жизненного цикла

Разработка ведется правообладателем. Изменения фиксируются в системе контроля версий. Релизы маркируются тегами версий.

Сопровождение включает исправление ошибок, обновление зависимостей, выпуск новых версий, поддержку пользователей и восстановление работоспособности при сбоях.
""",
    "07_технические_средства_хранения_и_сборки.md": """# Технические средства хранения и сборки

Исходный код хранится: {source_repo}.

Технические средства размещены: {hosting_provider}, {hosting_country}, {hosting_city}, сервер {server_ip}.

Сборка и развертывание выполняются средствами проекта. Секреты и эксплуатационные настройки хранятся отдельно от исходного кода.
""",
    "11_декларация_о_данных_и_приватности.md": """# Декларация о данных и приватности

ПО не запрашивает у пользователей ФИО, паспортные данные, адреса проживания, номера телефонов, платежные данные и иные сведения, позволяющие правообладателю самостоятельно идентифицировать физическое лицо.

Технические идентификаторы платформы используются только для маршрутизации сообщений и обеспечения работы сервиса.
""",
    "13_декларация_правообладателя.md": """# Декларация правообладателя

{rightsholder_name} подтверждает наличие исключительных прав на программное обеспечение {software_name}.

ПО создано самостоятельно, распространяется на условиях лицензии {license}, доступно пользователям {distribution}.

Дата формирования документа: {today}.
""",
}

def load_json(path: Path):
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--profile", default="")
    parser.add_argument("--out", default="registry_ru")
    parser.add_argument("--software-name", default="")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    profile = load_json(Path(args.profile)) if args.profile else {}
    package_json = load_json(project / "package.json") if (project / "package.json").exists() else {}
    support = profile.get("support", {})
    hosting = profile.get("hosting", {})

    values = {
        "software_name": args.software_name or package_json.get("name", project.name),
        "version": package_json.get("version", "указать версию"),
        "rightsholder_name": profile.get("rightsholder_name", "указать правообладателя"),
        "product_url": package_json.get("homepage", "указать сайт продукта"),
        "source_repo": package_json.get("repository", {}).get("url", "указать репозиторий") if isinstance(package_json.get("repository"), dict) else package_json.get("repository", "указать репозиторий"),
        "license": package_json.get("license", "указать лицензию"),
        "distribution": "бесплатно / open source",
        "short_description": package_json.get("description", "указать краткое описание"),
        "purpose": "решения пользовательских задач, описанных в README проекта",
        "feature_1": "указать ключевую функцию",
        "feature_2": "указать ключевую функцию",
        "feature_3": "указать ключевую функцию",
        "support": f"{support.get('provided_by', 'указать')} ({support.get('email', 'email не указан')}, регламент {support.get('response_time', 'не указан')})",
        "hosting_provider": hosting.get("provider", "указать провайдера"),
        "hosting_country": hosting.get("country", "Россия"),
        "hosting_city": hosting.get("city", "указать город"),
        "server_ip": hosting.get("server_ip", "указать IP"),
        "today": date.today().strftime("%d.%m.%Y"),
    }

    out = project / args.out
    out.mkdir(parents=True, exist_ok=True)
    for name, template in DOCS.items():
        (out / name).write_text(template.format(**values), encoding="utf-8")
    print(f"Created {len(DOCS)} draft documents in {out}")

if __name__ == "__main__":
    main()

