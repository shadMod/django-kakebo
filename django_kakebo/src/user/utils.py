import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

from user.constants import GOOGLE_RECAPTCHA_VERIFY_URL


def validate_recaptcha(recaptcha: str) -> dict[str, Any]:
    """Validate reCAPTCHA response from Google reCAPTCHA.

    Args:
        recaptcha (str): the reCAPTCHA value.

    Returns:
        dict[str, Any]: the reCAPTCHA response from GOOGLE API.
    """
    values = {
        "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        "response": recaptcha,
    }
    data = urlencode(values).encode()
    request = Request(GOOGLE_RECAPTCHA_VERIFY_URL, data=data)
    with urlopen(request) as response:
        return json.load(response)
