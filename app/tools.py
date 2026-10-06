from datetime import datetime
from uuid import uuid4

from app.database import (
    get_doctors,
    get_available_slots,
    add_appointment,
    get_appointments
)


def search_doctors(specialty: str):
    """
    Search doctors by specialty.
    """

    specialty = specialty.strip().lower()

    results = [
        doctor
        for doctor in get_doctors()
        if doctor["specialty"].lower() == specialty
    ]

    return {
        "success": True,
        "doctors": results
    }


def check_availability(doctor_id: str, date: str):
    """
    Check available appointment slots for a doctor.
    """

    slots = get_available_slots(doctor_id, date)

    return {
        "success": True,
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": slots
    }


def book_appointment(
    patient_name: str,
    doctor_id: str,
    date: str,
    time: str
):
    """
    Book an appointment if the requested slot is available.
    """

    slots = get_available_slots(doctor_id, date)

    if time not in slots:
        return {
            "success": False,
            "error": "Requested time is not available."
        }

    # Check for double booking
    for appointment in get_appointments():

        if (
            appointment["doctor_id"] == doctor_id
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return {
                "success": False,
                "error": "This appointment slot is already booked."
            }

    appointment_id = f"APT-{uuid4().hex[:8].upper()}"

    appointment = {
        "appointment_id": appointment_id,
        "patient_name": patient_name,
        "doctor_id": doctor_id,
        "date": date,
        "time": time,
        "status": "confirmed"
    }

    add_appointment(appointment)

    return {
        "success": True,
        "appointment": appointment
    }


def cancel_appointment(appointment_id: str):
    """
    Cancel an existing appointment.
    """

    for appointment in get_appointments():

        if appointment["appointment_id"] == appointment_id:

            appointment["status"] = "cancelled"

            return {
                "success": True,
                "appointment": appointment
            }

    return {
        "success": False,
        "error": "Appointment not found."
    }
