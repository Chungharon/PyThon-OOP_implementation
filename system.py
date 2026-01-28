
#School Management System - Object-Oriented Programming Implementation
#This system manages students, teachers, courses, and enrollments


from datetime import datetime
from typing import List, Dict, Optional
import json


class Person:
    """Base class for all people in the school system"""
    
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
            raise ValueError("Name cannot be empty")
        self._name = value
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str):
        self._phone = value
    
    def get_info(self) -> Dict:
        """Return person information as dictionary"""
        return {
            "id": self._person_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "created_at": self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(ID: {self._person_id}, Name: {self._name})"


class Student(Person):
    """Student class inheriting from Person"""
    
    def __init__(self, person_id: str, name: str, email: str, phone: str, 
                 grade_level: int, enrollment_date: Optional[datetime] = None):
        super().__init__(person_id, name, email, phone)
        self._grade_level = grade_level
        self._enrollment_date = enrollment_date or datetime.now()
        self._enrolled_courses: List['Course'] = []
        self._grades: Dict[str, float] = {}  # course_id: grade
    
    @property
    def grade_level(self) -> int:
        return self._grade_level
    
    @grade_level.setter
    def grade_level(self, value: int):
        if not 1 <= value <= 12:
            raise ValueError("Grade level must be between 1 and 12")
        self._grade_level = value
    
    def enroll_course(self, course: 'Course') -> bool:
        """Enroll student in a course"""
        if course in self._enrolled_courses:
            print(f"{self._name} is already enrolled in {course.name}")
            return False
        
        if course.add_student(self):
            self._enrolled_courses.append(course)
            print(f"{self._name} enrolled in {course.name}")
            return True
        return False
    
    def drop_course(self, course: 'Course') -> bool:
        """Drop a course"""
        if course not in self._enrolled_courses:
            print(f"{self._name} is not enrolled in {course.name}")
            return False
        
        course.remove_student(self)
        self._enrolled_courses.remove(course)
        if course.course_id in self._grades:
            del self._grades[course.course_id]
        print(f"{self._name} dropped {course.name}")
        return True
    
    def add_grade(self, course_id: str, grade: float):
        """Add grade for a course"""
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        self._grades[course_id] = grade
    
    def get_gpa(self) -> float:
        """Calculate GPA"""
        if not self._grades:
            return 0.0
        return sum(self._grades.values()) / len(self._grades)
    
    def get_enrolled_courses(self) -> List['Course']:
        """Get list of enrolled courses"""
        return self._enrolled_courses.copy()
    
    def get_info(self) -> Dict:
        """Return student information"""
        info = super().get_info()
        info.update({
            "grade_level": self._grade_level,
            "enrollment_date": self._enrollment_date.strftime("%Y-%m-%d"),
            "enrolled_courses": [course.name for course in self._enrolled_courses],
            "gpa": round(self.get_gpa(), 2)
        })
        return info


class Teacher(Person):
    """Teacher class inheriting from Person"""
    
    def __init__(self, person_id: str, name: str, email: str, phone: str, 
                 subject: str, hire_date: Optional[datetime] = None):
        super().__init__(person_id, name, email, phone)
        self._subject = subject
        self._hire_date = hire_date or datetime.now()
        self._courses_taught: List['Course'] = []
        self._salary = 0.0
    
    @property
    def subject(self) -> str:
        return self._subject
    
    @subject.setter
    def subject(self, value: str):
        self._subject = value
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, value: float):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
    
    def assign_course(self, course: 'Course'):
        """Assign a course to this teacher"""
        if course not in self._courses_taught:
            self._courses_taught.append(course)
            course.teacher = self
    
    def remove_course(self, course: 'Course'):
        """Remove a course from teacher's assignment"""
        if course in self._courses_taught:
            self._courses_taught.remove(course)
    
    def get_courses_taught(self) -> List['Course']:
        """Get list of courses taught"""
        return self._courses_taught.copy()
    
    def get_info(self) -> Dict:
        """Return teacher information"""
        info = super().get_info()
        info.update({
            "subject": self._subject,
            "hire_date": self._hire_date.strftime("%Y-%m-%d"),
            "courses_taught": [course.name for course in self._courses_taught],
            "salary": self._salary
        })
        return info


class Course:
    """Course class"""
    
    def __init__(self, course_id: str, name: str, description: str, 
                 credits: int, max_students: int = 30):
        self._course_id = course_id
        self._name = name
        self._description = description
        self._credits = credits
        self._max_students = max_students
        self._teacher: Optional[Teacher] = None
        self._enrolled_students: List[Student] = []
    
    @property
    def course_id(self) -> str:
        return self._course_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Course name cannot be empty")
        self._name = value
    
    @property
    def credits(self) -> int:
        return self._credits
    
    @property
    def teacher(self) -> Optional[Teacher]:
        return self._teacher
    
    @teacher.setter
    def teacher(self, value: Teacher):
        self._teacher = value
    
    def add_student(self, student: Student) -> bool:
        """Add a student to the course"""
        if len(self._enrolled_students) >= self._max_students:
            print(f"Course {self._name} is full")
            return False
        
        if student not in self._enrolled_students:
            self._enrolled_students.append(student)
            return True
        return False
    
    def remove_student(self, student: Student):
        """Remove a student from the course"""
        if student in self._enrolled_students:
            self._enrolled_students.remove(student)
    
    def get_enrolled_students(self) -> List[Student]:
        """Get list of enrolled students"""
        return self._enrolled_students.copy()
    
    def get_enrollment_count(self) -> int:
        """Get number of enrolled students"""
        return len(self._enrolled_students)
    
    def is_full(self) -> bool:
        """Check if course is full"""
        return len(self._enrolled_students) >= self._max_students
    
    def get_info(self) -> Dict:
        """Return course information"""
        return {
            "course_id": self._course_id,
            "name": self._name,
            "description": self._description,
            "credits": self._credits,
            "teacher": self._teacher.name if self._teacher else "No teacher assigned",
            "enrolled_students": len(self._enrolled_students),
            "max_students": self._max_students,
            "is_full": self.is_full()
        }
    
    def __str__(self) -> str:
        return f"Course(ID: {self._course_id}, Name: {self._name}, Students: {len(self._enrolled_students)}/{self._max_students})"


class Department:
    """Department class to manage courses and teachers"""
    
    def __init__(self, dept_id: str, name: str, head: Optional[Teacher] = None):
        self._dept_id = dept_id
        self._name = name
        self._head = head
        self._courses: List[Course] = []
        self._teachers: List[Teacher] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def head(self) -> Optional[Teacher]:
        return self._head
    
    @head.setter
    def head(self, value: Teacher):
        self._head = value
    
    def add_course(self, course: Course):
        """Add a course to the department"""
        if course not in self._courses:
            self._courses.append(course)
    
    def remove_course(self, course: Course):
        """Remove a course from the department"""
        if course in self._courses:
            self._courses.remove(course)
    
    def add_teacher(self, teacher: Teacher):
        """Add a teacher to the department"""
        if teacher not in self._teachers:
            self._teachers.append(teacher)
    
    def remove_teacher(self, teacher: Teacher):
        """Remove a teacher from the department"""
        if teacher in self._teachers:
            self._teachers.remove(teacher)
    
    def get_info(self) -> Dict:
        """Return department information"""
        return {
            "dept_id": self._dept_id,
            "name": self._name,
            "head": self._head.name if self._head else "No head assigned",
            "total_courses": len(self._courses),
            "total_teachers": len(self._teachers)
        }


class School:
    """Main School class that manages the entire system"""
    
    def __init__(self, name: str, address: str):
        self._name = name
        self._address = address
        self._students: Dict[str, Student] = {}
        self._teachers: Dict[str, Teacher] = {}
        self._courses: Dict[str, Course] = {}
        self._departments: Dict[str, Department] = {}
    
    def add_student(self, student: Student) -> bool:
        """Add a student to the school"""
        if student.person_id in self._students:
            print(f"Student with ID {student.person_id} already exists")
            return False
        self._students[student.person_id] = student
        print(f"Student {student.name} added successfully")
        return True
    
    def add_teacher(self, teacher: Teacher) -> bool:
        """Add a teacher to the school"""
        if teacher.person_id in self._teachers:
            print(f"Teacher with ID {teacher.person_id} already exists")
            return False
        self._teachers[teacher.person_id] = teacher
        print(f"Teacher {teacher.name} added successfully")
        return True
    
    def add_course(self, course: Course) -> bool:
        """Add a course to the school"""
        if course.course_id in self._courses:
            print(f"Course with ID {course.course_id} already exists")
            return False
        self._courses[course.course_id] = course
        print(f"Course {course.name} added successfully")
        return True
    
    def add_department(self, department: Department) -> bool:
        """Add a department to the school"""
        if department._dept_id in self._departments:
            print(f"Department already exists")
            return False
        self._departments[department._dept_id] = department
        print(f"Department {department.name} added successfully")
        return True
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """Get student by ID"""
        return self._students.get(student_id)
    
    def get_teacher(self, teacher_id: str) -> Optional[Teacher]:
        """Get teacher by ID"""
        return self._teachers.get(teacher_id)
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        return self._courses.get(course_id)
    
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        return list(self._students.values())
    
    def get_all_teachers(self) -> List[Teacher]:
        """Get all teachers"""
        return list(self._teachers.values())
    
    def get_all_courses(self) -> List[Course]:
        """Get all courses"""
        return list(self._courses.values())
    
    def generate_report(self) -> str:
        """Generate a comprehensive school report"""
        report = f"\n{'='*60}\n"
        report += f"School Report: {self._name}\n"
        report += f"{'='*60}\n\n"
        report += f"Total Students: {len(self._students)}\n"
        report += f"Total Teachers: {len(self._teachers)}\n"
        report += f"Total Courses: {len(self._courses)}\n"
        report += f"Total Departments: {len(self._departments)}\n"
        report += f"\n{'='*60}\n"
        return report
    
    def __str__(self) -> str:
        return f"School(Name: {self._name}, Students: {len(self._students)}, Teachers: {len(self._teachers)})"


# Demo/Example Usage
def main():
    """Demonstrate the School Management System"""
    
    print("\n" + "="*60)
    print("SCHOOL MANAGEMENT SYSTEM - DEMONSTRATION")
    print("="*60 + "\n")
    
    # Create school
    school = School("Springfield High School", "123 Main St, Springfield")
    print(f"Created: {school}\n")
    
    # Create departments
    math_dept = Department("DEPT001", "Mathematics")
    science_dept = Department("DEPT002", "Science")
    school.add_department(math_dept)
    school.add_department(science_dept)
    print()
    
    # Create teachers
    teacher1 = Teacher("T001", "Dr. John Smith", "john.smith@school.com", "555-0101", "Mathematics")
    teacher1.salary = 60000
    teacher2 = Teacher("T002", "Prof. Sarah Johnson", "sarah.j@school.com", "555-0102", "Physics")
    teacher2.salary = 65000
    
    school.add_teacher(teacher1)
    school.add_teacher(teacher2)
    print()
    
    # Add teachers to departments
    math_dept.add_teacher(teacher1)
    math_dept.head = teacher1
    science_dept.add_teacher(teacher2)
    
    # Create courses
    course1 = Course("C001", "Algebra I", "Introduction to Algebra", 3, 25)
    course2 = Course("C002", "Physics 101", "Basic Physics Principles", 4, 20)
    course3 = Course("C003", "Calculus", "Advanced Mathematics", 4, 15)
    
    school.add_course(course1)
    school.add_course(course2)
    school.add_course(course3)
    print()
    
    # Assign courses to teachers
    teacher1.assign_course(course1)
    teacher1.assign_course(course3)
    teacher2.assign_course(course2)
    
    # Add courses to departments
    math_dept.add_course(course1)
    math_dept.add_course(course3)
    science_dept.add_course(course2)
    
    # Create students
    student1 = Student("S001", "Alice Williams", "alice.w@student.com", "555-0201", 10)
    student2 = Student("S002", "Bob Brown", "bob.b@student.com", "555-0202", 11)
    student3 = Student("S003", "Carol Davis", "carol.d@student.com", "555-0203", 10)
    
    school.add_student(student1)
    school.add_student(student2)
    school.add_student(student3)
    print()
    
    # Enroll students in courses
    print("Enrolling students in courses:")
    student1.enroll_course(course1)
    student1.enroll_course(course2)
    student2.enroll_course(course1)
    student2.enroll_course(course3)
    student3.enroll_course(course2)
    student3.enroll_course(course3)
    print()
    
    # Add grades
    print("Adding grades:")
    student1.add_grade(course1.course_id, 92.5)
    student1.add_grade(course2.course_id, 88.0)
    student2.add_grade(course1.course_id, 95.0)
    student2.add_grade(course3.course_id, 90.5)
    student3.add_grade(course2.course_id, 87.5)
    student3.add_grade(course3.course_id, 93.0)
    print("Grades added successfully\n")
    
    # Display information
    print("\n" + "="*60)
    print("STUDENT INFORMATION")
    print("="*60)
    for student in school.get_all_students():
        print(f"\n{student}")
        info = student.get_info()
        print(f"  Grade Level: {info['grade_level']}")
        print(f"  GPA: {info['gpa']}")
        print(f"  Enrolled Courses: {', '.join(info['enrolled_courses'])}")
    
    print("\n" + "="*60)
    print("TEACHER INFORMATION")
    print("="*60)
    for teacher in school.get_all_teachers():
        print(f"\n{teacher}")
        info = teacher.get_info()
        print(f"  Subject: {info['subject']}")
        print(f"  Salary: ${info['salary']:,.2f}")
        print(f"  Courses Taught: {', '.join(info['courses_taught'])}")
    
    print("\n" + "="*60)
    print("COURSE INFORMATION")
    print("="*60)
    for course in school.get_all_courses():
        print(f"\n{course}")
        info = course.get_info()
        print(f"  Credits: {info['credits']}")
        print(f"  Teacher: {info['teacher']}")
        print(f"  Enrollment: {info['enrolled_students']}/{info['max_students']}")
    
    # Generate school report
    print(school.generate_report())
    
    # Test dropping a course
    print("Testing course drop:")
    student1.drop_course(course2)
    print(f"Updated enrolled courses: {', '.join([c.name for c in student1.get_enrolled_courses()])}\n")


if __name__ == "__main__":
    main()
        