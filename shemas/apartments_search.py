from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
import re
from typing import List


class Apartments_seach(BaseModel):
    address: str
    radius: int
    app_type: List[str]
