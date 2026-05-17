const puppeteer = require("puppeteer");
const { PDFDocument, StandardFonts, rgb } = require("pdf-lib");
const fs = require("fs");
const path = require("path");

const PREFIX = "cleaned_cam";
const OUTPUT = "ALL_CAMBRIDGE.pdf";

function getFiles() {
  return fs.readdirSync(".")
    .filter(f => f.startsWith(PREFIX) && f.endsWith(".html"))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
}

async function htmlToPdf(browser, file) {
  const page = await browser.newPage();

  const filePath = "file://" + path.resolve(file);
  await page.goto(filePath, { waitUntil: "networkidle0" });

  await page.addStyleTag({
    content: `@page { margin: 0 } body { margin: 0 }`
  });

  await autoScroll(page);

  const pdfBuffer = await page.pdf({
    format: "A4",
    printBackground: true,
    margin: 0,
    scale: 1
  });

  await page.close();
  return pdfBuffer;
}

async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise(resolve => {
      let total = 0;
      const distance = 500;

      const timer = setInterval(() => {
        window.scrollBy(0, distance);
        total += distance;

        if (total >= document.body.scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 100);
    });
  });
}

// =========================
// MAIN
// =========================
(async () => {
  const files = getFiles();
  const browser = await puppeteer.launch();

  const pdfDoc = await PDFDocument.create();
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);

  const indexData = [];
  let currentPage = 0;

  // =====================
  // MERGE
  // =====================
  for (const file of files) {
    console.log("▶", file);

    const pdfBytes = await htmlToPdf(browser, file);
    const tempDoc = await PDFDocument.load(pdfBytes);

    const pageCount = tempDoc.getPageCount();

    indexData.push({
      name: file.replace("cleaned_", "").replace(".html", "").toUpperCase(),
      page: currentPage + 1
    });

    const pages = await pdfDoc.copyPages(
      tempDoc,
      tempDoc.getPageIndices()
    );

    pages.forEach(p => pdfDoc.addPage(p));

    currentPage += pageCount;
  }

  await browser.close();

  // =====================
  // TEXT INDEX (page 1)
  // =====================
  const indexPage = pdfDoc.insertPage(0, [595, 842]);

  indexPage.drawText("TABLE OF CONTENTS", {
    x: 150,
    y: 800,
    size: 18,
    font
  });

  let y = 760;
  const lineHeight = 14;

  indexData.slice(0, 50).forEach((item, i) => {
    const text = `${i + 1}. ${item.name} .... ${item.page + 1}`;

    indexPage.drawText(text, {
      x: 70,
      y,
      size: 10,
      font,
      color: rgb(0, 0, 0)
    });

    y -= lineHeight;
  });

  // =====================
  // 🔥 BOOKMARK (SIDEBAR)
  // =====================
  const outline = pdfDoc.catalog.getOrCreateOutlines();

  indexData.forEach((item, i) => {
    outline.addItem(item.name, {
      pageIndex: item.page, // vì đã insert index page
    });
  });

  // =====================
  // SAVE
  // =====================
  const finalBytes = await pdfDoc.save();
  fs.writeFileSync(OUTPUT, finalBytes);

  console.log("✅ DONE →", OUTPUT);
})();