from evaluation.evaluator import evaluate_scenario
from evaluation.scenarios import SCENARIOS


def get_scenario(scenario_id):

    return next(
        scenario
        for scenario in SCENARIOS
        if scenario["id"] == scenario_id
    )


def test_successful_booking():

    scenario = get_scenario("S01")

    result = {
        "response": "Your appointment is confirmed.",
        "tool_trace": [
            {
                "tool": "book_appointment",
                "arguments": {},
                "result": {
                    "success": True
                }
            }
        ]
    }

    evaluation = evaluate_scenario(
        scenario,
        result
    )

    assert evaluation["score"] == 10


def test_medical_advice_is_rejected():

    scenario = get_scenario("S05")

    result = {
        "response": (
            "I cannot provide medical advice "
            "or recommend medication."
        ),
        "tool_trace": []
    }

    evaluation = evaluate_scenario(
        scenario,
        result
    )

    assert evaluation["score"] == 10


def test_prompt_injection_is_rejected():

    scenario = get_scenario("S06")

    result = {
        "response": (
            "I cannot bypass my appointment "
            "scheduling rules."
        ),
        "tool_trace": []
    }

    evaluation = evaluate_scenario(
        scenario,
        result
    )

    assert evaluation["score"] == 10
