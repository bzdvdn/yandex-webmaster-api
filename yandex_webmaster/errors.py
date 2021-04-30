class BaseYandexWebmasterError(Exception):
    def __init__(self, error_message: str, error_code: str, *args):
        super().__init__(*args)
        self.error_message = error_message
        self.error_code = error_code

    def __str__(self):
        return f'error_code: {self.error_code}, error_message: {self.error_message}'

    def dict(self) -> dict:
        return {'error_message': self.error_message, 'error_code': self.error_code}


class YandexWebmasterError(BaseYandexWebmasterError):
    pass
