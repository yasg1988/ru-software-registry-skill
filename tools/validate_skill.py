from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ru-software-registry"
SKILL_MD = SKILL / "SKILL.md"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def main() -> int:
    if not SKILL_MD.exists():
        return fail(f"Missing {SKILL_MD}")

    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return fail("SKILL.md must start with YAML frontmatter")

    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError:
        return fail("SKILL.md frontmatter is not closed")

    if not re.search(r"(?m)^name:\s*ru-software-registry\s*$", frontmatter):
        return fail("Frontmatter must contain name: ru-software-registry")

    match = re.search(r"(?m)^description:\s*(.+)\s*$", frontmatter)
    if not match:
        return fail("Frontmatter must contain description")

    description = match.group(1).strip().strip('"')
    if len(description) < 80:
        return fail("Description is too short for reliable triggering")

    if "# Реестр российского ПО" not in body:
        return fail("Body must contain the main skill heading")

    required = [
        SKILL / "scripts" / "audit_project.py",
        SKILL / "scripts" / "generate_registry_docs.py",
        SKILL / "references" / "document-package.md",
        SKILL / "references" / "portal-workflow.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        return fail("Missing required files: " + ", ".join(missing))

    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

