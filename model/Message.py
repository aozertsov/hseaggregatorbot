class Message:

    def __init__(self, dates, subject, body, attachments = None):
        print(attachments)
        self.date = dates
        self.subject = subject
        self.body = body
        self.attachments = attachments

    def __str__(self) -> str:
        return 'date:{}, subject:{}, body:{}, attachments: {}'\
            .format(self.date, self.subject, self.body, list(map(lambda x: x.get_name(), self.attachments)))

class Attachment:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def get_name(self):
        return self.name
