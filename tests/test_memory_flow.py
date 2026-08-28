from unittest.mock import Mock

from services.memory_service import (
    Mem0Service
)


def test_memory_add_and_retrieve():

    service = Mem0Service()

    service.memory = Mock()

    service.memory.get_all.return_value = [
        {
            "memory":
            "Customer smokes occasionally"
        }
    ]

    memories = (
        service.get_customer_memories(
            "CUST001"
        )
    )

    assert len(memories) == 1

    assert (
        memories[0]
        == "Customer smokes occasionally"
    )