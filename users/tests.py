from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase


class RegistrationTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_registration_page_uses_vue_and_bootstrap(self):
        response = self.client.get("/accounts/register/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your account")
        self.assertContains(response, "bootstrap@5.3.8")
        self.assertContains(response, "vue@3.5.42")

    def test_auth_markup_uses_csp_compatible_vue_hooks(self):
        response = self.client.get("/accounts/register/")

        self.assertContains(response, "data-auth-app")
        self.assertContains(response, 'data-password-input="password"')
        self.assertNotContains(response, "v-model=")
        self.assertNotContains(response, "@click=")

    def test_valid_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "new-user",
                "email": "new-user@example.com",
                "password1": "A-safe-passphrase-923!",
                "password2": "A-safe-passphrase-923!",
            },
        )

        self.assertRedirects(response, "/")
        user = get_user_model().objects.get(username="new-user")
        self.assertEqual(user.email, "new-user@example.com")
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(
            username="existing-user",
            email="first@example.com",
            password="A-safe-passphrase-923!",
        )

        response = self.client.post(
            "/accounts/register/",
            {
                "username": "existing-user",
                "email": "second@example.com",
                "password1": "Another-safe-passphrase-721!",
                "password2": "Another-safe-passphrase-721!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_username_length_matches_the_displayed_guidance(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "ab",
                "email": "short-name@example.com",
                "password1": "A-safe-passphrase-923!",
                "password2": "A-safe-passphrase-923!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at least 3 characters")
        self.assertFalse(get_user_model().objects.filter(username="ab").exists())

    def test_registration_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            "/accounts/register/",
            {
                "username": "new-user",
                "email": "new-user@example.com",
                "password1": "A-safe-passphrase-923!",
                "password2": "A-safe-passphrase-923!",
            },
        )

        self.assertEqual(response.status_code, 403)


class AuthenticationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(
            username="old-user",
            email="old-user@example.com",
            password="A-safe-passphrase-923!",
        )

    def test_anonymous_home_redirects_to_login(self):
        response = self.client.get("/")

        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_user_can_login_view_home_and_logout_with_post(self):
        login_response = self.client.post(
            "/accounts/login/",
            {"username": "old-user", "password": "A-safe-passphrase-923!"},
        )

        self.assertRedirects(login_response, "/")
        home_response = self.client.get("/")
        self.assertContains(home_response, "old-user")
        self.assertEqual(self.client.get("/accounts/logout/").status_code, 405)

        logout_response = self.client.post("/accounts/logout/")

        self.assertRedirects(logout_response, "/accounts/login/")
        self.assertRedirects(self.client.get("/"), "/accounts/login/?next=/")

    def test_login_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        response = csrf_client.post(
            "/accounts/login/",
            {"username": "old-user", "password": "A-safe-passphrase-923!"},
        )

        self.assertEqual(response.status_code, 403)

    def test_login_is_rate_limited_after_five_failures(self):
        credentials = {"username": "old-user", "password": "wrong-password"}

        for _ in range(4):
            response = self.client.post(
                "/accounts/login/", credentials, REMOTE_ADDR="203.0.113.10"
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/accounts/login/", credentials, REMOTE_ADDR="203.0.113.10"
        )
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, "Too many sign-in attempts", status_code=429)

    def test_login_rate_limit_is_scoped_by_client_and_username(self):
        credentials = {"username": "old-user", "password": "wrong-password"}
        for _ in range(5):
            self.client.post(
                "/accounts/login/", credentials, REMOTE_ADDR="203.0.113.10"
            )

        response = self.client.post(
            "/accounts/login/",
            {"username": "old-user", "password": "A-safe-passphrase-923!"},
            REMOTE_ADDR="203.0.113.11",
        )

        self.assertRedirects(response, "/")

    def test_auth_pages_send_content_security_policy(self):
        response = self.client.get("/accounts/login/")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
