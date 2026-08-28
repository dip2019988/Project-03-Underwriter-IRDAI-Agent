from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.lib.styles import getSampleStyleSheet

import uuid

import streamlit as st

from config.settings import settings
from graph.graph_builder import compiled_guarded_graph

from services.redis_service import redis_service
from services.memory_service import mem0_service


st.set_page_config(
    page_title="Insurance Underwriter Agent",
    page_icon="🛡️",
    layout="wide"
)

if "history" not in st.session_state:

    st.session_state.history = []

# --------------------------------------------------
# Workflow Wrapper
# --------------------------------------------------


def run_underwriting_workflow(
    query: str,
    customer_name: str,
    customer_id: str,
    thread_id: str
):

    cached_payload = (
        redis_service.get_cached_solution(
            query,
            customer_id
        )
    )

    if cached_payload:
        return cached_payload, True

    customer_memory = (
        mem0_service.get_customer_memories(
            customer_id
        )
    )

    initial_state = {

        "customer_id":
            customer_id,

        "customer_name":
            customer_name,

        "raw_query":
            query,

        "sanitized_query":
            "",

        "customer_memory":
            customer_memory,

        "customer_profile":
            {},

        "financial_profile":
            {},

        "medical_profile":
            {},

        "family_profile":
            {},

        "retrieved_docs":
            [],

        "bmi_result":
            {},

        "hlv_result":
            {},

        "premium_quote":
            {},

        "risk_score":
            0,

        "risk_category":
            "",

        "solution":
            "",

        "underwriting_recommendation":
            "",

        "confidence_score":
            0,

        "guardrail_passed":
            True,

        "guardrail_violation_reason":
            "",

        "retry_count":
            0,

        "human_approved":
            False,

        "human_feedback":
            "",

        "visited_nodes": [
            "START"
        ],

        "execution_logs": [
            f"Session started for {customer_id}"
        ]
    }

    config = {

        "configurable": {
            "thread_id": thread_id
        },

        "tags": [
            f"customer:{customer_id}",
            "insurance",
            "underwriting"
        ],

        "metadata": {

            "session_id":
                thread_id,

            "customer_id":
                customer_id,

            "project_version":
                settings.VERSION
        }
    }

    for _ in compiled_guarded_graph.stream(
        initial_state,
        config=config
    ):
        pass

    final_state = (
        compiled_guarded_graph
        .get_state(config)
        .values
    )

    if (
        final_state.get(
            "guardrail_passed",
            True
        )
        and
        final_state.get(
            "confidence_score",
            0
        )
        >= settings.CONFIDENCE_THRESHOLD
    ):

        redis_service.set_cached_solution(
            query,
            customer_id,
            final_state
        )

    if final_state.get(
        "guardrail_passed",
        True
    ):

        mem0_service.add_customer_memory(
            customer_id,
            query
        )

    return final_state, False

def generate_pdf_report(
    final_state
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    elements.append(
        Paragraph(
            "Insurance Underwriting Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            f"Customer: "
            f"{final_state.get('customer_name', 'N/A')}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Risk Category: "
            f"{final_state.get('risk_category', 'N/A')}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Confidence Score: "
            f"{final_state.get('confidence_score', 0)}%",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    elements.append(
        Paragraph(
            "Recommendation",
            styles["Heading2"]
        )
    )

    solution_text = (
        final_state.get(
            "solution",
            ""
        )
        .replace(
            "\n",
            "<br/>"
        )
    )

    elements.append(
        Paragraph(
            solution_text,
            styles["BodyText"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# --------------------------------------------------
# Sidebar
# --------------------------------------------------


with st.sidebar:

    st.title("🛡️ Insurance AI")

    st.success("✅ Presidio Enabled")
    st.success("✅ Guardrails Active")
    st.success("✅ Mem0 Connected")
    st.success("✅ MCP Services")
    st.success("✅ LangGraph")

    st.markdown("---")

    st.caption(
        f"Version: {settings.VERSION}"
    )

    st.markdown("---")

    st.subheader(
        "🕘 History"
    )

    if st.session_state.history:

        for item in reversed(
            st.session_state.history[-10:]
        ):

            st.caption(
                item["query"][:50]
            )

            st.write(
                item["risk_category"]
            )

            st.markdown("---")

    else:

        st.info(
            "No history yet."
        )
        
# --------------------------------------------------
# Header
# --------------------------------------------------


st.title(
    "🛡️ Conversational Life Insurance Underwriter"
)

st.caption(
    "IRDAI • MCP • Mem0 • Presidio • LangGraph"
)


# --------------------------------------------------
# Input Form
# --------------------------------------------------


with st.form("insurance_form"):

    col1, col2 = st.columns(2)

    with col1:

        customer_name = st.text_input(
            "Customer Name",
            value="John Smith"
        )

    with col2:

        customer_id = st.text_input(
            "Customer ID",
            value="CUST001"
        )

    query = st.text_area(
        "Insurance Query",
        value=(
            "I am 34 years old, "
            "earn 18 lakh annually "
            "and want 2.5 crore "
            "term insurance. "
            "I occasionally smoke."
        ),
        height=150
    )

    submitted = st.form_submit_button(
        "🔍 Analyze Underwriting Request",
        use_container_width=True
    )


# --------------------------------------------------
# Process Request
# --------------------------------------------------


if submitted:

    thread_id = str(
        uuid.uuid4()
    )[:8]

    with st.spinner(
        "Running underwriting workflow..."
    ):

        final_state, is_cached = (
            run_underwriting_workflow(
                query=query,
                customer_name=customer_name,
                customer_id=customer_id,
                thread_id=thread_id
            )
        )

    st.success(
        "Workflow completed successfully."
    )

    st.session_state.history.append(
        {
            "query":
                query,

            "intent":
                final_state.get(
                    "intent",
                    "N/A"
                ),

            "risk_category":
                final_state.get(
                    "risk_category",
                    "N/A"
                )
        }
    )

    st.divider()

    # --------------------------------------------------
    # Phase 1 & 2
    # KPI Dashboard
    # --------------------------------------------------

    risk_category = final_state.get(
        "risk_category",
        "N/A"
    )

    confidence = final_state.get(
        "confidence_score",
        0
    )

    intent = final_state.get(
        "intent",
        "N/A"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Risk Category",
        risk_category
    )

    col2.metric(
        "Confidence",
        f"{confidence}%"
    )

    col3.metric(
        "Intent",
        intent
    )

    col4.metric(
        "Execution",
        (
            "Redis Cache"
            if is_cached
            else "LangGraph"
        )
    )

    st.divider()

    # --------------------------------------------------
    # Phase 3
    # Knowledge vs Underwriting
    # --------------------------------------------------

    is_knowledge_query = (
        risk_category
        == "KNOWLEDGE_QUERY"
    )

    if is_knowledge_query:

        tab1, tab2 = st.tabs(
            [
                "Knowledge Answer",
                "Execution"
            ]
        )

        with tab1:

            st.subheader(
                "Knowledge Response"
            )

            st.markdown(
                final_state.get(
                    "solution",
                    "No response available."
                )
            )

        with tab2:

            st.subheader(
                "Execution Path"
            )

            st.code(
                " → ".join(
                    final_state.get(
                        "visited_nodes",
                        []
                    )
                )
            )

            with st.expander(
                "Debug State"
            ):
                st.json(
                    final_state
                )

    else:

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Recommendation",
                "MCP Results",
                "Execution",
                "Debug"
            ]
        )

        # ----------------------------------
        # Recommendation
        # ----------------------------------

        with tab1:

            st.subheader(
                "Underwriting Recommendation"
            )

            st.markdown(
                final_state.get(
                    "solution",
                    "No recommendation generated."
                )
            )

        # ----------------------------------
        # MCP Results
        # ----------------------------------

        with tab2:

            bmi_col, hlv_col, premium_col = (
                st.columns(3)
            )

            with bmi_col:

                st.markdown(
                    "### BMI"
                )

                bmi_result = (
                    final_state.get(
                        "bmi_result",
                        {}
                    )
                )

                if bmi_result:
                    st.json(
                        bmi_result
                    )
                else:
                    st.info(
                        "No BMI result."
                    )

            with hlv_col:

                st.markdown(
                    "### HLV"
                )

                hlv_result = (
                    final_state.get(
                        "hlv_result",
                        {}
                    )
                )

                if hlv_result:
                    st.json(
                        hlv_result
                    )
                else:
                    st.info(
                        "No HLV result."
                    )

            with premium_col:

                st.markdown(
                    "### Premium"
                )

                premium_result = (
                    final_state.get(
                        "premium_quote",
                        {}
                    )
                )

                if premium_result:
                    st.json(
                        premium_result
                    )
                else:
                    st.info(
                        "No premium quote."
                    )

        # ----------------------------------
        # Execution
        # ----------------------------------

        with tab3:

            st.subheader(
                "Execution Path"
            )

            st.code(
                " → ".join(
                    final_state.get(
                        "visited_nodes",
                        []
                    )
                )
            )

            st.subheader(
                "Execution Logs"
            )

            for log in final_state.get(
                "execution_logs",
                []
            ):
                st.write(
                    f"• {log}"
                )

        # ----------------------------------
        # Debug
        # ----------------------------------

        with tab4:

            st.json(
                final_state
            )

    st.divider()

    # --------------------------------------------------
    # Phase 5
    # Download Report
    # --------------------------------------------------

    pdf_buffer = (
        generate_pdf_report(
            final_state
        )
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_buffer,
        file_name=(
            f"underwriting_"
            f"{thread_id}.pdf"
        ),
        mime="application/pdf"
    )