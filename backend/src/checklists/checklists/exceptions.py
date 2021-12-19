
class InvalidChecklist(Exception):
    def __init__(self, checklist_id: int, msg: str = 'invalid checklist', *args):
        super(InvalidChecklist, self).__init__(msg, *args)
        self.checklist_id = checklist_id
