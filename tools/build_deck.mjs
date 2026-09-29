import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "/home/hariharan.c/Downloads/Snapdragon AI Lab Build & Present Challenge";
const SKILL_DIR = "/home/hariharan.c/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations";
const RUNTIME_PYTHON = "/home/hariharan.c/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const TMP_DIR = path.join(workspaceDir, ".codex-build");
const FINAL_PPTX = path.join(workspaceDir, "submission", "Rakshak_Edge_Pitch_Final.pptx");
await fs.mkdir(TMP_DIR, { recursive: true });
await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });

const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
const family = resolvePresentationFont({ fontFamily: "Aptos" });
const p = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const C = { bg: "#07130F", panel: "#0D1E18", ink: "#EEF8F2", muted: "#91A69C", line: "#234337", lime: "#B8FF5C", mint: "#64E6B0", red: "#FF6B62", amber: "#FFC85C" };

function box(slide, x, y, w, h, fill = "none", line = "none", radius = 0) {
  return slide.shapes.add({ geometry: "rect", position: { left: x, top: y, width: w, height: h }, fill, line: { fill: line, width: line === "none" ? 0 : 1 }, borderRadius: radius });
}
function text(slide, value, x, y, w, h, size = 24, color = C.ink, bold = false, opts = {}) {
  const s = slide.shapes.add({ geometry: "textbox", position: { left: x, top: y, width: w, height: h }, fill: "none", line: { fill: "none", width: 0 } });
  s.text = value;
  s.text.style = { typeface: family, fontSize: size, color, bold, autoFit: "shrinkText", ...opts };
  return s;
}
function base(slide, section, number) {
  slide.background.fill = C.bg;
  text(slide, "RAKSHAK EDGE", 66, 31, 260, 28, 13, C.lime, true, { letterSpacing: 1.8 });
  text(slide, `${number} / ${section}`, 1040, 32, 170, 25, 11, C.muted, true, { textAlign: "right" });
  box(slide, 66, 66, 1148, 1, C.line);
}
function notes(slide, copy) { slide.speakerNotes.textFrame.setText(copy); }

// 1. Cover
{
  const s = p.slides.add(); s.background.fill = C.bg;
  const hero = new Uint8Array(await fs.readFile(path.join(workspaceDir, "assets/screenshots/rakshak-hero.png")));
  s.images.add({ blob: hero, contentType: "image/png", alt: "Rakshak Edge product interface", fit: "cover", position: { left: 0, top: 0, width: 1280, height: 720 }, crop: { left: 0.43, top: 0.02, right: 0, bottom: 0.02 } });
  box(s, 0, 0, 735, 720, C.bg);
  text(s, "ON-DEVICE SOCIAL-ENGINEERING FIREWALL", 72, 92, 575, 28, 13, C.lime, true, { letterSpacing: 1.7 });
  text(s, "Rakshak\nEdge", 70, 140, 600, 210, 76, C.ink, true, { lineSpacing: 0.88 });
  text(s, "A private safety check before the user clicks, pays, or shares a secret", 76, 386, 535, 105, 26, C.muted, false, { lineSpacing: 1.16 });
  box(s, 76, 548, 212, 46, C.lime, C.lime, 8); text(s, "SNAPDRAGON X SERIES", 91, 560, 184, 22, 12, C.bg, true, { textAlign: "center", letterSpacing: 1.0 });
  text(s, "Hariharan C  |  2026", 76, 645, 300, 24, 13, C.muted);
  notes(s, "Product screenshot: Rakshak Edge local demo. Built for the Snapdragon AI Lab Build & Present Challenge.");
}

// 2. Problem
{
  const s = p.slides.add(); base(s, "PROBLEM", "01");
  text(s, "The critical moment happens before the tap", 68, 102, 935, 70, 42, C.ink, true);
  text(s, "A suspicious message exploits urgency and trust. Sending it to a cloud checker can expose the same private content the user is trying to protect.", 70, 184, 880, 80, 20, C.muted, false, { lineSpacing: 1.2 });
  box(s, 70, 310, 340, 236, C.panel, C.line, 18); text(s, "01", 94, 334, 55, 40, 24, C.lime, true); text(s, "Private content", 94, 386, 260, 36, 24, C.ink, true); text(s, "OTP messages, account alerts, payment handles, and personal context.", 94, 435, 270, 70, 17, C.muted);
  box(s, 470, 310, 340, 236, C.panel, C.line, 18); text(s, "02", 494, 334, 55, 40, 24, C.lime, true); text(s, "Fast manipulation", 494, 386, 260, 36, 24, C.ink, true); text(s, "Threats and rewards push the user to act before checking another channel.", 494, 435, 270, 70, 17, C.muted);
  box(s, 870, 310, 340, 236, C.panel, C.line, 18); text(s, "03", 894, 334, 55, 40, 24, C.lime, true); text(s, "Opaque verdicts", 894, 386, 260, 36, 24, C.ink, true); text(s, "A score alone cannot teach the user what triggered the warning or what to do next.", 894, 435, 270, 70, 17, C.muted);
  text(s, "Design question", 70, 610, 150, 22, 12, C.lime, true, { letterSpacing: 1.2 }); text(s, "Can a PC explain the risk locally, in the moment that matters?", 235, 599, 900, 42, 25, C.ink, true);
}

// 3. Product
{
  const s = p.slides.add(); base(s, "PRODUCT", "02");
  text(s, "One local workflow from suspicion to safe action", 68, 94, 1010, 60, 40, C.ink, true);
  const shot = new Uint8Array(await fs.readFile(path.join(workspaceDir, "assets/screenshots/rakshak-analysis.png")));
  s.images.add({ blob: shot, contentType: "image/png", alt: "Rakshak Edge analyzer with a sample KYC scam", fit: "cover", position: { left: 62, top: 177, width: 780, height: 500 }, crop: { left: 0, top: 0.08, right: 0, bottom: 0.04 }, geometry: "roundRect", borderRadius: 14 });
  text(s, "Paste", 900, 200, 230, 38, 25, C.lime, true); text(s, "Message, URL, UPI request, or QR payload", 900, 242, 265, 54, 17, C.muted);
  box(s, 900, 322, 270, 1, C.line);
  text(s, "Understand", 900, 350, 230, 38, 25, C.lime, true); text(s, "Risk score with visible evidence and extracted entities", 900, 392, 265, 62, 17, C.muted);
  box(s, 900, 480, 270, 1, C.line);
  text(s, "Act safely", 900, 510, 230, 38, 25, C.lime, true); text(s, "Independent verification path without another risky link", 900, 552, 265, 62, 17, C.muted);
  notes(s, "Product screenshot from the running local app. The default build sends no content outside 127.0.0.1.");
}

// 4. Architecture
{
  const s = p.slides.add(); base(s, "CORE INNOVATION", "03");
  text(s, "Scams unfold across a conversation", 68, 96, 1040, 58, 40, C.ink, true);
  text(s, "Rakshak connects the stages that single-message classifiers lose.", 70, 157, 900, 38, 19, C.muted);
  const turns = [
    ["01", "IDENTITY SETUP", "Hi, this is Arun from finance. Save my new number.", "42", C.amber],
    ["02", "ISOLATION", "I am boarding a flight. Do not call. Keep this confidential.", "55", C.amber],
    ["03", "EXTRACTION", "Purchase five vouchers and send the codes before 4 PM.", "72", C.red],
  ];
  turns.forEach((m,i)=>{const y=232+i*112;box(s,70,y,730,88,"#0B1C16",C.line,12);text(s,m[0],92,y+26,48,26,14,C.lime,true);text(s,m[1],158,y+14,185,24,12,m[4],true,{letterSpacing:1.1});text(s,m[2],158,y+43,535,27,16,C.ink);text(s,m[3],716,y+23,56,36,27,m[4],true,{textAlign:"right"});});
  box(s, 850, 232, 350, 312, "#10271E", C.lime, 18);
  text(s, "81", 888, 265, 160, 88, 68, C.red, true); text(s, "/100", 1034, 313, 72, 28, 16, C.muted);
  text(s, "COORDINATED SCAM", 890, 374, 240, 22, 12, C.red, true, {letterSpacing:1.2});
  text(s, "Identity setup\nIsolation and pressure\nMoney or access request", 890, 416, 268, 92, 19, C.ink, true, {lineSpacing:1.28});
  box(s, 70, 600, 1130, 48, C.lime, C.lime, 8); text(s, "The raw conversation is processed in memory and never appears in the exported report.", 92, 613, 1088, 22, 16, C.bg, true);
  notes(s, "Working conversation analyzer. Input contains three messages. Output: 81/100, three attack-chain stages, zero network calls, and no raw message persistence.");
}

// 5. Architecture
{
  const s = p.slides.add(); base(s, "TECHNICAL IMPLEMENTATION", "04");
  text(s, "Hybrid reasoning keeps security explainable", 68, 96, 1110, 64, 38, C.ink, true);
  text(s, "Transparent signals stay authoritative. A compact classifier adds context today; the production profile moves the encoder to the Hexagon NPU.", 70, 164, 1080, 56, 18, C.muted);
  const stages = [
    ["Input boundary", "Loopback API\nNo persistence", C.panel],
    ["Evidence engines", "URL + entity rules\nLocal semantic model", "#10261D"],
    ["Snapdragon profile", "INT8 encoder\nONNX Runtime + QNN", "#143021"],
    ["Decision layer", "Calibrated score\nReasons + safe action", "#173927"],
  ];
  stages.forEach((it, i) => {
    const x = 65 + i * 300; box(s, x, 275, 245, 210, it[2], i === 2 ? C.lime : C.line, 16);
    text(s, `0${i+1}`, x+22, 294, 40, 25, 14, C.lime, true);
    text(s, it[0], x+22, 342, 200, 36, 23, C.ink, true);
    text(s, it[1], x+22, 397, 195, 60, 17, C.muted, false, { lineSpacing: 1.2 });
    if(i<3){ text(s, ">", x+258, 360, 30, 38, 25, C.lime, true, { textAlign: "center" }); }
  });
  box(s, 66, 550, 1148, 84, "#0B2219", C.line, 12);
  text(s, "Graceful fallback", 90, 572, 190, 28, 17, C.lime, true); text(s, "QNN unavailable? ONNX Runtime uses CPU. Model absent? The deterministic engine still delivers a complete, testable product.", 286, 570, 875, 42, 18, C.ink);
  notes(s, "Technical references: ONNX Runtime QNN Execution Provider, https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html; Qualcomm AI Hub, https://aihub.qualcomm.com/");
}

// 6. AI evidence
{
  const s = p.slides.add(); base(s, "LIVE EVIDENCE", "05");
  text(s, "AI catches the scam\nwithout a malicious link", 68, 103, 970, 88, 34, C.ink, true, { lineSpacing: 1.0 });
  box(s, 70, 190, 305, 305, C.panel, C.line, 18);
  text(s, "72", 106, 218, 150, 105, 76, C.red, true); text(s, "/100", 246, 275, 70, 34, 18, C.muted);
  text(s, "HIGH RISK", 106, 338, 150, 25, 12, C.red, true, { letterSpacing: 1.5 }); text(s, "Stop and verify independently", 106, 382, 220, 68, 25, C.ink, true);
  const ev = [["Semantic scam pattern", "99.8% high-risk confidence", "AI"], ["Voucher purchase", "Financial coercion", "RULE"], ["No URL", "Nothing for a link scanner", "0"], ["No OTP or UPI", "Meaning comes from context", "0"]];
  ev.forEach((a,i)=>{const y=190+i*88;box(s,430,y,760,70,"#0B1C16",C.line,10);box(s,450,y+20,10,10,i<2?C.red:C.mint,i<2?C.red:C.mint,5);text(s,a[0],480,y+15,270,28,18,C.ink,true);text(s,a[1],760,y+17,290,25,15,C.muted);text(s,a[2],1082,y+17,76,25,14,C.lime,true,{textAlign:"right"});});
  box(s, 70, 550, 1120, 72, "#173323", C.lime, 10); text(s, "SAFEST NEXT STEP", 95, 568, 190, 20, 12, C.lime, true, { letterSpacing: 1.1 }); text(s, "Call the finance head using the number already in your contacts.", 302, 562, 820, 33, 22, C.ink, true);
  notes(s, "Input: Finance head here. I cannot take calls. Purchase five vouchers and send the numbers before the client meeting. Output from the checked-in hybrid analyzer: high risk, 72/100; local semantic model high-risk confidence 99.77%. The score is a risk indicator, not proof of fraud.");
}

// 7. Evaluation
{
  const s = p.slides.add(); base(s, "MEASURED EVIDENCE", "06");
  text(s, "A locked suite tests the complete product", 68, 104, 1040, 62, 38, C.ink, true);
  const metrics = [["97.78%", "45-case system suite"], ["15 / 15", "high-risk cases"], ["15 / 15", "medium-risk cases"], ["10 / 10", "regression tests"]];
  metrics.forEach((m,i)=>{const x=70+i*285;box(s,x,220,255,170,i===0?C.lime:C.panel,i===0?C.lime:C.line,16);text(s,m[0],x+22,247,205,58,38,i===0?C.bg:C.lime,true);text(s,m[1],x+22,324,205,45,15,i===0?"#315512":C.muted);});
  box(s, 70, 445, 1120, 112, "#0B1C16", C.line, 12);
  text(s, "ONE DISCLOSED ERROR", 94, 468, 210, 22, 12, C.amber, true, {letterSpacing:1.0});
  text(s, "A safety reminder about OTP and PIN is conservatively rated medium instead of low.", 94, 505, 790, 30, 20, C.ink, true);
  text(s, "39", 1040, 474, 90, 54, 38, C.amber, true, {textAlign:"right"});
  text(s, "The system suite is balanced, never used for training, and prints every error. The model-only holdout remains 94.44%.", 72, 600, 1080, 46, 17, C.muted);
  notes(s, "Reproduce with python benchmarks/evaluate_system.py. 44 of 45 balanced non-training cases correct. All 15 high-risk and 15 medium-risk cases correct. The evaluator prints the single false positive.");
}

// 8. Snapdragon fit
{
  const s = p.slides.add(); base(s, "SNAPDRAGON ADVANTAGE", "07");
  text(s, "Local protection is the product advantage", 68, 104, 1040, 64, 38, C.ink, true);
  const metrics = [["0", "cloud calls by default"], ["< 1 ms", "median reference CPU"], ["INT8", "production model target"], ["45 TOPS", "Snapdragon X Elite NPU"]];
  metrics.forEach((m,i)=>{const x=70+i*285;box(s,x,225,255,170,i===3?C.lime:C.panel,i===3?C.lime:C.line,16);text(s,m[0],x+22,252,205,58,38,i===3?C.bg:C.lime,true);text(s,m[1],x+22,329,205,45,15,i===3?"#315512":C.muted);});
  text(s, "Same private API, stronger production encoder", 70, 470, 720, 35, 24, C.ink, true);
  text(s, "The reference model makes the complete demo reproducible today. On Snapdragon X Series, the production profile swaps in an INT8 encoder through ONNX Runtime QNN while keeping the evidence layer, conversation logic, and offline boundary unchanged.", 70, 520, 1080, 88, 19, C.muted, false, {lineSpacing:1.25});
  notes(s, "Qualcomm states Snapdragon X Elite includes a Hexagon NPU with up to 45 TOPS. Source: Snapdragon X Elite product brief, https://docs.qualcomm.com/bundle/publicresource/87-71417-1_REV_D_Snapdragon_X_Elite_Product_Brief.pdf. QNN source: https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html");
}

// 9. Deployment and guardrails
{
  const s = p.slides.add(); base(s, "DEPLOYMENT & RESPONSIBILITY", "08");
  text(s, "A safety product needs honest failure behavior", 68, 106, 1080, 58, 38, C.ink, true);
  const rows = [
    ["Runs today", "One command, standard library server, offline message and thread APIs"],
    ["Private", "No raw history; exported reports exclude the source conversation"],
    ["Accessible", "Keyboard flow, high contrast, reduced motion, plain-language actions"],
    ["Deployable", "QNN adapter, INT8 model contract, CPU fallback, acceptance checks"],
    ["Bounded", "Risk indicator, not a fraud verdict; one false positive disclosed"],
  ];
  rows.forEach((r,i)=>{const y=195+i*84;text(s,String(i+1).padStart(2,"0"),72,y+6,55,26,14,C.lime,true);box(s,138,y,1,55,C.line);text(s,r[0],172,y,210,32,21,C.ink,true);text(s,r[1],420,y+2,730,36,18,C.muted);box(s,70,y+65,1120,1,C.line);});
  box(s, 70, 630, 470, 35, C.lime, C.lime, 6); text(s, "python app.py  →  localhost:8765", 86, 638, 435, 20, 14, C.bg, true, { fontFamily: "Courier New" });
}

// 10. Close
{
  const s = p.slides.add(); s.background.fill = C.lime;
  text(s, "RAKSHAK EDGE", 70, 50, 260, 26, 13, C.bg, true, { letterSpacing: 1.8 });
  text(s, "A safer pause\nbefore the tap", 66, 130, 850, 170, 66, C.bg, true, { lineSpacing: .92 });
  text(s, "Conversation-aware protection that stays on the PC", 72, 345, 930, 52, 26, "#315512", false);
  box(s, 72, 473, 550, 96, "#07130F", "#07130F", 14); text(s, "LIVE DEMO", 96, 491, 110, 22, 11, C.lime, true, { letterSpacing: 1.4 }); text(s, "python app.py", 96, 526, 440, 28, 22, C.ink, true, { fontFamily: "Courier New" });
  text(s, "Working demo, locked evaluation, privacy threat model, Snapdragon profile", 72, 646, 850, 24, 14, "#315512", true);
  text(s, "Hariharan C", 1030, 646, 180, 24, 14, C.bg, true, { textAlign: "right" });
}

const stagingDir = path.join(workspaceDir, ".codex-finalizer");
await fs.mkdir(stagingDir, { recursive: true });
const candidatePath = path.join(stagingDir, "candidate.pptx");
await (await PresentationFile.exportPptx(p)).save(candidatePath);
await finalizePresentation({
  explicitTotalSlideCount: 10,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  workspaceDir,
  candidatePath,
  finalPath: FINAL_PPTX,
  pythonExecutable: RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  fontPolicy: { basis: "design", families: [family, "Courier New"] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, "Rakshak_Edge_Pitch_Final.validation.json"),
});
console.log(FINAL_PPTX);
