
class EmailAlreadyTaken(Exception):
    def __init__(self, msg: str = 'email already taken', *args):
        super(EmailAlreadyTaken, self).__init__(msg, *args)
        self.field = 'email'


class InvalidProfile(Exception):
    def __init__(self, profile_id: int = -1, email: str = "", msg: str = 'invalid profile', *args):
        super(InvalidProfile, self).__init__(msg, *args)
        self.profile_id = profile_id
        self.email = email
