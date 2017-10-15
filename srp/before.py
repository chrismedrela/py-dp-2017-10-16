import re
import unittest


EMAIL_PATTERN = re.compile(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$')


class Person:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 email: str):
        self.first_name = first_name 
        self.last_name = last_name
        if self.validate_email(email):
            self.email = email
        else:
            raise ValueError('Invalid email')

    def validate_email(self, email):
        return EMAIL_PATTERN.match(email) is not None


class PersonTests(unittest.TestCase):
    def test_valid_email(self):
        Person('Jan', 'Kowalski', 'jan@kowalski.pl')

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Person('Jan', 'Kowalski', 'invalid email')


if __name__ == "__main__":
    unittest.main()
