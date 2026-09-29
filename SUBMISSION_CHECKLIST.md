# Final submission checklist

## Upload fields

- **Project title:** Rakshak Edge: A Private On-Device Social-Engineering Firewall for Snapdragon PCs
- **Brief Project Description:** `submission/Rakshak_Edge_Brief_Final.pdf`
- **GitHub Repository Link:** push this folder to a public repository, then paste its URL
- **Short Pitch Presentation in PDF:** `submission/Rakshak_Edge_Pitch_Final.pdf`
- **Short Pitch Presentation in PPT:** `submission/Rakshak_Edge_Pitch_Final.pptx`

## Before pressing Submit

- Open the public GitHub link in a signed-out browser and confirm the README and source are visible.
- Download each uploaded file from the form and confirm it opens.
- Run `python -m unittest discover -s tests -v` and confirm all checks pass.
- Run `python benchmarks/evaluate_model.py` to reproduce the fixed-holdout result.
- Run `python benchmarks/evaluate_system.py` to reproduce the 45-case product result and disclosed error.
- Run `python benchmarks/run_benchmark.py` to reproduce local latency measurements.
- Run `python app.py`, open `http://127.0.0.1:8765`, and test both the Boss request and Conversation intelligence demonstrations.
- Confirm the title and description match `docs/SUBMISSION_COPY.md`.
- Answer the Snapdragon laptop ownership question truthfully. The published eligibility text says the participant should own a Snapdragon-powered laptop and the form includes a confirmation.
- Double-check every field. The competition text says a submitted entry cannot be changed after proper submission.

## Recommended 90-second judging flow

Follow `docs/DEMO_SCRIPT.md`. Keep the live app open before presenting and lead with Conversation intelligence. It is the clearest product innovation and makes the local AI story memorable.
