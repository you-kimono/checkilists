
class InvalidChecklist(Exception):
    def __init__(self, checklist_id: int, msg: str = 'invalid checklist', *args):
        super(InvalidChecklist, self).__init__(msg, *args)
        self.checklist_id = checklist_id


class InvalidStep(Exception):
    def __init__(self, step_id: int, msg: str = 'invalid step', *args):
        super(InvalidStep, self).__init__(msg, *args)
        self.step_id = step_id
