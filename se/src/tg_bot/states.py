from tg_api import SendMessageRequest, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    DeleteMessageRequest
from yostate import Router, Locator

from django_tg_bot_framework import (
    PrivateChatStateMachine,
    PrivateChatState,
    PrivateChatMessageReceived,
    PrivateChatCallbackQuery,
)

from .models import Conversation
from .decorators import redirect_menu_commands

router = Router(decorators=[redirect_menu_commands])

state_machine = PrivateChatStateMachine(
    router=router,
    session_model=Conversation,
)


@router.register('/')
class FirstUserMessageState(PrivateChatState):
    """Состояние используется для обработки самого первого сообщения пользователя боту.

    Текст стартового сообщения от пользователя игнорируется, а бот переключается в
    следующий стейт, где уже отправит пользователю приветственное сообщение.

    Если вы хотите перекинуть бота в начало диалога -- на "стартовый экран" -- , то используйте другое
    состояние с приветственным сообщением. Это нужно только для обработки первого сообщения от пользователя.
    """

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        # Ignore any user input, redirect to welcome message
        return Locator('/welcome/')


@router.register('/programming-languages/')
class ProgrammingLanguages(PrivateChatState):
    languages_index: int = 0
    programming_languages = [
        {
            'name': 'C#',
        },
        {
            'name': 'Java',
        },
        {
            'name': 'C++',
        },
        {
            'name': 'Python',
        },
    ]

    def enter_state(self) -> Locator | None:
        current_language = self.programming_languages[self.languages_index]

        arrow_keyboard = []
        if self.languages_index > 0:
            arrow_keyboard.append(InlineKeyboardButton(text='⬅️', callback_data='back'))
        if current_language != self.programming_languages[-1]:
            arrow_keyboard.append(InlineKeyboardButton(text='➡️', callback_data='next'))

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            arrow_keyboard,
            [InlineKeyboardButton(text='back', callback_data='main_menu')],
        ])

        SendMessageRequest(
            text=current_language['name'],
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=keyboard,
        ).send()

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        delete_request = DeleteMessageRequest(chat_id=callback_query.message.chat.id,
                                              message_id=callback_query.message.message_id)
        delete_request.send()
        match callback_query.data:
            case 'main_menu':
                return Locator('/main-menu/')
            case 'next':
                return Locator('/programming-languages/', params={'languages_index': self.languages_index+1})
            case 'back':
                return Locator('/programming-languages/', params={'languages_index': self.languages_index-1})


    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        SendMessageRequest(
            text=f'Эхо: {message.text}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()
        return Locator('/programming-languages/')


@router.register('/main-menu/')
class MainMenuState(PrivateChatState):
    def enter_state(self) -> Locator | None:
        SendMessageRequest(
            text='Main Menu',
            chat_id=Conversation.current.tg_chat_id,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text='Languages',
                        ),
                    ],
                ],
            ),
        ).send()

    def process_callback_query(self, callback_query: PrivateChatCallbackQuery) -> Locator | None:
        match callback_query.data:
            case 'welcome':
                return Locator('/welcome/')

    def process_message_received(self, message: PrivateChatMessageReceived) -> Locator | None:
        match message.text:
            case 'Languages':
                return Locator('/programming-languages/')
        SendMessageRequest(
            text=f'Эхо: {message.text}',
            chat_id=Conversation.current.tg_chat_id,
        ).send()
        return Locator('/main-menu/')
