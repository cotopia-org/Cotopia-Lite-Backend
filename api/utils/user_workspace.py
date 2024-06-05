from sqlalchemy.orm import Session

from db.models import UserWorkspace as UWRModel
from schemas.user_workspace import UserWorkspaceBase as UserWorkspaceRole

def create_uwr(db: Session, uwr: UserWorkspaceRole):
    db_uwr = UWRModel()
    for var, value in vars(uwr).items():
        if value:
            setattr(db_uwr, var, value)
    db.add(db_uwr)
    db.commit()
    db.refresh(db_uwr)
    return db_uwr
