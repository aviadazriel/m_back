from typing import List

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()




# Get all users
@router.get("/")
def read_users():
    return "its working"

