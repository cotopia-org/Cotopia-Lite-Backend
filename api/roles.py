from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.auth import get_current_active_user
from api.utils.role import create_da_role, get_da_role_by_id, delete_da_role
from api.utils.permission_role import create_da_pr, get_da_pr_by_id, delete_da_pr
from db.db_setup import get_db
from schemas.role import Role, RoleBase
from schemas.permission_role import PermissionRole, PermissionRoleBase
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/roles/create", response_model=Role, status_code=201)
async def create_role(
    role: RoleBase,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_da_role(db=db, role=role)


@router.delete("/roles/{role_id}/delete", status_code=204)
async def delete_role(
    role_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_role = get_da_role_by_id(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail=f"Role (id = {role_id}) not found!")
    else:
        if True:  # check permission to to this
            delete_da_role(db=db, role_id=role_id)
        else:
            raise HTTPException(
                status_code=403, detail="You are not allowed to do this!"
            )


@router.post(
    "/roles/{role_id}/add_permissions",
    response_model=List[PermissionRole],
    status_code=201,
)
async def add_permissions_to_role(
    role_id: int,
    permissions: List[PermissionRoleBase],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    response = []
    for each in permissions:
        if each.role_id == role_id:
            create_da_pr(db=db, permission_role=each)
            response.append(each)

    return response


@router.delete("/roles/{role_id}/remove_permissions", status_code=204)
async def remove_permissions_from_role(
    role_id: int,
    permission_role_ids: List[int],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    for each in permission_role_ids:
        db_permission_role = get_da_pr_by_id(db=db, permission_role_id=each)
        if db_permission_role is None:
            raise HTTPException(
                status_code=404, detail=f"permission_role (id = {each}) not found!"
            )
        else:
            if True:  # check permission to to this
                delete_da_pr(db=db, permission_role_id=each)
            else:
                raise HTTPException(
                    status_code=403, detail="You are not allowed to do this!"
                )
