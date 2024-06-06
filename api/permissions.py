from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.permission import create_da_permission
from db.db_setup import get_db
from schemas.permission import Permission, PermissionBase
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/permissions/create", response_model=Permission, status_code=201)
async def create_permission(
    permission: PermissionBase,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_da_permission(db=db, permission=permission)
