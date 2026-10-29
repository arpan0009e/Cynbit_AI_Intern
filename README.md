# Cynbit AI Project Inquiry Intelligence Copilot

**Assessment:** AI/ML Engineer Intern  
**Candidate:** Arpan Mondal  
**Project type:** Proof of Concept (PoC)

## 1. Purpose

This prototype helps turn a free-text project inquiry into a structured first-pass brief. It:
- extracts simple project details using transparent keyword rules;
- suggests a service category;
- flags potentially missing information;
- generates follow-up questions;
- drafts a response for human review; and
- allows the output to be downloaded as JSON.

## 2. Important scope and limitations

This is an **API-independent baseline PoC**, not a production AI system. It uses rule-based keyword matching and regular expressions, not a trained ML model or LLM. This makes it easy to run and inspect, but it can miss context, synonyms, and unusual wording. Service recommendations and extracted fields must be reviewed by a person.

All examples in `data/sample_inquiries.json` are synthetic. The project is not connected to Cynbit's systems and does not use real customer records. Do not enter confidential information.

## 3. Requirements

- Python 3.10 or newer
- Internet access to install Streamlit the first time
- A web browser

## 4. Run locally

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, commonly `http://localhost:8501`.

## 5. Run tests

```bash
python -m unittest discover -s tests -v
```

## 6. Example workflow

1. Open the app.
2. Select a synthetic sample or enter a non-confidential inquiry.
3. Click **Analyze inquiry**.
4. Review the suggested service, extracted details, missing fields, and follow-up questions.
5. Edit the draft response as needed.
6. Download the JSON output for documentation or further testing.

## 7. Project structure

```text
cynbit-ai-project-copilot/
├── app.py
├── src/
│   ├── __init__.py
│   └── copilot.py
├── tests/
│   └── test_copilot.py
├── data/
│   └── sample_inquiries.json
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## 8. Evaluation plan

The supplied tests check empty-input handling, service-category mapping for sample cases, fallback to human review when no category is matched, and draft generation. These are functional tests, not a statistically valid model benchmark.

For a stronger evaluation:
- label a larger, diverse set of synthetic inquiries;
- compare predicted categories with expected categories;
- calculate precision, recall, and F1 by category;
- manually review field extraction and follow-up questions;
- measure processing time and the amount of editing required by reviewers;
- report failures and limitations rather than claiming unmeasured accuracy.

## 9. Proposed architecture

```text
User inquiry
    |
    v
Streamlit input and basic validation
    |
    v
Rule-based extraction and keyword matching
    |
    +--> Service category suggestion
    |
    +--> Missing-field checks and follow-up questions
    |
    v
Draft response generation
    |
    v
Results display + human review + JSON download
```

## 10. Security and responsible use

- Use synthetic examples for demonstrations.
- Do not store or transmit confidential customer information.
- Never send generated messages automatically.
- Review the original inquiry before accepting extracted fields or recommendations.
- For production, add authentication, logging controls, data-retention rules, monitoring, and security review.

## 11. Next improvements

1. Add document upload and safe text extraction.
2. Add a schema-constrained LLM provider behind a configurable interface.
3. Add source spans so users can trace extracted fields to original text.
4. Build a labeled evaluation set and report category-wise metrics.
5. Add persistence only after privacy and access requirements are defined.

## 12. Assessment deliverables

This repository is the **PoC deliverable**. Keep the AI Opportunity Report and Technical Approach Report as separate deliverables, and ensure all three use the same project name and scope.
