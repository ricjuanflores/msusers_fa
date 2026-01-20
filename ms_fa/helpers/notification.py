import requests
import json
from fastapi import HTTPException
from ms_fa.config import settings


def send_reset_password_notification(phone: str, token: str) -> None:
    data = {
        "template_name": "codigo_cc_gp_codigo_de_ingreso_a_app_movil",
        "phone": f"+521{phone}",
        "params": {
            "codigo": token
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    url = settings.NOTIFICATION_API_URL
    response = requests.post(
        f'{url}/api/v1/notify/whatsapp/template_message/',
        headers=headers,
        data=json.dumps(data)
    )

    if not response.ok:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"error from Bot: {response.text}"
        )

