class AkismetError(Exception):
    pass


class MissingApiKeyError(AkismetError):
    pass


class ParameterError(AkismetError):
    pass


class AkismetServerError(AkismetError):
    pass
