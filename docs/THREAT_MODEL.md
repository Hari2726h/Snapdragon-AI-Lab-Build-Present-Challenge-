# Threat model

## Protected assets

- Message content and contact context
- OTPs, PINs, CVVs, passwords, and account references
- UPI handles and payment details
- The user's decision before opening a link or transferring money

## In-scope threats

- Bank, courier, employer, police, government, and support impersonation
- Urgency, secrecy, threats, rewards, and remote-access coercion
- Look-alike and encoded domains
- Hidden destinations and redirects
- Requests for credentials, payments, gift cards, or crypto
- Mixed English and common Indian payment vocabulary
- Multi-message grooming that separates identity, isolation, and payment across turns

## Out of scope

- Definitive identity verification
- Malware execution or sandboxing
- Network reputation feeds in offline mode
- Proof that a low-risk message is genuine
- Automated blocking of transactions

## Abuse resistance

- The server accepts only a bounded JSON payload.
- Static files are resolved inside the web root.
- User text is inserted with `textContent`, not HTML.
- Content Security Policy restricts scripts and connections to the local origin.
- The app does not store server-side message history.
- Conversation results contain scores and stage labels but omit the raw source messages.
- Downloaded reports intentionally exclude the analyzed source content.

## Human factors

Risk explanations name the observable evidence. The product recommends a separate trusted channel and avoids asking the user to click another link. High-risk language uses a clear stop action without claiming certainty.
