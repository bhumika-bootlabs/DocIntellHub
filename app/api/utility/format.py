from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import require_roles
import json

router = APIRouter()

class FormatRequest(BaseModel):
    text: str
    format: str

@router.post("/format/response")
def format_response(
    data: FormatRequest,
    user=Depends(require_roles(["admin", "lawyer", "researcher","doctor","finance", "business"]))
):
    text = data.text
    fmt = data.format.lower()

    if fmt == "markdown":
        formatted = f"**Response:**\n\n{text}"

    elif fmt == "json":
        formatted = json.dumps({"response": text}, indent=2)

    else:
        formatted = text

    return {
        "formatted_text": formatted
    }

