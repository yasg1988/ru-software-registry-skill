import subprocess
import sys
import os
from pathlib import Path

root = Path(__file__).resolve().parents[1]
skill = root / "skills" / "ru-software-registry"
validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"

if not validator.exists():
    print(f"Validator not found: {validator}", file=sys.stderr)
    sys.exit(1)

env = os.environ.copy()
env["PYTHONUTF8"] = "1"
raise SystemExit(subprocess.call([sys.executable, str(validator), str(skill)], env=env))
