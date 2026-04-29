from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / ".mkdocs" / "docs"

INCLUDE_PATHS = [
    "README.md",
    "01_Java基础",
    "02_SpringBoot与Spring生态",
    "03_SSE流式传输",
    "04_数据库与分库分表",
    "05_Redis",
    "06_消息队列",
    "07_工作流与编排",
    "08_高可用与稳定性",
    "09_微服务与分布式",
    "10_任务调度",
    "11_可观测性",
    "12_AI工程化场景题",
    "13_项目经验高频问答",
    "14_面试作答方法论",
    "15_附录",
    "16_设计模式",
    "17_参考资料",
    "源码学习",
]


def copy_path(relative_path: str) -> None:
    source = ROOT / relative_path
    target = DOCS_DIR / relative_path

    if not source.exists():
        return

    if source.is_dir():
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns(".gitkeep"),
            dirs_exist_ok=True,
        )
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for path in INCLUDE_PATHS:
        copy_path(path)


if __name__ == "__main__":
    main()

