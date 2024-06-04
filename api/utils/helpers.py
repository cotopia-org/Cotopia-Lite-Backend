from fastapi import HTTPException


def response(data=None, message="Success"):
    return {
        "meta": {
            "message": message,
        },
        "data": data,
    }


def error(message, code=400):
    raise HTTPException(status_code=code, detail=message)
