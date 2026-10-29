# Architecture Notes

## Components
1. Streamlit UI (`app.py`): receives inquiry text and displays results.
2. Analysis module (`src/copilot.py`): extracts simple fields, maps service category, checks missing details, and creates a draft.
3. Synthetic examples (`data/sample_inquiries.json`): demonstrates four service categories without using customer data.
4. Unit tests (`tests/test_copilot.py`): checks key expected behaviors.

## Data flow
Input text -> input validation -> feature/technology keyword extraction -> timeline/budget parsing -> service mapping -> missing-field checks -> response draft -> human review/export.

## Trust boundaries
The prototype runs locally and has no external AI API integration. It does not persist inquiries. A production implementation would need a privacy review, authentication, approved model/data processing, access control, monitoring, and human approval.
