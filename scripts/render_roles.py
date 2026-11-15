#!/usr/bin/env python3
"""Render roles/*.html from content/roles/**/*.yml for the Metro-14 wiki."""
from __future__ import annotations

import html
from pathlib import Path

try:
    import yaml
except ImportError as e:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install pyyaml") from e

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "roles"
OUT = ROOT / "roles"
DISCORD = (
    '<p><strong>В случае наличия предложений по составу данной страницы '
    'обращайтесь в <a href="https://discord.gg/hjVpnug8C4" class="card-link"> Discord </a>.'
    '</strong> </p>'
)


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def paras(items: list[str]) -> str:
    return "\n".join(f"                <p>{esc(p)}</p>" for p in items if p)


def list_items(items: list[str], icon: str) -> str:
    return "\n".join(
        f'                    <li><i class="fas {icon}"></i> {esc(x)}</li>' for x in items if x
    )


def render(data: dict, slug_path: Path) -> str:
    title = data.get("title") or slug_path.stem
    access = data.get("access") or "свободный"
    icon = data.get("icon") or ""
    fraction = data.get("fraction_page") or "pages/roles.html"
    description = data.get("description") or []
    duties = data.get("duties") or []
    rights = data.get("rights") or []
    requirements = data.get("requirements") or []
    extra = data.get("extra") or []
    if isinstance(description, str):
        description = [description]
    if isinstance(extra, str):
        extra = [extra]

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <base href="/wiki/">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Википедия проекта - {esc(title)}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="resources/styles.css">
</head>
<body>
    <!-- Шапка сайта -->
    <div id="header-placeholder"></div>

    <!-- Навигация с вкладками -->
    <div id="nav-placeholder"></div>

    <!-- Основное содержимое -->
    <main class="container">
        <a href="{esc(fraction)}" class="back-link">
            <i class="fas fa-arrow-left"></i> Назад к списку ролей
        </a>

        <div class="role-detail">
            <div class="role-header">
                <div class="role-icon">
                     <img src="{esc(icon)}"
                     width="128"
                     height="128"
                     data-file-width="32"
                     data-file-height="32"
                     class="pixel-perfect">
                </div>
                <div class="role-title">
                    <h3>{esc(title)}</h3>
                    <p class="role-meta">Уровень доступа: {esc(access)}</p>
                </div>
            </div>

            <div class="role-section">
                <h4><i class="fas fa-info-circle"></i> Описание</h4>
{paras(description)}
            </div>

            <div class="role-section">
                <h4><i class="fas fa-tasks"></i> Обязанности</h4>
                <ul class="content-list">
{list_items(duties, "fa-check")}
                </ul>
            </div>

            <div class="role-section">
                <h4><i class="fas fa-unlock-alt"></i> Права и возможности</h4>
                <ul class="content-list">
{list_items(rights, "fa-star")}
                </ul>
            </div>

            <div class="role-section">
                <h4><i class="fas fa-user-plus"></i> Как получить роль</h4>
                <p>Роль не требует вхождение игрока в белый список. Но желательно соответствовать следующим требованиям:</p>
                <ul class="content-list">
{list_items(requirements, "fa-arrow-right")}
                </ul>
            </div>

            <div class="role-section">
                <h4><i class="fas fa-file-alt"></i> Дополнительная информация</h4>
{paras(extra)}
                {DISCORD}
            </div>
        </div>
    </main>

    <!-- Футер -->
    <div id="footer-placeholder"></div>

    <script src="resources/main.js"></script>
</body>
</html>
"""


def main() -> None:
    if not CONTENT.exists():
        raise SystemExit(f"missing {CONTENT}")
    count = 0
    for yml in sorted(CONTENT.rglob("*.yml")):
        data = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
        rel = yml.relative_to(CONTENT).with_suffix(".html")
        out = OUT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(data, yml), encoding="utf-8", newline="\n")
        count += 1
        print(f"rendered {out.relative_to(ROOT)}")
    print(f"ok: {count} role page(s)")


if __name__ == "__main__":
    main()
