from typing import Type, Any

from tg_api import SendMessageRequest
from yostate import Locator

from django_tg_bot_framework import (
    PrivateChatState,
    PrivateChatMessageReceived,
)


def redirect_menu_commands(state_class: Type[PrivateChatState]) -> Type[PrivateChatState]:
    class WrappedStateClass(state_class):
        def process(self, event: Any) -> Locator:
            if isinstance(event, PrivateChatMessageReceived):
                SendMessageRequest(
                    text=f'Текущий локатор: {state_class} !',
                    chat_id=event.chat.id,
                ).send()
                text = event.text or ''

                match text.split():
                    case ['/start']:
                        return Locator('/main-menu/')

            return super().process(event=event)
    return WrappedStateClass
