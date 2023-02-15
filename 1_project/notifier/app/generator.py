from abc import ABC, abstractmethod
from typing import Optional

from static.letter_template import generate_html_message


class Notification(ABC):
    @abstractmethod
    def send(self) -> None:
        ...


class HtmlNotification:
    def __init__(self, html_message: str) -> None:
        self.html_message = html_message

    def send(self) -> None:
        """Send notification using Amazon SQS or other service here"""


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
