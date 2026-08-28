import os
import sys
import uuid
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from graph.graph_builder import compiled_guarded_graph

os.environ["CI_AUTOMATION"] = "true"

with open(
    "evals/insurance_eval_dataset.json",
    "r",
    encoding="utf-8"
) as f:

    test_cases = json.load(f)

for case in test_cases:

    state = {
        "customer_id": "EVAL001",
        "customer_name": "LangSmith Evaluation",
        "raw_query": case["query"],
        "sanitized_query": "",
        "customer_memory": [],
        "customer_profile": {},
        "financial_profile": {},
        "medical_profile": {},
        "family_profile": {},
        "visited_nodes": ["START"],
        "execution_logs": []
    }

    try:

        print(
            f"\nRunning Evaluation: "
            f"{case['query']}"
        )
            
        config = {
            "configurable": {
                "thread_id": str(uuid.uuid4())[:8]
            }
        }

        print(
            f"Thread ID: "
            f"{config['configurable']['thread_id']}"
        )

        compiled_guarded_graph.invoke(
            state,
            config=config
        )

        print(
            f"PASSED: "
            f"{case['query']}"
        )

    except Exception as e:

        raise RuntimeError(
            f"FAILED: "
            f"{case['query']} "
            f"{e!s}"
        )