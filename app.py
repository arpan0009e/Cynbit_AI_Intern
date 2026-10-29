import streamlit as st
from src.copilot import analyze_inquiry

st.set_page_config(page_title="Cynbit AI Project Copilot", page_icon="🤖", layout="wide")

st.title("Cynbit AI Project Inquiry Intelligence Copilot")
st.caption("Assessment proof of concept | Synthetic examples only | Human review required")

with st.sidebar:
    st.header("About this PoC")
    st.write(
        "This prototype turns a project inquiry into a structured brief, identifies missing "
        "details, suggests a relevant service category, and drafts a response for review."
    )
    st.warning(
        "This is a rule-based demonstration, not a production system. It does not connect "
        "to Cynbit systems or use real customer records."
    )

examples = {
    "AI chatbot for e-commerce": (
        "We need an AI chatbot for our online store to answer common customer questions. "
        "We want to launch in four weeks and it should use our existing product catalog and FAQ."
    ),
    "Website development": (
        "Our small business needs a new responsive website with a contact form and an admin "
        "panel. We hope to launch in eight weeks. Our budget is around INR 150000."
    ),
    "Cloud migration": (
        "We want to migrate our current application to AWS and improve deployment reliability. "
        "We use a Python backend and PostgreSQL. We need a proposal next month."
    ),
    "Custom inquiry": ""
}
choice = st.selectbox("Choose a sample inquiry or enter your own", list(examples.keys()))
default_text = examples[choice]
inquiry = st.text_area(
    "Customer project inquiry",
    value=default_text,
    height=180,
    placeholder="Describe the customer's goal, requested features, budget, timeline, and constraints..."
)

if st.button("Analyze inquiry", type="primary", use_container_width=True):
    if not inquiry.strip():
        st.error("Please enter an inquiry before running the analysis.")
    else:
        result = analyze_inquiry(inquiry)
        st.session_state["last_result"] = result
        st.session_state["last_inquiry"] = inquiry

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    st.divider()
    st.subheader("Analysis results")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Suggested service category")
        st.success(result["service_category"])
        st.write(result["service_rationale"])
    with col2:
        st.markdown("#### Requirements detected")
        st.write(f"**Project goal:** {result['project_goal']}")
        st.write(f"**Features / needs:** {', '.join(result['features']) if result['features'] else 'Not clearly specified'}")
        st.write(f"**Timeline:** {result['timeline'] or 'Not provided'}")
        st.write(f"**Budget:** {result['budget'] or 'Not provided'}")
        st.write(f"**Technology / integration clues:** {', '.join(result['technologies']) if result['technologies'] else 'Not provided'}")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Missing information to clarify")
        if result["missing_fields"]:
            for item in result["missing_fields"]:
                st.write(f"- {item}")
        else:
            st.write("No required fields were flagged by the basic checks. A human review is still recommended.")
    with right:
        st.markdown("#### Follow-up questions")
        for question in result["follow_up_questions"]:
            st.write(f"- {question}")

    st.markdown("#### Draft response for human review")
    draft = st.text_area("Edit the response before use", value=result["draft_response"], height=170)
    st.caption("The draft is not sent automatically. Verify all details before sending.")
    st.download_button(
        "Download analysis as JSON",
        data=__import__("json").dumps({**result, "draft_response": draft}, indent=2),
        file_name="inquiry_analysis.json",
        mime="application/json",
        use_container_width=True,
    )

    with st.expander("Validation notes"):
        st.write("**Checks passed:**")
        for check in result["validation_checks"]:
            st.write(f"- {check}")
        st.write("**Limitations:**")
        for limitation in result["limitations"]:
            st.write(f"- {limitation}")

st.divider()
st.caption("Prototype note: service suggestions and extracted fields are heuristic. Validate outputs against the original inquiry.")
