from fastapi import APIRouter, HTTPException
import httpx
import json

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}
