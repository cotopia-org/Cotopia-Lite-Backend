from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from livekit import api
from sqlalchemy.orm import Session

from api.utils.auth import (
    get_current_active_user,
)
from api.utils.user import (
    edit_user,
    get_user,
    get_users,
)
from api.utils.user_workspace import create_uwr, delete_uwr, get_uwr
from api.utils.workspace import get_user_workspaces
from db.db_setup import get_db
from schemas.user import User, UserUpdate
from schemas.user_workspace import UserWorkspaceBase, UserWorkspace

router = fastapi.APIRouter()


@router.get("/users", response_model=List[User])
async def read_users(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.post("/users/update", response_model=User)
async def update_user(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return edit_user(db=db, user_id=current_user.id, user=user)


@router.get("/users/workspaces")
async def user_workspaces(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return get_user_workspaces(user=current_user)


@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/livekit/rooms")
async def get_rooms():
    lkapi = api.LiveKitAPI(
        "https://live-kit-server.cotopia.social/",
    )

    # results = await lkapi.room.list_participants(api.ListParticipantsRequest(room='1'))
    results = await lkapi.room.list_rooms(api.ListRoomsRequest())
    print(results, "HERE")
    await lkapi.aclose()


@router.post(
    "/users/{user_id}/give_role", response_model=UserWorkspace, status_code=201
)
async def give_user_a_role(
    user_workspace_role: UserWorkspaceBase,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_uwr(db=db, uwr=user_workspace_role)


@router.delete("/users/{user_id}/remove_role", status_code=204)
async def remove_users_role(
    user_id: int,
    workspace_id: int,
    role_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_uwr = get_uwr(db=db, user_id=user_id, workspace_id=workspace_id, role_id=role_id)
    if db_uwr is None:
        raise HTTPException(
            status_code=404,
            detail="user_worksapce not found!",
        )
    else:
        if True:  # check permission to to this
            delete_uwr(
                db=db, user_id=user_id, workspace_id=workspace_id, role_id=role_id
            )
        else:
            raise HTTPException(
                status_code=403, detail="You are not allowed to do this!"
            )


# TO_DO
# get /users/me/workspaces
