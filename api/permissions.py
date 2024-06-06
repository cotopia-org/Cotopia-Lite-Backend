from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.permission import (
    create_da_permission,
    get_da_permission_by_id,
    delete_da_permission,
)
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


@router.delete("/permissions/{permission_id}/delete", status_code=204)
async def delete_permission(
    permission_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_permission = get_da_permission_by_id(db=db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(
            status_code=404, detail=f"Permission (id = {permission_id}) not found!"
        )
    else:
        if True:  # check permission to to this
            delete_da_permission(db=db, permission_id=permission_id)
        else:
            raise HTTPException(
                status_code=403, detail="You are not allowed to do this!"
            )
