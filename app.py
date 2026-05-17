from pathlib import Path
import re

ROOT_DIR = Path(".")

HOME_URL = "https://shiny-hall-e5c5.cuxuanthoai.workers.dev/"

# New black & white button
NEW_HOME_BUTTON = f"""
<div class="home-button-wrapper">
    <a href="{HOME_URL}" class="home-button">
        Home
    </a>
</div>

<style>
.home-button-wrapper {{
    margin: 20px 0;
}}

.home-button {{
    display: inline-block;
    padding: 10px 18px;
    border: 2px solid #000;
    background: #fff;
    color: #000;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 600;
    font-family: Arial, sans-serif;
    transition: 0.2s ease;
}}

.home-button:hover {{
    background: #000;
    color: #fff;
}}
</style>
"""

pattern = re.compile(
    r"cleaned_cam(1[0-9]|20)_test[1-4]\.html$",
    re.IGNORECASE
)

updated_count = 0

for file in ROOT_DIR.rglob("*.html"):

    if not pattern.search(file.name):
        continue

    print(f"Updating: {file}")

    content = file.read_text(encoding="utf-8")

    # =========================
    # Remove OLD button blocks
    # =========================

    # remove old inline button div
    content = re.sub(
        r'<div[^>]*>\s*<a href="https://shiny-hall-e5c5\.cuxuanthoai\.workers\.dev/".*?</div>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # remove old style block if exists
    content = re.sub(
        r'<style>.*?home-button.*?</style>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # =========================
    # Insert new button
    # =========================
    if "<body" in content.lower():

        content = re.sub(
            r'(<body[^>]*>)',
            r'\1\n' + NEW_HOME_BUTTON,
            content,
            count=1,
            flags=re.IGNORECASE
        )

    else:
        content = NEW_HOME_BUTTON + content

    file.write_text(content, encoding="utf-8")

    updated_count += 1

    print("  -> done")

print("\n===================")
print(f"Updated files: {updated_count}")
print("===================")