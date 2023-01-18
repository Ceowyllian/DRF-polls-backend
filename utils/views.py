from django.core.exceptions import ValidationError as Django_ValidationError
from rest_framework import views
from rest_framework.exceptions import ValidationError as DRF_ValidationError


class APIView(views.APIView):
    def handle_exception(self, exc):
        if isinstance(exc, Django_ValidationError):
            return super().handle_exception(
                DRF_ValidationError(
                    code=getattr(exc, "code", None), detail=exc.messages
                )
            )

        return super().handle_exception(exc)
