import random
import string
from datetime import datetime
from typing import Any
from fileStorage3 import S3
from ms_fa.config import settings


def s3_session() -> S3:
    return S3({
        "aws_access_key_id": settings.S3_ACCESS_KEY,
        "aws_secret_access_key": settings.S3_SECRET_KEY,
        "region": settings.S3_REGION,
        "bucket": settings.S3_BUCKET
    })


def upload_file(origin: str, destination: str) -> str:
    s3 = s3_session()
    return s3.put(origin, destination)


def generate_client_filename(client: Any, filename: str) -> str:
    letters = string.ascii_lowercase
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = ''.join(random.choice(letters) for _ in range(6))
    ext = filename.split(".")[-1]
    return f"{client.id}_{now}_{rand}.{ext}"


def s3_ping() -> bool:
    try:
        s3 = s3_session()
        s3.resource.meta.client.head_bucket(Bucket=settings.S3_BUCKET)
        return True
    except Exception as e:
        print(e)
        return False

