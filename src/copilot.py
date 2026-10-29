"""Core logic for the Cynbit AI Project Inquiry Intelligence Copilot PoC.

This implementation is intentionally API-independent. It uses transparent rules and
keyword matching so the demo runs without a paid model API or private company data.
"""

import re
from typing import Dict, List


SERVICE_RULES = {
    "AI Automation": [
        "ai chatbot", "chatbot", "llm", "ai agent", "virtual assistant",
        "automate", "automation", "generative ai", "customer questions"
    ],
    "Custom Software Development": [
        "website", "web app", "application", "mobile app", "admin panel",
        "software", "platform", "dashboard", "api", "contact form"
    ],
    "Cloud and DevOps": [
        "aws", "azure", "cloud", "migration", "deploy", "deployment",
        "infrastructure", "ci/cd", "reliability", "kubernetes", "docker"
    ],
    "Digital Marketing": [
        "seo", "marketing", "campaign", "advertising", "social media",
        "lead generation", "analytics", "search ranking"
    ],
}

FEATURE_KEYWORDS = [
    "chatbot", "dashboard", "admin panel", "contact form", "mobile app",
    "website", "api integration", "payment integration", "product catalog",
    "faq", "analytics", "authentication", "cloud migration", "automated deployment",
    "customer support", "reporting"
]

TECH_KEYWORDS = [
    "python", "postgresql", "mysql", "mongodb", "aws", "azure", "docker",
    "kubernetes", "react", "node.js", "shopify", "wordpress", "stripe"
]

MISSING_QUESTIONS = {
    "goal": "What business outcome should the project achieve, and how will success be measured?",
    "budget": "What budget range has been approved for the project?",
    "timeline": "What is the target launch date, and are there any fixed milestones?",
    "users": "Who are the intended users, and approximately how many users or requests are expected?",
    "integrations": "Which existing systems, data sources, or third-party services must be integrated?",
    "acceptance": "What are the key acceptance criteria or must-have features for the first release?",
}


def _find_budget(text: str) -> str:
    patterns = [
        r'(?i)(?:budget|cost|spend|around|approximately)\s*(?:of\s*)?(?:is\s*)?(?:₹|rs\.?|inr|\$)?\s*[\d,]+(?:\.\d+)?\s*(?:k|thousand|lakh|lakhs|million)?',
        r'(?i)(?:₹|rs\.?|inr|\$)\s*[\d,]+(?:\.\d+)?\s*(?:k|thousand|lakh|lakhs|million)?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return re.sub(r"\s+", " ", match.group(0)).strip()
    return ""


def _find_timeline(text: str) -> str:
    patterns = [
        r'(?i)\b(?:within|in|by|over the next)\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a|an)\s*(?:business\s*)?(?:days?|weeks?|months?)\b',
        r'(?i)\b(?:next month|this month|as soon as possible|urgent|flexible timeline)\b',
        r'(?i)\b(?:launch|deadline|delivery)\s+(?:by|on)\s+[\w ,/-]+\b',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return re.sub(r"\s+", " ", match.group(0)).strip()
    return ""


def _extract_features(text: str) -> List[str]:
    lower = text.lower()
    return [feature for feature in FEATURE_KEYWORDS if feature in lower]


def _extract_technologies(text: str) -> List[str]:
    lower = text.lower()
    return [tech for tech in TECH_KEYWORDS if tech in lower]


def _service_category(text: str):
    lower = text.lower()
    scores = {
        category: sum(1 for keyword in keywords if keyword in lower)
        for category, keywords in SERVICE_RULES.items()
    }
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return (
            "Needs Human Review",
            "The inquiry does not contain enough matching keywords for a reliable service suggestion."
        )
    rationale = (
        f"Matched {scores[best]} keyword(s) associated with {best.lower()}. "
        "This is a rule-based suggestion and should be confirmed by a team member."
    )
    return best, rationale


def _project_goal(text: str, features: List[str]) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    # Keep a concise, readable summary rather than claiming semantic understanding.
    if len(clean) <= 220:
        return clean
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0]
    return sentence[:220].rstrip() + ("..." if len(sentence) > 220 else "")


def analyze_inquiry(text: str) -> Dict:
    """Analyze an inquiry and return a validated, transparent structured result."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Inquiry text must not be empty.")

    clean = text.strip()
    features = _extract_features(clean)
    technologies = _extract_technologies(clean)
    budget = _find_budget(clean)
    timeline = _find_timeline(clean)
    category, rationale = _service_category(clean)

    lower = clean.lower()
    missing_fields = []
    if len(clean.split()) < 8:
        missing_fields.append("Provide more detail about the business goal and requested outcome.")
    if not budget:
        missing_fields.append("Budget range")
    if not timeline:
        missing_fields.append("Target timeline")
    if not any(term in lower for term in ["user", "customer", "team", "staff", "visitor", "shopper"]):
        missing_fields.append("Target users or expected usage")
    if not any(term in lower for term in ["integrat", "existing", "database", "data source", "api", "platform"]):
        missing_fields.append("Required integrations or data sources")
    if not any(term in lower for term in ["success", "measure", "acceptance", "must-have", "requirement"]):
        missing_fields.append("Success criteria or acceptance requirements")

    follow_up_questions = []
    if "Budget range" in missing_fields:
        follow_up_questions.append(MISSING_QUESTIONS["budget"])
    if "Target timeline" in missing_fields:
        follow_up_questions.append(MISSING_QUESTIONS["timeline"])
    if "Target users or expected usage" in missing_fields:
        follow_up_questions.append(MISSING_QUESTIONS["users"])
    if "Required integrations or data sources" in missing_fields:
        follow_up_questions.append(MISSING_QUESTIONS["integrations"])
    if "Success criteria or acceptance requirements" in missing_fields:
        follow_up_questions.append(MISSING_QUESTIONS["acceptance"])
    if not follow_up_questions:
        follow_up_questions.append("Are there any constraints or requirements not included in the inquiry?")

    goal = _project_goal(clean, features)
    draft_response = (
        "Subject: Follow-up on your project inquiry\n\n"
        "Hello,\n\n"
        "Thank you for sharing your project requirements. We understand that your request is: "
        f"{goal}\n\n"
        "To help prepare a suitable initial scope, could you please clarify the following?\n"
        + "\n".join(f"- {question}" for question in follow_up_questions)
        + "\n\nOnce these details are confirmed, our team can review the requirements and discuss suitable next steps.\n\n"
        "Best regards,\nCynbit Team"
    )

    checks = [
        "Input is non-empty.",
        "Budget and timeline are marked as missing when no matching text is detected.",
        "Service category is based on explicit keyword rules.",
        "The response is a draft and is not sent automatically.",
    ]
    limitations = [
        "Keyword matching may miss synonyms or misunderstand context.",
        "A detected budget or timeline is not guaranteed to be normalized correctly.",
        "No trained ML model or LLM is used in this baseline implementation.",
        "Generated responses are drafts only and are not sent automatically.",
        "Use synthetic examples for the assessment; do not enter confidential customer data.",
    ]

    return {
        "project_goal": goal,
        "features": features,
        "timeline": timeline,
        "budget": budget,
        "technologies": technologies,
        "service_category": category,
        "service_rationale": rationale,
        "missing_fields": missing_fields,
        "follow_up_questions": follow_up_questions,
        "draft_response": draft_response,
        "validation_checks": checks,
        "limitations": limitations,
    }
