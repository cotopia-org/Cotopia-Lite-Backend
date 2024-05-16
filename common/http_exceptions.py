from fastapi import HTTPException, status

UNAUTHENTICATED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You are not authorized to do this",
    headers={"WWW-Authenticate": "Bearer"},
)

MISSMATCHAUTH = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

NOTFOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not found",
)

CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="",
)

PASS_NOTACCEPTABLE = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Password is too short!",
)
