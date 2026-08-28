import os

from rich.console import Console
from rich.prompt import Prompt

from graph.state import UnderwritingState
from utils.logger import logger

console = Console()


def human_approval_node(
    state: UnderwritingState
) -> dict:

    """
    Human Underwriter Review Node

    Triggered when confidence is below threshold.
    """

    logger.info(
        "--- [NODE] Human Underwriter Review ---"
    )

    console.print(
        "\n[bold red]⚠ LOW CONFIDENCE UNDERWRITING DECISION[/bold red]"
    )

    console.print(
        f"Confidence Score: "
        f"[yellow]{state.get('confidence_score')}%[/yellow]"
    )

    console.print(
        "\n[bold cyan]Recommendation Preview:[/bold cyan]"
    )

    console.print(
        f"[dim]{state.get('solution', '')[:500]}...[/dim]\n"
    )

    console.print(
        "\n[1] Approve Recommendation"
        "\n[2] Provide Feedback & Retry"
        "\n[3] Escalate To Senior Underwriter\n"
    )

    if os.getenv(
        "CI_AUTOMATION",
        "false"
    ).lower() == "true":

        logger.info(
            "[HUMAN REVIEW] "
            "CI automation mode enabled. "
            "Auto-approving recommendation."
        )

        return {
            "human_approved": True,

            "visited_nodes": [
                "human_approval_node"
            ],

            "execution_logs": [
                "Auto-approved by CI automation"
            ]
        }

    choice = Prompt.ask(
        "Underwriter Action",
        choices=["1", "2", "3"],
        default="1",
        show_choices=False
    )

    # ----------------------------------
    # APPROVE
    # ----------------------------------

    if choice == "1":

        return {

            "human_approved": True,

            "visited_nodes": [
                "human_approval_node"
            ],

            "execution_logs": [
                "Approved by human underwriter"
            ]
        }

    # ----------------------------------
    # FEEDBACK LOOP
    # ----------------------------------

    elif choice == "2":

        feedback = Prompt.ask(
            "Provide underwriting feedback"
        )

        return {

            "human_approved": False,

            "human_feedback": feedback,

            "visited_nodes": [
                "human_approval_node"
            ],

            "execution_logs": [
                f"Human underwriter feedback: {feedback}"
            ]
        }

    # ----------------------------------
    # ESCALATE
    # ----------------------------------

    else:

        return {

            "human_approved": True,

            "solution": (
                "ESCALATED FOR SENIOR "
                "UNDERWRITER REVIEW."
            ),

            "visited_nodes": [
                "human_approval_node"
            ],

            "execution_logs": [
                "Escalated for senior underwriting review"
            ]
        }