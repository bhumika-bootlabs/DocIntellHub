from fastapi import Depends, HTTPException, status
from app.auth_rbac.roles import ROLE_DOMAIN_MAP
from app.api.utility.deps import get_current_user


def require_domain_access(domain: str):
    def checker(user=Depends(get_current_user)):
        allowed_domains = ROLE_DOMAIN_MAP.get(user.role, [])

        if domain not in allowed_domains:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user.role}' cannot upload '{domain}' documents",
            )
        return user

    return checker
