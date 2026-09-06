import re
from typing import Any
from langchain.agents import AgentState
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.runtime import Runtime


@before_model(can_jump_to=["end"])
def prompt_injection_guard(
    state: AgentState,
    runtime: Runtime
) -> dict[str, Any] | None:

    messages = state.get("messages", [])

    if not messages:
        return None

    last_message = messages[-1]

    if isinstance(last_message, HumanMessage):

        content = last_message.content

        injection_patterns = [
            r"ignore previous instructions",
            r"disregard all prior directives",
            r"system prompt:",
            r"you are now in developer mode",
        ]

        for pattern in injection_patterns:

            if re.search(pattern, content, re.IGNORECASE):

                return {
                    "messages": [
                        AIMessage(
                            content="Security violation detected: "
                                    "Potential prompt injection attempt blocked."
                        )
                    ],
                    "jump_to": "end",
                }

    return None