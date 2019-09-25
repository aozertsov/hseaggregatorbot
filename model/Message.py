class Message:

    def __init__(self, dates, subject, body):
        self.date = dates
        self.subject = subject
        self.body = body

    def print(self):
        return 'date:{}, subject:{}, body:{}'.format(self.date, self.subject, self.body)

    def __str__(self) -> str:
        return 'date:{}, subject:{}, body:{}'.format(self.date, self.subject, self.body)

