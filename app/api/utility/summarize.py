
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import require_roles

# router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str
    method: str = "extractive"

# @router.post("/summarize/text")
# def summarize_text(
#     data: SummarizeRequest,
#     user=Depends(require_roles(["admin", "lawyer", "researcher", "finance", "business"]))
# ):
#     text = data.text

#     # VERY BASIC summarization logic 
#     sentences = text.split(".")
#     summary = ".".join(sentences[:3]).strip()

#     return {
#         "summary": summary
#     }

from app.services.summarization import effective_extractive_summary
# from app.schemas.summarize import SummarizeRequest

router = APIRouter()

@router.post("/summarize/text")
def summarize_text(
    data: SummarizeRequest,
    user=Depends(require_roles(["admin", "lawyer", "researcher", "finance", "business"]))
):
    text = data.text.strip()

    if not text:
        return {"summary": ""}

    method = data.method or "extractive"

    if method == "extractive":
        summary = effective_extractive_summary(text)
    else:
        summary = effective_extractive_summary(text)

    return {"summary": summary}


