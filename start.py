from Mail import Mail
from TelegramConnector import TelegramConnector
import time
from datetime import datetime
import config


def main():
    mail_service = Mail()
    mail_service.build_service()
    while True:
        print('start work in {}'.format(datetime.now()))
        messages = mail_service.get_messages()

        if (len(messages)) > 0:
            fist_message_id = messages[0]['id']
            for message in messages:
                if not config.LAST_MESSAGE_ID == message['id']:
                    print('try to get message with id {}'.format(message['id']))
                    msg = mail_service.get_message(message['id'])
                    connector = TelegramConnector()
                    connector.send_message(msg)
                else:
                    config.LAST_MESSAGE_ID = fist_message_id
                    break

        time.sleep(10)


if __name__ == '__main__':
    main()
