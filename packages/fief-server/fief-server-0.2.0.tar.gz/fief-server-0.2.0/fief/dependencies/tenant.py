from typing import List, Optional, Tuple

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import select

from fief.dependencies.account_managers import get_tenant_manager
from fief.dependencies.pagination import (
    Ordering,
    Pagination,
    get_ordering,
    get_paginated_objects,
    get_pagination,
)
from fief.managers import TenantManager
from fief.models import Tenant


async def get_current_tenant(
    tenant_slug: Optional[str] = Query(None),
    manager: TenantManager = Depends(get_tenant_manager),
) -> Tenant:
    if tenant_slug is None:
        tenant = await manager.get_default()
    else:
        tenant = await manager.get_by_slug(tenant_slug)

    if tenant is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return tenant


async def get_paginated_tenants(
    pagination: Pagination = Depends(get_pagination),
    ordering: Ordering = Depends(get_ordering),
    manager: TenantManager = Depends(get_tenant_manager),
) -> Tuple[List[Tenant], int]:
    statement = select(Tenant)
    return await get_paginated_objects(statement, pagination, ordering, manager)
