import os
import shutil


TRANSLATION_DIR = "translations"
DOCS_DIR = "docs"

LANGUAGES = {
    "zh": "中文",
    "en": "English",
    "fr": "Français",
}


EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".obsidian",
    ".venv-pages",
    "docs",
    "site",
    "scripts",
    "translations",
}


def find_projects():
    projects = []

    for entry in sorted(os.listdir(".")):
        if not os.path.isdir(entry):
            continue

        if entry in EXCLUDED_DIRS:
            continue

        if entry.startswith("."):
            continue

        projects.append(entry)

    return projects


def clean_docs():
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)

    os.makedirs(DOCS_DIR)


def copy_markdown_files(
    source_dir,
    target_dir
):
    if not os.path.exists(source_dir):
        return

    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in files:
            if not filename.endswith(".md"):
                continue

            source_file = os.path.join(
                root,
                filename
            )

            relative_path = os.path.relpath(
                source_file,
                source_dir
            )

            target_file = os.path.join(
                target_dir,
                relative_path
            )

            os.makedirs(
                os.path.dirname(target_file),
                exist_ok=True
            )

            shutil.copy2(
                source_file,
                target_file
            )


def create_homepage():
    homepage = """# <span style="font-weight: bold;">42 Common Core Notes</span>

### <span style="color: #668F80; font-weight: bold;">Welcome to my 42 Common Core learning notes -- Hua</span>

## <span style="color: #5C7FA3; font-weight: bold;">Languages</span>

- [中文](zh/index.md)
- [English](en/index.md)
- [Français](fr/index.md)
"""

    homepage_file = os.path.join(
        DOCS_DIR,
        "index.md"
    )

    with open(
        homepage_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(homepage)


def create_language_homepage(
    language_code
):
    if language_code == "zh":
        content = """# 中文笔记

这里是我的 42 Common Core 中文学习笔记。
"""

    elif language_code == "en":
        content = """# English Notes

These are my English 42 Common Core learning notes.
"""

    else:
        content = """# Notes en français

Voici mes notes d'apprentissage du 42 Common Core en français.
"""

    language_dir = os.path.join(
        DOCS_DIR,
        language_code
    )

    os.makedirs(
        language_dir,
        exist_ok=True
    )

    homepage_file = os.path.join(
        language_dir,
        "index.md"
    )

    with open(
        homepage_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(content)


def build_language(
    language_code,
    source_base
):
    target_dir = os.path.join(
        DOCS_DIR,
        language_code
    )

    for project in find_projects():
        source_dir = os.path.join(
            source_base,
            project
        )

        if not os.path.exists(source_dir):
            continue

        project_target = os.path.join(
            target_dir,
            project
        )

        copy_markdown_files(
            source_dir,
            project_target
        )


def build_site_content():
    clean_docs()

    create_homepage()

    create_language_homepage("zh")
    create_language_homepage("en")
    create_language_homepage("fr")

    build_language(
        "zh",
        "."
    )

    build_language(
        "en",
        os.path.join(
            TRANSLATION_DIR,
            "en"
        )
    )

    build_language(
        "fr",
        os.path.join(
            TRANSLATION_DIR,
            "fr"
        )
    )


def main():
    print("Building website content...")

    projects = find_projects()

    print(
        f"Found {len(projects)} projects:"
    )

    for project in projects:
        print(
            f"  - {project}"
        )

    build_site_content()

    print(
        "Website content generated successfully."
    )

    print(
        f"Output directory: {DOCS_DIR}"
    )


if __name__ == "__main__":
    main()
