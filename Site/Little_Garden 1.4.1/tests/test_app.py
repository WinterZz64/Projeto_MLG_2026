"""Testes automatizados básicos para as rotas e controles de segurança."""

import os
import re
import tempfile
import unittest
from pathlib import Path

_TEMP_DIR = tempfile.TemporaryDirectory()
os.environ["APP_ENV"] = "development"
os.environ["LITTLE_GARDEN_SECRET"] = "test-secret-key-that-is-long-enough-for-tests"
os.environ["LITTLE_GARDEN_DATABASE"] = str(Path(_TEMP_DIR.name) / "test.db")

from app import app, get_db  # noqa: E402


class LittleGardenSecurityTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        with app.app_context():
            get_db().execute("DELETE FROM users")
            get_db().commit()
        self.client = app.test_client()

    def csrf_token(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        match = re.search(rb'name="_csrf_token" value="([^"]+)"', response.data)
        self.assertIsNotNone(match, f"Token CSRF não encontrado em {path}")
        return match.group(1).decode()

    def test_public_pages_and_security_headers(self):
        for path in ("/", "/sobre", "/mecanicas", "/personagens", "/ambiental"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
                self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
                self.assertIn("Content-Security-Policy", response.headers)

    def test_profile_requires_login(self):
        response = self.client.get("/perfil")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_post_without_csrf_is_rejected(self):
        response = self.client.post("/logout")
        self.assertEqual(response.status_code, 400)

    def test_registration_login_profile_and_logout(self):
        token = self.csrf_token("/cadastro")
        response = self.client.post(
            "/cadastro",
            data={
                "_csrf_token": token,
                "username": "Jardineiro",
                "email": "teste@example.com",
                "password": "uma-senha-bem-longa-123",
                "confirm_password": "uma-senha-bem-longa-123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jardineiro", response.data)
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        with app.app_context():
            stored_hash = get_db().execute(
                "SELECT password_hash FROM users WHERE email = ?",
                ("teste@example.com",),
            ).fetchone()["password_hash"]
            self.assertNotEqual(stored_hash, "uma-senha-bem-longa-123")

        logout_token = self.csrf_token("/")
        response = self.client.post("/logout", data={"_csrf_token": logout_token})
        self.assertEqual(response.status_code, 302)

        login_token = self.csrf_token("/login")
        response = self.client.post(
            "/login",
            data={
                "_csrf_token": login_token,
                "email": "TESTE@example.com",
                "password": "uma-senha-bem-longa-123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jardineiro", response.data)

    def test_duplicate_email_is_rejected(self):
        token = self.csrf_token("/cadastro")
        data = {
            "_csrf_token": token,
            "username": "Primeiro",
            "email": "duplicado@example.com",
            "password": "senha-comprida-o-suficiente",
            "confirm_password": "senha-comprida-o-suficiente",
        }
        self.client.post("/cadastro", data=data)
        token = self.csrf_token("/cadastro")
        data["_csrf_token"] = token
        data["username"] = "Segundo"
        response = self.client.post("/cadastro", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Já existe uma conta".encode(), response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
