# Mock clinic database

doctors = [
    {
        "id": "D001",
        "name": "Dr. Smith",
        "specialty": "Dermatology"
    },
    {
        "id": "D002",
        "name": "Dr. Priya",
        "specialty": "Cardiology"
    },
    {
        "id": "D003",
        "name": "Dr. Kumar",
        "specialty": "General Medicine"
    }
]


available_slots = {
    ("D001", "2026-10-07"): [
        "10:00",
        "11:30",
        "15:00"
    ],
    ("D002", "2026-10-07"): [
        "09:30",
        "14:00"
    ],
    ("D003", "2026-10-07"): [
        "10:30",
        "16:00"
    ]
}


appointments = []


def get_doctors():
    return doctors


def get_available_slots(doctor_id, date):
    return available_slots.get((doctor_id, date), [])


def add_appointment(appointment):
    appointments.append(appointment)


def get_appointments():
    return appointments
