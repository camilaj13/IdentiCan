"""
Storage utilities for file uploads.

Currently returns mock URLs. When R2 storage is configured,
replace the mock functions with actual S3-compatible uploads.
"""

import uuid
from typing import Optional

from app.core.config import settings


def upload_image(file_bytes: bytes, filename: str, folder: str = "noses") -> str:
    """
    Upload an image to storage and return its URL.

    Currently returns a mock URL. Replace with R2/S3 upload when ready.
    """
    # TODO: Implement actual R2 upload when storage is configured
    # if settings.R2_ENDPOINT:
    #     import boto3
    #     s3 = boto3.client(
    #         "s3",
    #         endpoint_url=settings.R2_ENDPOINT,
    #         aws_access_key_id=settings.R2_ACCESS_KEY,
    #         aws_secret_access_key=settings.R2_SECRET_KEY,
    #     )
    #     key = f"{folder}/{uuid.uuid4().hex}_{filename}"
    #     s3.put_object(
    #         Bucket=settings.R2_BUCKET_NAME,
    #         Key=key,
    #         Body=file_bytes,
    #         ContentType="image/jpeg",
    #     )
    #     return f"{settings.R2_ENDPOINT}/{settings.R2_BUCKET_NAME}/{key}"

    file_id = uuid.uuid4().hex[:12]
    return f"https://storage.identican.app/{folder}/{file_id}_{filename}"


def delete_image(url: str) -> bool:
    """
    Delete an image from storage.

    Currently a no-op mock. Replace with R2/S3 delete when ready.
    """
    # TODO: Implement actual R2 delete when storage is configured
    return True
