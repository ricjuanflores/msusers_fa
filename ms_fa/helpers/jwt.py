import jwt
from typing import Optional, Dict, Any
from ms_fa.config import settings
from ms_fa.helpers.time import epoch_now


class JwtHelper:
    def __init__(
        self,
        algorithms: str = 'HS256',
        token_lifetime: int = 43200,
        refresh_token_lifetime: int = 86400,
        token_type: str = 'Bearer'
    ):
        self.key = settings.APP_SECRET_KEY
        self.algorithms = algorithms
        self.token_type = token_type
        self.token_lifetime = token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def encode(self, payload: Dict[str, Any], lifetime: int) -> str:
        payload_copy = payload.copy()
        payload_copy['exp'] = epoch_now() + lifetime
        encoded = jwt.encode(payload_copy, self.key, algorithm=self.algorithms)
        return encoded

    def decode(self, token: str) -> Dict[str, Any]:
        token = token.replace(self.token_type, '').strip()
        payload = jwt.decode(token, self.key, algorithms=[self.algorithms])
        return payload

    def get_tokens(self, payload: Dict[str, Any]) -> Dict[str, str]:
        token = self.encode(payload, self.token_lifetime)
        refresh_token = self.encode(payload, self.refresh_token_lifetime)
        return {
            'token': token,
            'refresh_token': refresh_token,
        }

    def check(self, token: str) -> bool:
        try:
            payload = self.decode(token)
            return epoch_now() <= payload['exp']
        except (jwt.InvalidSignatureError, jwt.DecodeError, jwt.ExpiredSignatureError, KeyError):
            return False

