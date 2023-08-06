import os
import telebot


class TgLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.bot = telebot.TeleBot(os.getenv('tg_api_key'))


    def __call__(self, request):

        response = self.get_response(request)
        if 400 <= response.status_code <= 500:
            self.bot.send_message(
                chat_id=os.getenv('chat_id'),
                text=f'Status code: {response.status_code}',
            )
        response.template_name = ''
        return response