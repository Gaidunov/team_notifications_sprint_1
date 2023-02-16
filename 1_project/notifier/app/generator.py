from abc import ABC, abstractmethod
from typing import Optional

from templates.letter_template import generate_html_message
import smtplib
from email.mime.text import MIMEText


class Notification(ABC):
    @abstractmethod
    def send(self) -> None:
        ...


class HtmlNotification:
    def __init__(self, html_message: str) -> None:
        self._html_message = html_message

    def send(self) -> None:
        smtp_connection = smtplib.SMTP('localhost', 1025)
        message = self._generate_smtp_message()
        smtp_connection.send_message(message)
        smtp_connection.quit()

    def _generate_smtp_message(self) -> MIMEText:
        message = MIMEText(self._html_message)
        message['From'] = 'notifier@example.com'
        message['To'] = 'recipient@example.com'
        message['Subject'] = 'Film service notification'
        return message


class BaseNotificationGenerator(ABC):
    @abstractmethod
    def make_notification(self) -> Notification:
        ...


class EmailGenerator(BaseNotificationGenerator):
    def __init__(
        self,
        text: str,
        user_name: Optional[str] = None,
    ) -> None:
        self._text = text
        self._user_name = user_name

    def make_notification(self) -> HtmlNotification:
        message_text = generate_html_message(self._text, self._user_name)
        return HtmlNotification(message_text)


class PushGenerator(BaseNotificationGenerator):
    def make_notification(self) -> Notification:
        ...


class SMSGenerator(BaseNotificationGenerator):
    def make_notification(self) -> Notification:
        ...
