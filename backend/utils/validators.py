import os
from fastapi import HTTPException
from .config import Config

def validate_file_extension(filename: str) -> None:
    """Validate if the file extension is allowed"""
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension not in Config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not supported. Allowed: {Config.ALLOWED_EXTENSIONS}"
        )

def validate_file_size(file_size: int) -> None:
    """Validate if the file size is within limits"""
    if file_size > Config.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {Config.MAX_FILE_SIZE // (1024*1024)}MB"
        ) 