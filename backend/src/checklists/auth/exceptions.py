
class EmailAlreadyTaken(Exception):
    def __init__(self, msg='email already taken', *args):
        super(EmailAlreadyTaken, self).__init__(msg, *args)
        self.field = 'email'
