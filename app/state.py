from typing import Dict, List, Any


sessions: Dict[str, Dict[str, Any]] = {}


def create_session(session_id: str):
    sessions[session_id] = {
        "messages": [],
        "patient_name": None,
        "specialty": None,
        "doctor_id": None,
        "date": None,
        "time": None,
        "appointment_id": None,
        "tool_trace": []
    }

    return sessions[session_id]


def get_session(session_id: str):

    if session_id not in sessions:
        create_session(session_id)

    return sessions[session_id]


def add_message(
    session_id: str,
    role: str,
    content: str
):

    session = get_session(session_id)

    session["messages"].append(
        {
            "role": role,
            "content": content
        }
    )


def add_tool_trace(
    session_id: str,
    tool_name: str,
    arguments: dict,
    result: dict
):

    session = get_session(session_id)

    session["tool_trace"].append(
        {
            "tool": tool_name,
            "arguments": arguments,
            "result": result
        }
    )
