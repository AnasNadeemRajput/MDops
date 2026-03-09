from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    mrn: str


class ChatOrSymptomRequest(BaseModel):
    mrn: str
    query: Optional[str] = None       # user chat
    symptoms: Optional[str] = None    # optional symptom report