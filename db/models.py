import datetime
import enum
from datetime import timezone
from typing import List

from sqlalchemy import Boolean, String, ForeignKey, Enum, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, )
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(nullable=True)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(511), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)

    workspaces: Mapped[List["Workspace"]] = relationship(back_populates="user")
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
    user_workspace: Mapped[List["UserWorkspace"]] = relationship(back_populates='user')
    room_user: Mapped[List["RoomUser"]] = relationship(back_populates="user")


class Workspace(Base):
    __tablename__ = "workspaces"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="workspaces")

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_private: Mapped[bool] = mapped_column(Boolean(), default=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    banner: Mapped[str] = mapped_column(String(255), nullable=True)

    rooms: Mapped[List["Room"]] = relationship(back_populates="workspace")
    settings: Mapped[List["Setting"]] = relationship(back_populates="workspace")
    user_workspace: Mapped[List["UserWorkspace"]] = relationship(back_populates='workspace')


class UserWorkspace(Base):
    __tablename__ = "user_workspace"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="user_workspace")

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["Workspace"] = relationship(back_populates="user_workspace")

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=True)
    role: Mapped["Role"] = relationship(back_populates="user_workspace")


class Role(Base):
    __tablename__ = "roles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    user_workspace: Mapped[List["UserWorkspace"]] = relationship(back_populates='role')
    permission_role: Mapped[List["PermissionRole"]] = relationship(back_populates='role')


class Room(Base):
    __tablename__ = "rooms"

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["Workspace"] = relationship(back_populates="rooms")

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_locked: Mapped[bool] = mapped_column(Boolean(), default=True)

    password: Mapped[str] = mapped_column(String(511), nullable=False)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=True)

    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

    background_image: Mapped[str] = mapped_column(String(255), nullable=True)
    landing_spot: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")

    messages: Mapped[List["Message"]] = relationship(back_populates="room")
    room_user: Mapped[List["RoomUser"]] = relationship(back_populates="room")


class Message(Base):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="messages")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship(back_populates="messages")

    reply_to: Mapped[int] = mapped_column(Integer(), nullable=True)

    edited: Mapped[bool] = mapped_column(Boolean(), default=False)
    text: Mapped[str] = mapped_column(String(10000), nullable=False)


class VoiceStatus(enum.Enum):
    disconnected = "disconnected"
    muted = "muted"
    unmuted = "unmuted"
    deafened = "deafened"


class VideoStatus(enum.Enum):
    disconnected = "disconnected"
    camera = "sharing camera"
    screen = "sharing screen"


class RoomUser(Base):
    __tablename__ = "room_user"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="room_user")

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship(back_populates="room_user")

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    voice_status: Mapped[VoiceStatus] = mapped_column(Enum(VoiceStatus),
                                                      default=VoiceStatus.disconnected)
    video_status: Mapped[VideoStatus] = mapped_column(Enum(VideoStatus),
                                                      default=VideoStatus.disconnected)

    coordinates: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")
    screenshare_coordinates: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")
    screenshare_size: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")
    video_coordinates: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")
    video_size: Mapped[str] = mapped_column(String(100), nullable=False, default="0, 0")


class Setting(Base):
    __tablename__ = "settings"

    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
    workspace: Mapped["Workspace"] = relationship(back_populates="settings")
    key: Mapped[str] = mapped_column(String(4096), nullable=False)
    value: Mapped[str] = mapped_column(String(4096), nullable=False)


class Permission(Base):
    __tablename__ = "permissions"

    ability: Mapped[str] = mapped_column(String(4096), nullable=False)
    permission_role: Mapped[List["PermissionRole"]] = relationship(back_populates='permission')


class PermissionRole(Base):
    __tablename__ = "permission_role"

    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))
    permission: Mapped["Permission"] = relationship(back_populates="permission_role")

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="permission_role")


class File(Base):
    __tablename__ = "files"

    fileable_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    fileable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)