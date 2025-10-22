import unittest
from app import app


class UserBlueprintTests(unittest.TestCase):

    def setUp(self):
        """Налаштування, яке виконується перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_route_works(self):
        response = self.client.get("/users/hi/Maria?age=25")

        self.assertEqual(response.status_code, 200)

        self.assertIn(b"MARIA", response.data)
        self.assertIn(b"25", response.data)

    def test_admin_redirect_shows_correct_content(self):
        """Тест для /users/admin, що перевіряє правильний редірект."""
        response = self.client.get("/users/admin", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)


        self.assertIn(b"age is unknown", response.data)