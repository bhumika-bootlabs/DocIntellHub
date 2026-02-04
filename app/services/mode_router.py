from app.services.prompts.legal import LEGAL_PROMPT
from app.services.prompts.finance import FINANCE_PROMPT
from app.services.prompts.academic import ACADEMIC_PROMPT
from app.services.prompts.healthcare import HEALTHCARE_PROMPT
from app.services.prompts.business import BUSINESS_PROMPT

def get_prompt(mode: str, context: str, question: str):
    prompts = {
        "legal": LEGAL_PROMPT,
        "finance": FINANCE_PROMPT,
        "academic": ACADEMIC_PROMPT,
        "healthcare": HEALTHCARE_PROMPT,
        "business": BUSINESS_PROMPT,
    }

    template = prompts.get(mode)
    if not template:
        raise ValueError("Unsupported mode")

    return template.format(context=context, question=question)
