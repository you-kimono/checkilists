
class EmailAlreadyTaken(Exception):
    def __init__(self, msg: str = 'email already taken', *args):
        super(EmailAlreadyTaken, self).__init__(msg, *args)
        self.field = 'email'


class UserNotExisting(Exception):
    def __init__(self, user_id: int, msg: str = 'email already taken', *args):
        super(UserNotExisting, self).__init__(msg, *args)
        self.user_id = user_id
