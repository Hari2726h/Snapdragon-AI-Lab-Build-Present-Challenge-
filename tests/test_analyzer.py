import unittest

from engine.analyzer import analyze


class AnalyzerTests(unittest.TestCase):
    def test_high_risk_otp_payment(self):
        result = analyze("URGENT: KYC expires today. Share OTP and pay Rs 10 to verify at sbi-secure-login.xyz")
        self.assertEqual(result["level"], "high")
        self.assertGreaterEqual(result["score"], 70)

    def test_brand_impersonation(self):
        result = analyze("Microsoft support: install AnyDesk now from microsoft-help-secure.top")
        titles = {s["title"] for s in result["signals"]}
        self.assertIn("Possible brand impersonation", titles)
        self.assertIn("Sensitive information requested", titles)

    def test_benign_message_is_low(self):
        result = analyze("Lunch at 1 pm? I will meet you near the library.")
        self.assertEqual(result["level"], "low")
        self.assertLess(result["score"], 38)

    def test_security_warning_discount(self):
        result = analyze("Official warning: never share OTP or password. Report suspicious requests.")
        self.assertNotEqual(result["level"], "high")

    def test_upi_and_amount_extraction(self):
        result = analyze("Pay INR 4,999 now to refunddesk@upi")
        self.assertIn("refunddesk@upi", result["entities"]["upi_ids"])
        self.assertIn("4,999", result["entities"]["amounts_inr"])

    def test_semantic_model_catches_linkless_impersonation(self):
        result = analyze("Finance head here. I cannot take calls. Purchase five vouchers and send the numbers before the client meeting.")
        self.assertIn(result["level"], {"medium", "high"})
        self.assertIn(result["model"]["label"], {"medium", "high"})

    def test_model_metadata_is_exposed(self):
        result = analyze("Please review the quarterly budget before the finance meeting.")
        self.assertIn("probabilities", result["model"])


if __name__ == "__main__":
    unittest.main()
