#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION_DIR = ROOT / "tests" / "integration"


def resolve_target(target: str | None) -> str:
    if not target:
        return str(INTEGRATION_DIR)

    if "::" in target:
        file_part, test_part = target.split("::", 1)
    else:
        file_part, test_part = target, None

    candidate = Path(file_part)
    if not candidate.suffix:
        if not file_part.startswith("test_"):
            file_part = f"test_{file_part}"
        candidate = Path(f"{file_part}.py")

    if not candidate.is_absolute():
        if str(candidate).startswith("tests/"):
            candidate = ROOT / candidate
        else:
            candidate = INTEGRATION_DIR / candidate

    return f"{candidate}::{test_part}" if test_part else str(candidate)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run integration tests. Supports folder, single file, or single test."
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Examples: test_users | test_users.py | test_users::test_create_user_creates_db_object",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Run pytest with -q")
    parser.add_argument(
        "--db-url",
        default="sqlite:///./integration_test.db",
        help="Base relational DB URL for tests.",
    )
    parser.add_argument(
        "--separate-db",
        action="store_true",
        help="Use separate DB instance per run (suffix applied for sqlite DB file).",
    )
    parser.add_argument(
        "--db-suffix",
        default=None,
        help="Optional custom DB suffix for separate DB mode.",
    )
    args, passthrough = parser.parse_known_args()

    target = resolve_target(args.target)
    command = [sys.executable, "-m", "pytest", target]
    if args.quiet:
        command.append("-q")
    command.extend(passthrough)

    env = os.environ.copy()
    env["TEST_DATABASE_URL"] = args.db_url
    env["TEST_DB_ISOLATED"] = "1" if args.separate_db else "0"
    if args.separate_db:
        env["TEST_DB_RUN_SUFFIX"] = args.db_suffix or uuid4().hex[:8]

    db_name = env["TEST_DATABASE_URL"]
    if env["TEST_DB_ISOLATED"] == "1":
        db_name = f"{db_name} (suffix={env['TEST_DB_RUN_SUFFIX']})"

    print("Running:", " ".join(command))
    print("Using test DB:", db_name)
    return subprocess.call(command, cwd=ROOT, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
