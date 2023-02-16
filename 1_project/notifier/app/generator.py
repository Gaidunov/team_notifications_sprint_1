import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Optional

from .api_config.config import config
from .templates.letter_template import generate_html_message


class Notification(ABC):
    @abstractmethod
    def send(self) -> None:
        ...


class HtmlNotification:
    SUBJECT = 'Film service notification'

    def __init__(self, html_message: str) -> None:
        self._html_message = html_message

    def send(self, email: str) -> None:
        smtp_connection = smtplib.SMTP('localhost', 1025)
        message = self._generate_smtp_message(email)
        smtp_connection.send_message(message)
        smtp_connection.quit()

    def _generate_smtp_message(self, email: str) -> MIMEText:
        message = MIMEText(self._html_message)
        message['From'] = config.service_email
        message['To'] = email
        message['Subject'] = self.SUBJECT
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
