"""Transparent risk signals used by the deterministic safety layer."""

URGENCY = {
    "expires today", "act now", "immediately", "within 24 hours", "last chance",
    "account blocked", "account suspended", "final warning", "urgent", "jaldi",
    "abhi", "turant", "இப்போது", "உடனே",
}

SECRETS = {
    "otp", "one time password", "pin", "cvv", "password", "screen share",
    "remote access", "anydesk", "teamviewer", "verification code", "security code",
}

PAYMENT = {
    "upi", "pay now", "transfer", "refund fee", "processing fee", "deposit",
    "gift card", "gift cards", "voucher", "vouchers", "crypto", "wallet", "collect request", "scan qr", "₹",
    "payment", "cashback", "prize", "lottery", "kyc fee",
}

IMPERSONATION = {
    "bank officer", "police", "customs", "income tax", "rbi", "courier",
    "hr department", "ceo", "manager", "support team", "electricity board",
    "aadhaar", "pan card", "kyc", "digital arrest",
}

PRESSURE = {
    "do not tell", "keep this confidential", "stay on the call", "don't disconnect",
    "avoid arrest", "legal action", "penalty", "fine", "reward", "guaranteed return",
    "limited slots", "secret",
}

SAFE_CONTEXT = {
    "never share otp", "do not share otp", "official warning", "fraud awareness",
    "security training", "sample scam", "report suspicious",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "cutt.ly", "rb.gy", "is.gd",
    "rebrand.ly", "shorturl.at",
}

HIGH_RISK_TLDS = {"zip", "mov", "click", "top", "xyz", "support", "rest", "cam", "loan"}

BRAND_DOMAINS = {
    "sbi": {"sbi.co.in", "onlinesbi.sbi"},
    "hdfc": {"hdfcbank.com"},
    "icici": {"icicibank.com"},
    "axis": {"axisbank.com"},
    "amazon": {"amazon.in", "amazon.com"},
    "flipkart": {"flipkart.com"},
    "microsoft": {"microsoft.com", "live.com"},
    "google": {"google.com"},
    "paytm": {"paytm.com"},
}
