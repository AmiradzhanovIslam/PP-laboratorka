from typing import Protocol
import unittest


class EligibilityRule(Protocol):
    """Общий контракт правила проверки пререквизитов."""

    def check(self, student: dict, course: dict) -> tuple[bool, str]:
        """Возвращает решение и причину результата."""
        ...


class CreditsRule:
    """Проверяет минимальное количество набранных кредитов."""

    def __init__(self, required: int = 30):
        self.required = required

    def check(self, student: dict, course: dict) -> tuple[bool, str]:
        credits = student.get("credits", 0)
        if credits >= self.required:
            return True, "достаточно кредитов"
        return False, f"недостаточно кредитов: {credits}/{self.required}"


class CourseRule:
    """Проверяет наличие обязательного пройденного курса."""

    def __init__(self, prerequisite: str):
        self.prerequisite = prerequisite

    def check(self, student: dict, course: dict) -> tuple[bool, str]:
        completed = student.get("completed_courses", [])
        if self.prerequisite in completed:
            return True, f"курс «{self.prerequisite}» пройден"
        return False, f"не пройден курс «{self.prerequisite}»"


class GpaRule:
    """Проверяет минимальный средний балл студента."""

    def __init__(self, minimum: float = 2.5):
        self.minimum = minimum

    def check(self, student: dict, course: dict) -> tuple[bool, str]:
        gpa = student.get("gpa", 0.0)
        if gpa >= self.minimum:
            return True, f"GPA {gpa:.2f} соответствует минимуму"
        return False, f"GPA {gpa:.2f} ниже минимума {self.minimum:.2f}"


class EnrollmentService:
    """Сервис проверки допуска к дисциплине через взаимозаменяемые правила."""

    def __init__(self, rules: list[EligibilityRule]):
        if not rules:
            raise ValueError("Необходимо передать хотя бы одно правило")
        self._rules = list(rules)

    def check(self, student: dict, course: dict) -> dict:
        reasons = []
        for rule in self._rules:
            allowed, reason = rule.check(student, course)
            if not allowed:
                reasons.append(reason)

        return {
            "allowed": not reasons,
            "reasons": reasons if reasons else ["все требования выполнены"],
        }


class MemoryRule:
    """Тестовый дублёр правила, сохраняющий вызовы в памяти."""

    def __init__(self, allowed: bool = True, reason: str = "тестовое правило"):
        self.allowed = allowed
        self.reason = reason
        self.calls = []

    def check(self, student: dict, course: dict) -> tuple[bool, str]:
        self.calls.append((student, course))
        return self.allowed, self.reason


class EnrollmentServiceTests(unittest.TestCase):
    def setUp(self):
        self.student_ok = {
            "id": 1,
            "name": "Алина",
            "credits": 45,
            "gpa": 3.2,
            "completed_courses": ["Математика", "Программирование"],
        }
        self.course = {
            "name": "Алгоритмы",
            "prerequisite": "Программирование",
        }

    def test_all_rules_pass(self):
        service = EnrollmentService([
            CreditsRule(30),
            CourseRule("Программирование"),
            GpaRule(2.5),
        ])
        result = service.check(self.student_ok, self.course)
        self.assertTrue(result["allowed"])
        self.assertEqual(result["reasons"], ["все требования выполнены"])

    def test_credits_rule_rejects_student(self):
        student = dict(self.student_ok, credits=20)
        service = EnrollmentService([
            CreditsRule(30),
            CourseRule("Программирование"),
            GpaRule(2.5),
        ])
        result = service.check(student, self.course)
        self.assertFalse(result["allowed"])
        self.assertIn("недостаточно кредитов", result["reasons"][0])

    def test_course_rule_rejects_student(self):
        student = dict(self.student_ok, completed_courses=["Математика"])
        service = EnrollmentService([
            CreditsRule(30),
            CourseRule("Программирование"),
            GpaRule(2.5),
        ])
        result = service.check(student, self.course)
        self.assertFalse(result["allowed"])
        self.assertIn("не пройден курс", result["reasons"][0])

    def test_gpa_rule_rejects_student(self):
        student = dict(self.student_ok, gpa=2.1)
        service = EnrollmentService([
            CreditsRule(30),
            CourseRule("Программирование"),
            GpaRule(2.5),
        ])
        result = service.check(student, self.course)
        self.assertFalse(result["allowed"])
        self.assertIn("GPA", result["reasons"][0])

    def test_multiple_failures_are_returned(self):
        student = dict(
            self.student_ok,
            credits=10,
            gpa=1.8,
            completed_courses=[]
        )
        service = EnrollmentService([
            CreditsRule(30),
            CourseRule("Программирование"),
            GpaRule(2.5),
        ])
        result = service.check(student, self.course)
        self.assertFalse(result["allowed"])
        self.assertEqual(len(result["reasons"]), 3)

    def test_rules_are_replaceable_without_changing_service(self):
        memory_rule = MemoryRule(True, "заменяемый компонент")
        service = EnrollmentService([memory_rule])
        result = service.check(self.student_ok, self.course)

        self.assertTrue(result["allowed"])
        self.assertEqual(result["reasons"], ["все требования выполнены"])
        self.assertEqual(len(memory_rule.calls), 1)

    def test_empty_rules_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "хотя бы одно правило"):
            EnrollmentService([])


def demo():
    student = {
        "id": 101,
        "name": "Амина",
        "credits": 42,
        "gpa": 3.4,
        "completed_courses": ["Программирование", "Математика"],
    }
    course = {
        "name": "Алгоритмы",
        "prerequisite": "Программирование",
    }

    service = EnrollmentService([
        CreditsRule(30),
        CourseRule("Программирование"),
        GpaRule(2.5),
    ])

    print("Обычная проверка:")
    print(service.check(student, course))

    memory_rule = MemoryRule(True, "допуск подтвержден тестовым правилом")
    replaceable_service = EnrollmentService([memory_rule])

    print("\nПроверка заменяемым компонентом:")
    print(replaceable_service.check(student, course))
    print("Количество вызовов MemoryRule:", len(memory_rule.calls))


if __name__ == "__main__":
    demo()
    print("\nРезультаты тестов:")
    unittest.main()
