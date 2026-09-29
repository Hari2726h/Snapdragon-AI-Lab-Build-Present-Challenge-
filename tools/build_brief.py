from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "Rakshak_Edge_Brief_Final.pdf"
OUT.parent.mkdir(exist_ok=True)

BG = colors.HexColor("#07130F")
INK = colors.HexColor("#11231B")
MUTED = colors.HexColor("#5E7067")
LIME = colors.HexColor("#94E83F")
PALE = colors.HexColor("#EAF6EC")
LINE = colors.HexColor("#B8CABF")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverKicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=LIME, spaceAfter=10, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=35, leading=38, textColor=colors.white, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontName="Helvetica", fontSize=15, leading=22, textColor=colors.HexColor("#C7D8CF"), alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=INK, spaceBefore=3, spaceAfter=11))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=INK, spaceBefore=12, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=15.2, textColor=MUTED, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.3, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=13, leading=18, textColor=INK, leftIndent=5*mm, rightIndent=5*mm, spaceBefore=5, spaceAfter=5))


def header_footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.line(18*mm, 282*mm, 192*mm, 282*mm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(INK)
        canvas.drawString(18*mm, 286*mm, "RAKSHAK EDGE")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(192*mm, 12*mm, f"{doc.page - 1}")
    canvas.restoreState()


doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=21*mm, bottomMargin=18*mm, title="Rakshak Edge Project Brief", author="Hariharan C")
story = []

cover = Table([[Paragraph("SNAPDRAGON AI LAB BUILD &amp; PRESENT CHALLENGE", styles["CoverKicker"])], [Paragraph("Rakshak Edge", styles["CoverTitle"])], [Paragraph("A private, on-device social-engineering firewall for Snapdragon-powered PCs", styles["CoverSub"])], [Spacer(1, 35*mm)], [Paragraph("PAUSE THE SCAM BEFORE THE TAP", styles["CoverKicker"])], [Paragraph("Hariharan C  |  September 2026", styles["CoverSub"])]], colWidths=[174*mm], rowHeights=[18*mm, 38*mm, 32*mm, 42*mm, 16*mm, 20*mm])
cover.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), BG), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 12*mm), ("RIGHTPADDING", (0,0), (-1,-1), 12*mm), ("BOX", (0,0), (-1,-1), 0, BG)]))
story += [cover, PageBreak()]

story += [Paragraph("Executive summary", styles["H1x"]), Paragraph("Rakshak Edge analyzes suspicious messages and entire conversation threads before a user acts. A trained local classifier catches linkless social engineering, while a new conversation engine detects how a scam progresses from identity setup to isolation and extraction. Every result explains the evidence and recommends a safer verification path. The complete build works fully offline with no account, telemetry, cloud upload, or stored message history.", styles["Bodyx"])]

callout = Table([[Paragraph("The product protects the decision point: the few seconds before a person clicks a link, shares an OTP, or approves a payment.", styles["Callout"])]], colWidths=[174*mm])
callout.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALE), ("BOX", (0,0), (-1,-1), 1, LIME), ("LEFTPADDING", (0,0), (-1,-1), 5*mm), ("RIGHTPADDING", (0,0), (-1,-1), 5*mm), ("TOPPADDING", (0,0), (-1,-1), 5*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 5*mm)]))
story += [callout, Spacer(1, 4*mm)]

story += [Paragraph("Problem", styles["H2x"]), Paragraph("Social-engineering scams exploit context, urgency, and trusted identities. A link scanner alone misses scams such as digital-arrest calls or requests from a compromised contact. A cloud-only checker introduces another privacy decision because the user must upload the very message, account detail, or payment request they distrust.", styles["Bodyx"]), Paragraph("Solution", styles["H2x"]), Paragraph("Rakshak Edge accepts copied text from SMS, email, WhatsApp, a URL, or a QR decoder. It extracts security-relevant entities, scores visible manipulation patterns, and produces an evidence-first report. High-risk results begin with a clear stop action and direct the user to an independently trusted contact path.", styles["Bodyx"])]

criteria = [
    ["Evaluation area", "Evidence in this submission"],
    ["Technical implementation", "Working message and thread APIs, trained semantic classifier, transparent corpus, attack-chain engine, rules, tests, locked evaluation, and QNN adapter"],
    ["Use case and innovation", "Conversation-level scam progression for linkless impersonation, multilingual Indian payment signals, and explainable intervention"],
    ["Deployment and accessibility", "Zero-dependency demo, CPU fallback, QNN production path, keyboard support, high contrast, and reduced motion"],
    ["Presentation and documentation", "Pitch deck, brief, live demo script, architecture, threat model, deployment guide, and clean repository"],
]
t = Table([[Paragraph(f"<b>{c}</b>" if r == 0 else c, styles["Small"]) for c in row] for r, row in enumerate(criteria)], colWidths=[45*mm, 129*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BG), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), .4, LINE), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 3*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm), ("TOPPADDING", (0,0), (-1,-1), 2.5*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 2.5*mm)]))
story += [Spacer(1, 2*mm), t, PageBreak(), Spacer(1, 24*mm)]

story += [Paragraph("Technical implementation", styles["H1x"]), Paragraph("The architecture uses a hybrid pipeline because security decisions need both semantic context and traceable evidence.", styles["Bodyx"])]
pipeline = [
    ["1", "Input boundary", "Loopback-only API, bounded payload, no server-side persistence"],
    ["2", "Transparent analysis", "URL structure, UPI handles, phone numbers, amounts, credential requests, authority claims, urgency, and coercion"],
    ["3", "Semantic model", "Trained word and character n-gram classifier for paraphrases and mixed language"],
    ["4", "Evidence fusion", "Calibrated score, top reasons, extracted entities, and safe actions"],
    ["5", "Conversation engine", "Per-turn timeline, progression bonus, attack-chain stages, and intervention point"],
]
pt = Table([[Paragraph(f"<b>{a}</b>", styles["Small"]), Paragraph(f"<b>{b}</b>", styles["Small"]), Paragraph(c, styles["Small"])] for a,b,c in pipeline], colWidths=[12*mm, 42*mm, 120*mm])
pt.setStyle(TableStyle([("BACKGROUND", (0,0), (0,-1), LIME), ("GRID", (0,0), (-1,-1), .4, LINE), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 3*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm), ("TOPPADDING", (0,0), (-1,-1), 3*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm)]))
story += [pt, Paragraph("Measured model and complete-system evaluation", styles["H2x"]), Paragraph("The checked-in classifier trains from 72 multilingual examples and achieves 94.44% on a fixed 18-message model holdout. A separate balanced 45-case suite evaluates the complete hybrid product without contributing to training. It scores 97.78%, with all 15 high-risk and all 15 medium-risk cases correct. The evaluator prints the one conservative false positive rather than hiding it.", styles["Bodyx"])]

metrics = [["System accuracy", "97.78%"], ["Locked suite", "45 cases"], ["Regression tests", "10 passing"], ["Default cloud calls", "0"]]
mt = Table([[Paragraph(f"<b>{a}</b><br/><font color='#5E7067'>{b}</font>", styles["Bodyx"]) for a,b in metrics]], colWidths=[43.5*mm]*4)
mt.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), PALE), ("BOX", (0,0), (-1,-1), .7, LINE), ("INNERGRID", (0,0), (-1,-1), .4, LINE), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("TOPPADDING", (0,0), (-1,-1), 5*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 5*mm), ("LEFTPADDING", (0,0), (-1,-1), 3*mm)]))
story += [mt, Paragraph("The model holdout and locked system suite serve different purposes. Both are intentionally transparent and prove reproducibility, not production-scale generalization. Target-device NPU validation remains an explicit acceptance check.", styles["Small"]), Paragraph("Snapdragon optimization", styles["H2x"]), Paragraph("The Snapdragon production profile upgrades the compact reference model to a quantized encoder through ONNX Runtime's QNN Execution Provider. Static INT8 quantization reduces memory traffic while the transparent rules, evidence fusion, and conversation logic remain on CPU. The same local API supports CPU fallback when QNN is unavailable.", styles["Bodyx"])]

story += [Paragraph("Safety and responsibility", styles["H2x"]), Paragraph("Rakshak Edge reports risk indicators and safer actions. It does not claim that a message is proven fraudulent or safe. The UI uses textContent for user-derived values, the server constrains static-file paths, and the content security policy limits scripts and connections to the local origin. The threat model documents identity verification, malware sandboxing, and network reputation as out of scope.", styles["Bodyx"]), PageBreak(), Spacer(1, 8*mm)]

story += [Paragraph("Product experience", styles["H1x"]), Paragraph("The interface supports single-message triage and conversation intelligence. Single-message results show local model confidence, visible evidence, latency, and one primary action. Conversation mode scores each turn, reconstructs the attack chain, and shows when to intervene. Privacy-safe reports exclude the pasted source content.", styles["Bodyx"])]
demo_rows = [
    ["Scenario", "Expected evidence", "Primary response"],
    ["KYC + OTP", "Credential request, false urgency, look-alike SBI domain, UPI payment", "Stop. Contact the bank through the official app or known number."],
    ["Boss request", "99.8% high-risk semantic output plus voucher-payment evidence; no URL, OTP, or UPI", "Call the finance head using the number already in your contacts."],
    ["Three-turn conversation", "Identity setup, isolation, and extraction linked into an 81/100 coordinated-scam result", "Stop before sending codes; verify through a known contact path."],
    ["Safe warning", "Security-awareness context discounts quoted risk terms", "No strong pattern found; continue to verify unexpected requests."],
]
dt = Table([[Paragraph(f"<b>{c}</b>" if r == 0 else c, styles["Small"]) for c in row] for r,row in enumerate(demo_rows)], colWidths=[32*mm, 76*mm, 66*mm], repeatRows=1)
dt.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), BG), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), .4, LINE), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 3*mm), ("RIGHTPADDING", (0,0), (-1,-1), 3*mm), ("TOPPADDING", (0,0), (-1,-1), 3*mm), ("BOTTOMPADDING", (0,0), (-1,-1), 3*mm)]))
story += [dt, Paragraph("Run and evaluate", styles["H2x"]), Paragraph("Start the product with <b>python app.py</b>, then open <b>http://127.0.0.1:8765</b>. Run the regression suite with <b>python -m unittest discover -s tests -v</b>. Reproduce the model holdout with <b>python benchmarks/evaluate_model.py</b>, the locked product suite with <b>python benchmarks/evaluate_system.py</b>, and latency with <b>python benchmarks/run_benchmark.py</b>.", styles["Bodyx"]), Paragraph("Roadmap", styles["H2x"]), Paragraph("The next milestone expands the consented multilingual corpus, calibrates confidence across scam families, adds Windows share-target integration, and validates a QNN INT8 encoder on a Snapdragon-powered HP PC. A later release can add opt-in federation that shares model updates without raw message content.", styles["Bodyx"])]

story += [Paragraph("Key references", styles["H2x"]), Paragraph("1. ONNX Runtime, Qualcomm QNN Execution Provider: https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html<br/>2. Qualcomm AI Hub: https://aihub.qualcomm.com/<br/>3. Snapdragon X Elite product brief: https://docs.qualcomm.com/bundle/publicresource/87-71417-1_REV_D_Snapdragon_X_Elite_Product_Brief.pdf", styles["Small"]), Spacer(1, 7*mm), Paragraph("Repository package", styles["H2x"]), Paragraph("The folder contains the working application, tests, benchmarks, architecture, threat model, Snapdragon deployment guide, demo script, submission copy, pitch deck, and this brief. Add the public GitHub URL to the Unstop form after pushing the repository.", styles["Bodyx"])]

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
