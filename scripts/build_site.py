import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote


ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".obsidian",
    ".trash",
    ".venv",
    ".venv-pages",
    "__pycache__",
    "docs",
    "node_modules",
    "scripts",
    "site",
    "translations",
}

WIKILINK_RE = re.compile(r"(!?)\[\[([^\]]+)\]\]")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(.*?)\1")


def is_excluded(path):
    """判断路径是否包含需要排除的目录。"""
    return any(
        part in EXCLUDED_DIRS or part.startswith(".")
        for part in path.parts
    )


def find_markdown_files():
    """查找仓库中的所有中文原始 Markdown 笔记。"""
    markdown_files = []

    for path in ROOT_DIR.rglob("*.md"):
        relative_path = path.relative_to(ROOT_DIR)

        if is_excluded(relative_path):
            continue

        if relative_path == Path("README.md"):
            continue

        markdown_files.append(path)

    return sorted(markdown_files)


def build_note_index(markdown_files):
    """建立笔记名称索引，用于解析 Obsidian 双链。"""
    index = {}

    for path in markdown_files:
        relative_path = path.relative_to(ROOT_DIR)
        relative_name = relative_path.as_posix()
        relative_stem = relative_path.with_suffix("").as_posix()

        keys = {
            relative_name,
            relative_stem,
            path.name,
            path.stem,
        }

        for key in keys:
            normalized_key = key.casefold()

            if normalized_key not in index:
                index[normalized_key] = path
            elif index[normalized_key] != path:
                index[normalized_key] = None

    return index


def resolve_wikilink(target, note_index):
    """根据双链目标查找对应的 Markdown 文件。"""
    note_part, separator, heading = target.partition("#")
    note_part = note_part.strip().lstrip("/")

    if not note_part:
        return None, heading if separator else ""

    if note_part.lower().endswith(".md"):
        note_part = note_part[:-3]

    candidates = [
        note_part,
        f"{note_part}.md",
        Path(note_part).name,
        Path(note_part).stem,
    ]

    for candidate in candidates:
        result = note_index.get(candidate.casefold())

        if result is not None:
            return result, heading if separator else ""

    return None, ""


def make_heading_anchor(heading):
    """将标题转换为 Markdown 锚点。"""
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading)
    heading = re.sub(r"\s+", "-", heading)

    return heading


def replace_wikilinks(text, source_file, note_index):
    """将能够解析的 Obsidian 普通双链转换为 Markdown 链接。"""

    def replace_match(match):
        # 暂时保留 Obsidian 嵌入语法，不将其错误转换成普通链接。
        if match.group(1) == "!":
            return match.group(0)

        target_expression = match.group(2).strip()

        target, separator, display_text = target_expression.partition("|")

        target = target.strip()
        display_text = display_text.strip()

        if not display_text:
            display_text = Path(
                target.split("#", 1)[0]
            ).stem

        target_file, heading = resolve_wikilink(
            target,
            note_index
        )

        if target_file is None:
            return match.group(0)

        source_doc = DOCS_DIR / source_file.relative_to(ROOT_DIR)
        target_doc = DOCS_DIR / target_file.relative_to(ROOT_DIR)

        relative_link = os.path.relpath(
            target_doc,
            source_doc.parent
        ).replace(os.sep, "/")

        if heading:
            relative_link += "#" + make_heading_anchor(heading)

        relative_link = quote(
            relative_link,
            safe="/-_.#"
        )

        return f"[{display_text}]({relative_link})"

    return WIKILINK_RE.sub(replace_match, text)


def process_markdown(text, source_file, note_index):
    """处理 Markdown，同时保留代码块和行内代码中的原始内容。"""
    lines = text.splitlines(keepends=True)

    processed_lines = []
    fence_char = None
    fence_length = 0

    for line in lines:
        fence_match = FENCE_RE.match(line)

        if fence_match:
            marker = fence_match.group(1)

            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)

            elif (
                marker[0] == fence_char
                and len(marker) >= fence_length
            ):
                fence_char = None
                fence_length = 0

            processed_lines.append(line)
            continue

        if fence_char is not None:
            processed_lines.append(line)
            continue

        parts = INLINE_CODE_RE.split(line)

        for index in range(0, len(parts), 3):
            parts[index] = replace_wikilinks(
                parts[index],
                source_file,
                note_index
            )

        processed_lines.append("".join(parts))

    return "".join(processed_lines)


def clean_docs():
    """删除旧的构建目录并重新创建 docs。"""
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)

    DOCS_DIR.mkdir(parents=True)


def copy_markdown_files(markdown_files, note_index):
    """复制并处理所有 Markdown 笔记。"""
    for source_file in markdown_files:
        relative_path = source_file.relative_to(ROOT_DIR)
        target_file = DOCS_DIR / relative_path

        target_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with source_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()

        processed_content = process_markdown(
            content,
            source_file,
            note_index
        )

        with target_file.open(
            "w",
            encoding="utf-8"
        ) as file:
            file.write(processed_content)


def create_project_homepages(markdown_files):
    """为每个项目生成笔记目录首页。"""
    projects = {}

    for path in markdown_files:
        relative_path = path.relative_to(ROOT_DIR)

        if len(relative_path.parts) < 2:
            continue

        project = relative_path.parts[0]
        project_relative = Path(*relative_path.parts[1:])

        projects.setdefault(project, []).append(project_relative)

    for project, files in projects.items():
        homepage = [
            f"# {project}",
            "",
            "## 笔记列表",
            "",
        ]

        for file_path in sorted(files):
            link = quote(
                file_path.as_posix(),
                safe="/-_."
            )

            title = file_path.with_suffix("").as_posix()

            homepage.append(f"- [{title}]({link})")

        homepage.append("")

        homepage_file = DOCS_DIR / project / "index.md"

        homepage_file.write_text(
            "\n".join(homepage),
            encoding="utf-8"
        )


def create_homepage(markdown_files):
    """生成中文网站首页。"""
    projects = sorted({
        path.relative_to(ROOT_DIR).parts[0]
        for path in markdown_files
        if len(path.relative_to(ROOT_DIR).parts) > 1
    })

    homepage = [
        "# 42 Common Core 中文学习笔记",
        "",
        "这里是我的 42 Common Core 中文学习笔记 -- Hua",
        "",
        "## 学习项目",
        "",
    ]

    for project in projects:
        project_link = quote(
            project,
            safe="/-_."
        )

        homepage.append(
            f"- [{project}]({project_link}/index.md)"
        )

    homepage.append("")

    homepage_file = DOCS_DIR / "index.md"

    homepage_file.write_text(
        "\n".join(homepage),
        encoding="utf-8"
    )


def build_site_content():
    """执行中文笔记网站内容构建。"""
    print("Scanning Chinese Markdown notes...")

    markdown_files = find_markdown_files()

    print(f"Found {len(markdown_files)} Markdown files.")

    note_index = build_note_index(markdown_files)

    clean_docs()

    copy_markdown_files(
        markdown_files,
        note_index
    )

    create_project_homepages(markdown_files)

    create_homepage(markdown_files)

    print("Website content generated successfully.")
    print(f"Output directory: {DOCS_DIR}")


def main():
    print("Building Chinese Obsidian notes...")

    build_site_content()


if __name__ == "__main__":
    main()
