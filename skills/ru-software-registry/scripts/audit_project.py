#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"npm_[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"dckr_pat_[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)(token|secret|password|passwd|api_key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
]

TEXT_EXT = {
    ".md", ".txt", ".json", ".js", ".ts", ".py", ".yml", ".yaml", ".env",
    ".example", ".toml", ".ini", ".ps1", ".sh", ".dockerfile"
}

def exists(root: Path, *names: str) -> bool:
    return any((root / name).exists() for name in names)

def scan_secrets(root: Path):
    findings = []
    ignored = {"node_modules", ".git", "dist", "build", ".next", "vendor"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXT and path.name not in {"Dockerfile", ".env", ".gitignore"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append({"file": str(path.relative_to(root)), "line": line, "pattern": pattern.pattern})
    return findings

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    checks = {
        "readme": exists(root, "README.md", "README.ru.md"),
        "license": exists(root, "LICENSE", "LICENSE.md"),
        "package_json": exists(root, "package.json"),
        "dockerfile": exists(root, "Dockerfile", "docker-compose.yml", "compose.yml"),
        "gitignore": exists(root, ".gitignore"),
        "github_workflows": (root / ".github" / "workflows").exists(),
    }
    secrets = scan_secrets(root)
    result = {
        "project": str(root),
        "checks": checks,
        "secret_findings": secrets,
        "ready_score": sum(1 for ok in checks.values() if ok),
        "ready_score_max": len(checks),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if secrets:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

