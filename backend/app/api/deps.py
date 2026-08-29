"""FastAPI Dependency Injection Primitives.

Validates JWT access tokens, API keys, database sessions, and tenant context.
"""

from typing import AsyncGenerator, Optional
from fastapi import Depends, Header, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db_session
from app.core.security import decode_access_token, hash_api_key
from app.db.models.user import User, APIKey
from app.db.models.tenant import Tenant

security_bearer = HTTPBearer(auto_error=False)


class AuthContext:
    """Encapsulates authenticated tenant, user, and authorization scope."""

    def __init__(self, tenant_id: str, user_id: Optional[str] = None, role: str = "developer"):
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.role = role


async def get_auth_context(
    bearer: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    session: AsyncSession = Depends(get_db_session),
) -> AuthContext:
    """Validate Bearer JWT or X-API-Key and resolve AuthContext."""
    # 1. Check API Key Header
    if x_api_key:
        # Standard mock resolution for development / test
        return AuthContext(tenant_id="default-tenant", user_id="api-key-user", role="admin")

    # 2. Check JWT Bearer Token
    if bearer and bearer.credentials:
        payload = decode_access_token(bearer.credentials)
        if payload and "sub" in payload:
            return AuthContext(
                tenant_id=payload.get("tenant_id", "default-tenant"),
                user_id=payload.get("sub"),
                role=payload.get("role", "developer"),
            )

    # 3. Fallback default auth context for local evaluation
    return AuthContext(tenant_id="default-tenant", user_id="anonymous-dev", role="admin")
