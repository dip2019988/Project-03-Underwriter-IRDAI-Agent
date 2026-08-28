from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from graph.router import evaluate_confidence_route, route_by_intent
from graph.state import UnderwritingState
from nodes.auth_node import auth_analysis_node
from nodes.classify_node import classify_intent_node
from nodes.confidence_node import confidence_check_node

# Import Nodes
from nodes.guardrail_node import input_guardrail_node, output_guardrail_node
from nodes.human_node import human_approval_node
from nodes.kb_node import fallback_kb_node
from nodes.knowledge_node import knowledge_answer_node
from nodes.mcp_node import mcp_execution_node
from nodes.medical_followup_node import medical_followup_node
from nodes.profile_extraction_node import profile_extraction_node
from nodes.risk_assessment_node import risk_assessment_node
from nodes.solution_node import generate_solution_node


def route_guardrail_check(
    state: UnderwritingState
) -> str:
    """
    Routes to profile extraction if
    guardrail validation succeeds.
    """

    if state.get(
        "guardrail_passed",
        True
    ):
        return "profile_extraction_node"

    return "END"


def build_guarded_mcp_graph(
    checkpointer=None
) -> StateGraph:
    """
    Constructs StateGraph wrapped
    with Security Guardrail Nodes.
    """

    workflow = StateGraph(
        UnderwritingState
    )

    # --------------------------------------------------
    # Register Nodes
    # --------------------------------------------------

    workflow.add_node(
        "input_guardrail_node",
        input_guardrail_node
    )

    workflow.add_node(
        "profile_extraction_node",
        profile_extraction_node
    )

    workflow.add_node(
        "classify_node",
        classify_intent_node
    )

    workflow.add_node(
        "auth_node",
        auth_analysis_node
    )

    workflow.add_node(
        "mcp_execution_node",
        mcp_execution_node
    )

    workflow.add_node(
        "kb_node",
        fallback_kb_node
    )

    workflow.add_node(
        "knowledge_node",
        knowledge_answer_node
    )

    workflow.add_node(
        "solution_node",
        generate_solution_node
    )

    workflow.add_node(
        "confidence_node",
        confidence_check_node
    )

    workflow.add_node(
        "human_approval_node",
        human_approval_node
    )

    workflow.add_node(
        "output_guardrail_node",
        output_guardrail_node
    )

    workflow.add_node(
        "risk_assessment_node",
        risk_assessment_node
    )

    workflow.add_node(
        "medical_followup_node",
        medical_followup_node
    )

    # --------------------------------------------------
    # Entry Point
    # --------------------------------------------------

    workflow.set_entry_point(
        "input_guardrail_node"
    )

    # --------------------------------------------------
    # Guardrail Routing
    # --------------------------------------------------

    workflow.add_conditional_edges(
        "input_guardrail_node",
        route_guardrail_check,
        {
            "profile_extraction_node":
                "profile_extraction_node",

            "END":
                END,
        }
    )

    # --------------------------------------------------
    # Profile Extraction
    # --------------------------------------------------

    workflow.add_edge(
        "profile_extraction_node",
        "risk_assessment_node"
    )

    workflow.add_edge(
        "risk_assessment_node",
        "medical_followup_node"
    )

    workflow.add_edge(
        "medical_followup_node",
        "classify_node"
    )


    # --------------------------------------------------
    # Intent Routing
    # --------------------------------------------------

    workflow.add_conditional_edges(
        "classify_node",
        route_by_intent,
        {
            "mcp_node":
                "mcp_execution_node",

            "kb_node":
                "kb_node",

            "underwriting_node":
                "auth_node",
        }
    )

    # --------------------------------------------------
    # Knowledge Flow
    # --------------------------------------------------

    workflow.add_edge(
        "kb_node",
        "knowledge_node"
    )

    workflow.add_edge(
        "knowledge_node",
        "output_guardrail_node"
    )

    # --------------------------------------------------
    # Underwriting Flow
    # --------------------------------------------------

    workflow.add_edge(
        "auth_node",
        "solution_node"
    )

    workflow.add_edge(
        "mcp_execution_node",
        "solution_node"
    )

    workflow.add_edge(
        "solution_node",
        "confidence_node"
    )

    workflow.add_conditional_edges(
        "confidence_node",
        evaluate_confidence_route,
        {
            "END":
                "output_guardrail_node",

            "solution_node":
                "solution_node",

            "human_approval_node":
                "human_approval_node",
        }
    )

    workflow.add_conditional_edges(
        "human_approval_node",
        lambda state:
            (
                "output_guardrail_node"
                if state.get(
                    "human_approved"
                )
                else "solution_node"
            ),
        {
            "output_guardrail_node":
                "output_guardrail_node",

            "solution_node":
                "solution_node"
        }
    )

    # --------------------------------------------------
    # Final Output
    # --------------------------------------------------

    workflow.add_edge(
        "output_guardrail_node",
        END
    )

    memory_saver = (
        checkpointer
        if checkpointer is not None
        else MemorySaver()
    )

    return workflow.compile(
        checkpointer=memory_saver
    )


compiled_guarded_graph = (
    build_guarded_mcp_graph()
)