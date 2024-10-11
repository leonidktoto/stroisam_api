from fastapi import HTTPException, status


class UserIsNotRegisteredException(HTTPException):
    def __init__(self, detail: str = "Пользователь не зарегистрирован"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

    
class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Пользователь уже существует"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UserIsBlocked(HTTPException):
    def __init__(self, detail: str = "Пользователь временно заблокирован"):
        super().__init__(status_code=status.HTTP_423_LOCKED, detail=detail)


class UserInActive(HTTPException):
    def __init__(self, detail: str = "Пользователь не активен"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        
class UserNotAdmin(HTTPException):
    def __init__(self, detail: str = "Пользователь не администратор"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class IncorrectSmsValidationException(HTTPException):
    def __init__(self, detail: str = "Неверный код подтверждения"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class SmsValidationExpired(HTTPException):
    def __init__(self, detail: str = "Срок действия кода подтверждения истек"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class TokenExpiredException(HTTPException):
    def __init__(self, detail: str = "Срок действия токена истек"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TokenAbsentException(HTTPException):
    def __init__(self, detail: str = "Токен отсутствует"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class IncorrectTokenFormatException(HTTPException):
    def __init__(self, detail: str = "Неверный формат токена"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class InvalidToken(HTTPException):
    def __init__(self, detail: str = "Недействительный токен"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class InvalidTokenType(HTTPException):
    def __init__(self, detail: str = "Неверный тип токена"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UserIsNotPresentException(HTTPException):
    def __init__(self, detail: str = ""):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class CannotAddDataToDatabase(HTTPException):
    def __init__(self, detail: str = "Не удалось добавить запись"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class CannotAddUpdateDatabase(HTTPException):
    def __init__(self, detail: str = "Не удалось обновить запись"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class CannotDeleteFromDatabase(HTTPException):
    def __init__(self, detail: str = "Не удалось удалить запись"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)



class CannotProcessCSV(HTTPException):
    def __init__(self, detail: str = "Не удалось обработать CSV файл"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class CartIsEmpty(HTTPException):
    def __init__(self, detail: str = "Корзина пуста, не возможно создать заказ"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class OrderNumError(HTTPException):
    def __init__(self, detail: str = "Ошибка номера заказа"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class OrderNotCanceled(HTTPException):
    def __init__(self, detail: str = "Заказ не может быть отменен"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
