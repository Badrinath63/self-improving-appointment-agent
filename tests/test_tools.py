from app.tools import (
    search_doctors,
    check_availability,
    book_appointment,
    cancel_appointment
)


def test_search_doctors():

    result = search_doctors("Dermatology")

    assert result["success"] is True
    assert len(result["doctors"]) == 1
    assert result["doctors"][0]["id"] == "D001"


def test_check_availability():

    result = check_availability(
        "D001",
        "2026-10-07"
    )

    assert result["success"] is True
    assert "10:00" in result["available_slots"]


def test_book_appointment():

    result = book_appointment(
        patient_name="Badrinath",
        doctor_id="D001",
        date="2026-10-07",
        time="10:00"
    )

    assert result["success"] is True
    assert result["appointment"]["status"] == "confirmed"


def test_unavailable_slot():

    result = book_appointment(
        patient_name="Test Patient",
        doctor_id="D001",
        date="2026-10-07",
        time="12:00"
    )

    assert result["success"] is False


def test_cancel_appointment():

    booking = book_appointment(
        patient_name="Test Patient",
        doctor_id="D003",
        date="2026-10-07",
        time="10:30"
    )

    appointment_id = booking["appointment"]["appointment_id"]

    result = cancel_appointment(appointment_id)

    assert result["success"] is True
    assert result["appointment"]["status"] == "cancelled"

