from pathlib import Path
import pymupdf
import html

PDF_FILE = "cam10-20-listening-cut.pdf"
OUTPUT_FILE = "merged_output.html"

doc = pymupdf.open(PDF_FILE)

all_pages = []

print(f"Total pages: {len(doc)}")

for page_num in range(len(doc)):

    page = doc.load_page(page_num)

    text = page.get_text("text")

    escaped_text = html.escape(text)

    escaped_text = escaped_text.replace("\n", "<br>\n")

    page_html = f"""
<section class="page-section" id="page-{page_num + 1}">

    <div class="page-content">
        {escaped_text}
    </div>
</section>
"""

    all_pages.append(page_html)

# =========================
# Final HTML
# =========================
final_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>cam10-20-listening-cut</title>

<style>

body {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px;
    font-family: Arial, sans-serif;
    background: white;
    color: black;
    line-height: 1.8;
}}

h1 {{
    text-align: center;
    margin-bottom: 50px;
    border-bottom: 3px solid black;
    padding-bottom: 20px;
}}

.page-section {{
    margin-bottom: 80px;
    padding-bottom: 40px;
    border-bottom: 1px solid #ccc;
}}

.page-section h2 {{
    margin-bottom: 25px;
}}

.page-content {{
    font-size: 18px;
    word-break: break-word;
}}

</style>

</head>

<body>

<h1>cam10-20-listening-cut</h1>

{''.join(all_pages)}

</body>
</html>
"""

Path(OUTPUT_FILE).write_text(final_html, encoding="utf-8")

doc.close()

print(f"\nSaved -> {OUTPUT_FILE}")