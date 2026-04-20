ADMIN = "admin"
LAWYER = "lawyer"
DOCTOR = "doctor"
RESEARCHER = "researcher"
FINANCE = "finance"
BUSINESS = "business"

# ALL_ROLES = [ADMIN, LAWYER, DOCTOR, RESEARCHER, FINANCE, BUSINESS]


ROLE_DOMAIN_MAP = {
    "lawyer": ["legal"],
    "doctor": ["medical"],
    "finance": ["finance"],
    "researcher": ["research"],
    "admin": ["legal", "medical", "finance", "research"],
}
