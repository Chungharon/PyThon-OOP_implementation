# Hospital Managment System - Object-Oriented Pogramming Implementation.
# This System Manages Patients, Doctors, Health and Appointments.

import datetime
from typing import List, Dict, Optional
import json
from enum import Enum

class BloodType(Enum):
    """Blood Type class"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"



class AppointmentStatus(Enum):
    """Appointment Status enumeration"""
    SCHEDULED = "Scheduled"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"


class RoomType(Enum):
    """Room Type enumeration"""
    ICU = "ICU"
    PRIVATE = "Private"
    GENERAL = "General"
    EMERGENCY = "Emergency"
    

class Person:
    # Base class for all people in the Hospital system

    def __init__(self, person_id: str, name: str, email: str, phone: str, date_of_birth: datetime):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
        self._date_of_birth = date_of_birth
        self._created_at = datetime.now()

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise valueError("Please type in your name")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def name(self, value: str):
        if "@" not in value.strip():
            raise valueError("Invalid Email Format")
        self._email = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    def get_age(self) -> int:
        """Calculate age fromdate of birth"""
        today = datetime.now()
        return today.year - self._date_of_birth.year - (
            (today.month, today.day) < (self._date_of_birth.month, self._date_of_birth.day)
        )
    
    def get_info(self) -> Dict:
        """Return person information as dictionary"""
        return {
            "id": self.person_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self._date_of_birth.strftime("%Y-%m-%d"),
            "age": self.get_age(),
            "created_at": self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(ID: {self.person_id}, Name: {self.name})"

class Patient(Person):
    # Patient class for the Hospital Management System
    def __init__(self, person_id: str, name: str, email: str, phone: str, date_of_birth: datetime, BloodType: BloodType):
        super().__init__(person_id, name, email, phone, date_of_birth)
        self._blood_type = BloodType
        self._medical_history: List[str] = []
        self._allergies: List[str] = []
        self._room: Optional[int] = None
        self._admission_date: Optional[datetime] = None
        self._discharge_date: Optional[datetime] = None
        self._appointments: List['Appointment'] = []
        self._assigned_doctor: Optional['Doctor'] = None
        self._is_admitted: bool = False
        self._vital_signs: Dict[str, Dict] = {} # {timestamp: {"temperature": float, "heart_rate": int, "blood_pressure": str, "oxygen_level": int}}

    @property
    def BloodType(self) -> BloodType:
        return self._blood_type


    @property
    def _is_admitted(self) -> bool:
        return self._is_admitted
    
    @property
    def add_allergy(self, allergy: str):
        """Add an allergy to the patient"""
        if allergy not in self._allergies:
            self._allergies.append(allergy)
            print(f"{self._name} has been added to {allergy}")
        else:
            print(f"{self._name} is already in {allergy}")
        return self._allergies

    def add_medical_history(self, history: str):
        """Add medical history entry"""
        self._medical_history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {history}")
        print(f"{self._name} has been added to {history}")
        return self._medical_history

    def assign_doctor(self, doctor: 'Doctor'):
        """Assign a doctor to the patient"""
        self._assigned_doctor = doctor
        print(f"Dr. {doctor.name} has been assigned to {self._name}")
        return self._assigned_doctor
    
    def Schedule_appointment(self, appointment: 'Appointment') -> bool:
        """Schedule an appointment for the patient"""
        if appointment not in self._appointments:
            self._appointments.append(appointment)
            return True
        return False

    def admit_to_hospital(self, room: "Room"):
        """Admit Patient to hospital"""
        if not self._is_admitted:
            self._room = room
            self._admission_date = datetime.now()
            self._is_admitted = True
            room.occupy(self)
            print(f"{self._name} admitted to {room.room_type.value} - Room {room.room_number}")
        else:
            print(f"{self._name} is already admitted")
            return self._is_admitted
    def discharge(self):
        """Discharge the patient from the hospital"""
        if self._is_admitted and self._room:
            self._room.vacate()
            print(f"{self._name} discharged from Room {self._room.room_number}")
            self._room = None
            self._admission_date = None
            self._is_admitted = False
        else:
            print(f"{self._name} is not currently admitted")
            return self._is_admitted
        

    def update_vital_signs(self, blood_pressure: str, temperature: float, heart_rate: int, pulse: int):
        """Update patient vital signs"""
        timestamp = datetime.now().strftime("%Y-m-%d %H:%M:%S")
        self._vital_signs[timestamp] = {
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "heart_rate": heart_rate,
            "pulse": pulse
        }
        return self._vital_signs

    def get_vital_signs(self) -> Dict[str, Dict]:
        """Get patient vital signs"""
        return self._vital_signs

    def get_appointments(self) -> List['Appointment']:
        """Get list of appointments"""
        return self._appointments.copy()
    
    def get_info(self) -> Dict:
        """Return patient information"""
        info = super().get_info()
        info.update({
            "blood_type": self._blood_type.value,
            "allergies": self._allergies,
            "assigned_doctor": self._assigned_doctor if self._assigned_doctor else "Not assigned",
            "is_admitted": self._is_admitted,
            "room": f"{self._room.room_type.value} - {self._room.room_number}" if self._room else "N/A",
            "total_appointments": len(self._appointments)
        })
        return info


class Doctor(Person):
    """Doctor class for the Hospital Management System"""
    
    def __init__(self, person_id: str, name: str, email: str, phone: str, 
                 date_of_birth: datetime, specialization: str, license_number: str):
        super().__init__(person_id, name, email, phone, date_of_birth)
        self._specialization = specialization
        self._license_number = license_number
        self._hire_date = datetime.now()
        self._patients: List[Patient] = []
        self._appointments: List['Appointment'] = []
        self._department: Optional['MedicalDepartment'] = None
        self._salary = 0.0
    
    @property
    def specialization(self) -> str:
        return self._specialization
    
    @property
    def license_number(self) -> str:
        return self._license_number
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, value: float):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
    
    def add_patient(self, patient: Patient):
        """Add a patient to doctor's list"""
        if patient not in self._patients:
            self._patients.append(patient)
    
    def remove_patient(self, patient: Patient):
        """Remove a patient from doctor's list"""
        if patient in self._patients:
            self._patients.remove(patient)
    
    def schedule_appointment(self, appointment: 'Appointment'):
        """Schedule an appointment"""
        if appointment not in self._appointments:
            self._appointments.append(appointment)
    
    def get_today_appointments(self) -> List['Appointment']:
        """Get today's appointments"""
        today = datetime.now().date()
        return [apt for apt in self._appointments 
                if apt.appointment_date.date() == today 
                and apt.status == AppointmentStatus.SCHEDULED]
    
    def prescribe_medication(self, patient: Patient, prescription: 'Prescription'):
        """Prescribe medication to a patient"""
        print(f"Dr. {self._name} prescribed medication to {patient.name}")
        return prescription
    
    def write_diagnosis(self, patient: Patient, diagnosis: str):
        """Write diagnosis for a patient"""
        patient.add_medical_history(f"Diagnosis: {diagnosis}")
        print(f"Diagnosis written for {patient.name}: {diagnosis}")
    
    def get_patients(self) -> List[Patient]:
        """Get list of patients"""
        return self._patients.copy()
    
    def get_info(self) -> Dict:
        """Return doctor information"""
        info = super().get_info()
        info.update({
            "specialization": self._specialization,
            "license_number": self._license_number,
            "hire_date": self._hire_date.strftime("%Y-%m-%d"),
            "total_patients": len(self._patients),
            "salary": self._salary,
            "department": self._department.name if self._department else "Not assigned"
        })
        return info