from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / ".mkdocs" / "docs"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".claude",
    ".mkdocs",
    "site",
    "tools",
    "新建文件夹",
}

EXCLUDED_FILE_SUFFIXES = {
    ".env",
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".jks",
    ".keystore",
    ".sqlite",
    ".db",
    ".cer",
    ".crt",
    ".der",
    ".asc",
}

EXCLUDED_NAME_FRAGMENTS = {
    "secret",
    "token",
    "password",
    "passwd",
    "credential",
}


def copy_path(relative_path: str) -> None:
    source = ROOT / relative_path
    target = DOCS_DIR / relative_path

    if not source.exists():
        return

    if source.is_dir():
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns(
                ".gitkeep",
                "*.env",
                "*.key",
                "*.pem",
                "*.p12",
                "*.pfx",
                "*.jks",
                "*.keystore",
                "*.sqlite",
                "*.db",
                "*.cer",
                "*.crt",
                "*.der",
                "*.asc",
                "*secret*",
                "*token*",
                "*password*",
                "*passwd*",
                "*credential*",
            ),
            dirs_exist_ok=True,
        )
        return

    lower_name = source.name.lower()
    if source.suffix.lower() in EXCLUDED_FILE_SUFFIXES:
        return
    if any(fragment in lower_name for fragment in EXCLUDED_NAME_FRAGMENTS):
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    copy_path("README.md")
    for child in sorted(ROOT.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        if child.name in EXCLUDED_DIRS:
            continue
        copy_path(child.name)


if __name__ == "__main__":
    main()
