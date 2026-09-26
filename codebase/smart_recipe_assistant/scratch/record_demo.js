const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer-core");

const FRAMES_DIR = path.join(__dirname, "frames");
if (!fs.existsSync(FRAMES_DIR)) {
  fs.mkdirSync(FRAMES_DIR, { recursive: true });
} else {
  for (const f of fs.readdirSync(FRAMES_DIR)) {
    fs.unlinkSync(path.join(FRAMES_DIR, f));
  }
}

let frameIndex = 0;

async function recordFrames(page, durationMs, fps = 5) {
  const intervalMs = Math.round(1000 / fps);
  const steps = Math.ceil(durationMs / intervalMs);
  for (let i = 0; i < steps; i++) {
    const filename = path.join(FRAMES_DIR, `frame_${String(frameIndex).padStart(5, "0")}.png`);
    await page.screenshot({ path: filename, type: "png" });
    frameIndex++;
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}

(async () => {
  console.log("Launching browser for demo recording...");
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/google-chrome",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--headless=new"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });

  const appUrl = "https://smart-recipe-assistant-frontend-260088329841.us-central1.run.app";
  console.log("Navigating to:", appUrl);
  await page.goto(appUrl, { waitUntil: "networkidle2" });

  // Initial display freeze (1.5 seconds)
  await recordFrames(page, 1500);

  // 1. First Prompt: Click high-protein dinner prompt chip
  console.log("Submitting 1st prompt: High-protein dinner...");
  const promptChip = await page.$(".prompt-chip");
  if (promptChip) {
    await promptChip.click();
  } else {
    await page.type("#input", "Find a healthy high-protein vegetarian dinner recipe");
    await page.click("form button");
  }

  // Wait and capture frames while agent processes and returns reply
  console.log("Waiting for 1st agent response...");
  await recordFrames(page, 4000);

  // Wait for agent bubble to contain text
  try {
    await page.waitForFunction(
      () => {
        const bubbles = document.querySelectorAll(".msg.agent .bubble");
        if (bubbles.length === 0) return false;
        const last = bubbles[bubbles.length - 1];
        return last.textContent && !last.textContent.includes("…");
      },
      { timeout: 12000 }
    );
  } catch (e) {
    console.log("Timeout waiting for 1st reply, continuing...");
  }

  // Record 1st reply card in UI (2 seconds)
  await recordFrames(page, 2000);

  // 2. Second Richer Prompt: Tool Call & Calculation / Scaling
  console.log("Submitting 2nd richer prompt...");
  const inputSelector = "#input";
  await page.click(inputSelector);
  await page.type(inputSelector, "Scale a recipe for 6 people and convert 2 cups flour to grams");
  await recordFrames(page, 800);
  await page.click("form button");

  // Wait and capture frames while agent processes tools & scaling calculations
  console.log("Waiting for 2nd agent response...");
  await recordFrames(page, 4000);

  try {
    await page.waitForFunction(
      () => {
        const bubbles = document.querySelectorAll(".msg.agent .bubble");
        if (bubbles.length < 2) return false;
        const last = bubbles[bubbles.length - 1];
        return last.textContent && !last.textContent.includes("…");
      },
      { timeout: 15000 }
    );
  } catch (e) {
    console.log("Timeout waiting for 2nd reply, continuing...");
  }

  // Final hold on completed dialogue layout (3 seconds)
  await recordFrames(page, 3000);

  console.log(`Demo recording finished! Captured ${frameIndex} frames.`);
  await browser.close();
})();
