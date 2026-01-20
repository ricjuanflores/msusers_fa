import json
from redis import Redis
from typing import Any, Union
from ms_fa.helpers.time import epoch_now


class Cache:
    def __init__(self, config: dict) -> None:
        self.chunk_size = 5000
        self.config = config
        self.conn = self.connection()

    def connection(self) -> Redis:
        return Redis(
            host=self.config.get("HOST"),
            port=self.config.get("PORT"),
            username=self.config.get("USERNAME"),
            password=self.config.get("PASSWORD"),
            db=self.config.get("DATABASE")
        )

    def set(self, key: str, value: Any, exp: Union[int, None] = None) -> Union[bool, None]:
        data = json.dumps({
            "data": value,
            "key": key,
            "created_at": epoch_now(),
            "exp": exp
        })
        return self.conn.set(key, data, ex=exp)

    def get(self, key: str) -> Union[Any, None]:
        data = self.get_raw(key)
        return None if data is None else data.get("data")

    def get_raw(self, key: str) -> Union[dict, None]:
        data = self.conn.get(key)
        if data is not None:
            data = json.loads(data)
        return data

    def delete(self, key: str) -> int:
        return self.conn.delete(key)

    def truncate(self, prefix: str = None) -> bool:
        cursor = None
        while cursor != 0:
            c = cursor or 0
            cursor, keys = self.conn.scan(
                cursor=c,
                match=f"{prefix}*" if prefix else "*",
                count=self.chunk_size
            )
            if keys:
                self.conn.delete(*keys)
        return True

    def exists(self, key: str) -> bool:
        return self.conn.exists(key) > 0

    def ping(self) -> bool:
        try:
            return self.conn.ping()
        except Exception:
            return False

