import uuid
import time
from app.agent import run_agent
from evaluation.scenarios import SCENARIOS
from app.database import reset_database
from evaluation.evaluator import evaluate_scenario
from evaluation.improvement import apply_improvement
def run_scenario(scenario):

    # Every scenario starts with clean mock clinic state.
    reset_database()

    session_id = (
        f"eval-{scenario['id']}-{uuid.uuid4().hex[:8]}"
    )

    result = None

    for message in scenario["messages"]:

        result = run_agent(
            session_id=session_id,
            user_message=message
        )

    return result


def run_evaluation():

    results = []

    print("\n")
    print("=" * 60)
    print("INITIAL EVALUATION")
    print("=" * 60)

    for scenario in SCENARIOS:

        result = run_scenario(scenario)

        # Small delay to respect free-model rate limits.
        time.sleep(5)

        evaluation = evaluate_scenario(
            scenario,
            result
        )

        results.append(evaluation)

        print(
            f"{evaluation['scenario_id']} "
            f"{evaluation['scenario']}: "
            f"{evaluation['score']}/"
            f"{evaluation['max_score']}"
        )

        for reason in evaluation["reasons"]:
            print(f"  - {reason}")

    total_score = sum(
        result["score"]
        for result in results
    )

    max_score = sum(
        result["max_score"]
        for result in results
    )

    print("\n")
    print(
        f"Initial Score: "
        f"{total_score}/{max_score}"
    )

    failures = [
        result
        for result in results
        if result["score"] < result["max_score"]
    ]

    if not failures:

        print("\nNo failures detected.")
        print("No improvement required.")

        return

    print("\n")
    print("=" * 60)
    print("SELF-IMPROVEMENT")
    print("=" * 60)

    for failure in failures:

        improvement = apply_improvement(
            failure
        )

        if improvement:

            print(
                f"\nFailure: "
                f"{failure['scenario']}"
            )

            print(
                f"Added rule: "
                f"{improvement['id']}"
            )

            print(
                f"Rule: "
                f"{improvement['rule']}"
            )

    print("\n")
    print("=" * 60)
    print("RE-EVALUATION")
    print("=" * 60)

    after_results = []

    for scenario in SCENARIOS:
        result = run_scenario(scenario)

        # Small delay to respect free-model rate limits.
        time.sleep(5)

        evaluation = evaluate_scenario(
            scenario,
            result
        )

        after_results.append(evaluation)

        print(
            f"{evaluation['scenario_id']} "
            f"{evaluation['scenario']}: "
            f"{evaluation['score']}/"
            f"{evaluation['max_score']}"
        )

    final_score = sum(
        result["score"]
        for result in after_results
    )

    print("\n")
    print(
        f"Final Score: "
        f"{final_score}/{max_score}"
    )

    print(
        f"Improvement: "
        f"{final_score - total_score:+d}"
    )

    # --------------------------------------------------
    # Regression check
    # --------------------------------------------------

    regression = False

    for before, after in zip(
        results,
        after_results
    ):

        if after["score"] < before["score"]:

            regression = True

            print(
                f"\nREGRESSION:"
                f" {before['scenario_id']} "
                f"dropped from "
                f"{before['score']} to "
                f"{after['score']}"
            )

    if regression:

        print("\nRegression Check: FAIL")

    else:

        print(
            "\nRegression Check: PASS"
        )


if __name__ == "__main__":
    run_evaluation()
