import os
import telebot
from rest_framework.renderers import JSONRenderer


class TgLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.bot = telebot.TeleBot(os.getenv('tg_api_key'))


    def __call__(self, request):

        response = self.get_response(request)
        if 400 >= response.status_code <= 500:
            self.bot.send_message(
                chat_id=os.getenv('chat_id'),
                text=f'Status code: {response.status_code}',
                disable_web_page_preview=True
            )
        # response.accepted_renderer = JSONRenderer()
        # response.accepted_media_type = "application/json"
        # response.renderer_context = {}

        return response