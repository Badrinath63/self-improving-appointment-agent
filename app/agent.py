import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from app.prompts import build_system_prompt
from app.tools import (
    search_doctors,
    check_availability,
    book_appointment,
    cancel_appointment
)
from app.state import (
    get_session,
    add_message,
    add_tool_trace
)


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = os.getenv("OPENAI_MODEL")


TOOLS = [
    {
        "type": "function",
        "name": "search_doctors",
        "description": "Search doctors by medical specialty.",
        "parameters": {
            "type": "object",
            "properties": {
                "specialty": {
                    "type": "string",
                    "description": "Medical specialty, for example Dermatology"
                }
            },
            "required": ["specialty"]
        }
    },
    {
        "type": "function",
        "name": "check_availability",
        "description": "Check available appointment slots for a doctor on a date.",
        "parameters": {
            "type": "object",
            "properties": {
                "doctor_id": {
                    "type": "string",
                    "description": "Doctor ID"
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                }
            },
            "required": ["doctor_id", "date"]
        }
    },
    {
        "type": "function",
        "name": "book_appointment",
        "description": "Book an available appointment slot.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {
                    "type": "string"
                },
                "doctor_id": {
                    "type": "string"
                },
                "date": {
                    "type": "string"
                },
                "time": {
                    "type": "string"
                }
            },
            "required": [
                "patient_name",
                "doctor_id",
                "date",
                "time"
            ]
        }
    },
    {
        "type": "function",
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment.",
        "parameters": {
            "type": "object",
            "properties": {
                "appointment_id": {
                    "type": "string"
                }
            },
            "required": ["appointment_id"]
        }
    }
]


def execute_tool(name, arguments):

    if name == "search_doctors":
        return search_doctors(**arguments)

    if name == "check_availability":
        return check_availability(**arguments)

    if name == "book_appointment":
        return book_appointment(**arguments)

    if name == "cancel_appointment":
        return cancel_appointment(**arguments)

    return {
        "success": False,
        "error": f"Unknown tool: {name}"
    }


def run_agent(session_id: str, user_message: str):

    session = get_session(session_id)

    add_message(
        session_id,
        "user",
        user_message
    )

    response = client.responses.create(
        model=MODEL,
        instructions=build_system_prompt(),
        tools=TOOLS,
        input=session["messages"]
    )

    while True:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            break

        tool_outputs = []

        for tool_call in tool_calls:

            arguments = json.loads(
                tool_call.arguments
            )

            result = execute_tool(
                tool_call.name,
                arguments
            )

            add_tool_trace(
                session_id,
                tool_call.name,
                arguments,
                result
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result)
                }
            )

        response = client.responses.create(
            model=MODEL,
            instructions=build_system_prompt(),
            tools=TOOLS,
            input=[
                *session["messages"],
                *response.output,
                *tool_outputs
            ]
        )

    final_response = response.output_text

    add_message(
        session_id,
        "assistant",
        final_response
    )

    return {
        "response": final_response,
        "tool_trace": session["tool_trace"]
    }
