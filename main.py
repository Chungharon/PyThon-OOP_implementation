# Hospital Managment System - Object-Oriented Pogramming Implementation.
# This System Manages Patients, Doctors, Health and Appointments.

import datetime
from typing import List, Dict, Optional
import json

class Person:
    # Base class for all people in the Hospital system

    def __init__(self, person_id: str, name: str, email: str, phone: str):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone
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
        if not value.strip():
            raise valueError("Invalid Email")
        self._email = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value
    
    def get_info(self) -> Dict:
        # Return person information as dictionary
        return {
            "id": self.person_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    
    
    