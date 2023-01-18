from typing import Tuple

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class BaseAPITestCase(APITestCase):
    @staticmethod
    def create_user_with_token(username, email) -> Tuple[User, str]:
        user = User.objects.create_user(
            username=username, email=email, password="6FPbscNOW3vLfRyuL8e"
        )
        token = Token.objects.create(user=user)
        return user, f"Token {token.key}"

    def assert_status_codes_equal(self, received: int, expected: int):
        self.assertEqual(
            received,
            expected,
            "Expected HTTP response code {0}, received {1} instead.".format(
                expected, received
            ),
        )
