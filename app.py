import uuid

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config.settings import settings
from graph.graph_builder import compiled_guarded_graph
from services.memory_service import mem0_service
from services.redis_service import redis_service

console = Console()


def print_banner():

    console.clear()

    console.print(

        Panel.fit(

            f"[bold cyan]{settings.PROJECT_NAME}[/bold cyan]\n"
            f"[green]Conversational Life Insurance Underwriter[/green]\n"
            f"[dim]Presidio • Mem0 • MCP • Guardrails • LangSmith[/dim]",

            border_style="cyan"
        )
    )


def run_underwriting_workflow(
    query: str,
    customer_name: str,
    customer_id: str,
    thread_id: str
):

    cached_payload = redis_service.get_cached_solution(
        query,
        customer_id
    )

    if cached_payload:

        console.print(
            "\n[green]⚡ Cache Hit[/green]"
        )

        return cached_payload, True

    console.print(
        "\n[blue]🧠 Loading Customer Memory...[/blue]"
    )

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

        "customer_profile": {},

        "financial_profile": {},

        "medical_profile": {},

        "family_profile": {},

        "retrieved_docs": [],

        "bmi_result": {},

        "hlv_result": {},

        "premium_quote": {},

        "ulip_illustration": {},

        "risk_score": 0,

        "risk_category": "",

        "solution": "",

        "underwriting_recommendation": "",

        "confidence_score": 0,

        "guardrail_passed": True,

        "guardrail_violation_reason": "",

        "retry_count": 0,

        "human_approved": False,

        "human_feedback": "",

        "visited_nodes": ["START"],

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

            "session_id": thread_id,

            "customer_id": customer_id,

            "project_version":
                settings.VERSION
        }
    }

    console.print(
        f"\n[green]Thread:[/green] {thread_id}\n"
    )

    for event in compiled_guarded_graph.stream(
        initial_state,
        config=config
    ):

        for node_name, _ in event.items():

            console.print(
                f" ➜ {node_name}"
            )

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
            final_state.get("sanitized_query", query),
            customer_id,
            final_state
        )

    if final_state.get(
        "guardrail_passed",
        True
    ):

        mem0_service.add_customer_memory(
            customer_id,
            final_state.get("sanitized_query", query)
        )

    return final_state, False


def render_summary(
    final_state,
    is_cached,
    thread_id
):

    table = Table(
        title="Insurance Underwriting Summary"
    )

    table.add_column(
        "Property",
        style="cyan"
    )

    table.add_column(
        "Value",
        style="green"
    )

    table.add_row(
        "Session",
        thread_id
    )

    table.add_row(
        "Customer",
        final_state.get(
            "customer_name",
            "N/A"
        )
    )

    table.add_row(
        "Risk Category",
        str(
            final_state.get(
                "risk_category",
                "Pending"
            )
        )
    )

    table.add_row(
        "Execution",
        "Redis Cache"
        if is_cached
        else "LangGraph"
    )

    table.add_row(
        "LangSmith",
        settings.LANGCHAIN_PROJECT
    )

    table.add_row(
        "Path",
        " -> ".join(
            final_state.get(
                "visited_nodes",
                []
            )
        )
    )

    console.print("\n")
    console.print(table)

    console.print(
        "\n[bold cyan]Final Recommendation[/bold cyan]"
    )

    console.print(

        Panel(

            final_state.get(
                "solution",
                "No recommendation generated."
            ),

            border_style="green"
        )
    )


def main():

    print_banner()

    customer_name = Prompt.ask(
        "Customer Name",
        default="John Smith"
    )

    customer_id = Prompt.ask(
        "Customer ID",
        default="CUST001"
    )

    query = Prompt.ask(

        "Customer Query",

        default=(
            "I am 34 years old, "
            "earn 18 lakh annually and "
            "want 2.5 crore term insurance. "
            "I occasionally smoke."
        )
    )

    thread_id = str(
        uuid.uuid4()
    )[:8]

    try:

        final_state, is_cached = (
            run_underwriting_workflow(
                query,
                customer_name,
                customer_id,
                thread_id
            )
        )

        render_summary(
            final_state,
            is_cached,
            thread_id
        )

    finally:

        if hasattr(
            mem0_service,
            "close"
        ):
            mem0_service.close()


if __name__ == "__main__":
    main()