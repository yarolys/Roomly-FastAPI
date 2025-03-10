from fastapi import HTTPException, status


UserAlredyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользовател ьуже существует",
) 


IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль",
    )


TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек",
)


TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует",
)


IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена",
)

UserNotInJWTTokenException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров"
)