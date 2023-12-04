# from django.core.management.base import BaseCommand
# from mainapp.models import Specialist
# import requests
# import logging
# from django.conf import settings

# logger = logging.getLogger(__name__)

# class Command(BaseCommand):
#     help = 'Отправляет ссылку на тест специалистам'

#     def add_arguments(self, parser):
#         parser.add_argument('test_id', type=int)
#         parser.add_argument('specialist_ids', nargs='+', type=int)

#     def handle(self, *args, **options):
#         test_id = options['test_id']
#         specialist_ids = options['specialist_ids']
#         for specialist_id in specialist_ids:
#             try:
#                 specialist = Specialist.objects.get(pk=specialist_id)
#                 self.send_telegram_message(specialist.telegram_chat_id, test_id)
#             except Specialist.DoesNotExist:
#                 logger.error(f'Специалист с ID {specialist_id} не найден')

#     def send_telegram_message(self, chat_id, test_id):
#         token = '6459750758:AAFmjgRCn4ach9QVIXFCDMIoLZunfQrfAf8'
#         url = f'https://api.telegram.org/bot{token}/sendMessage'
#         message = f'Привет! Пожалуйста, пройдите тест: http://127.0.0.1:8000/start_test/{test_id}/'
#         data = {'chat_id': chat_id, 'text': message}
#         response = requests.post(url, data=data)
#         if response.status_code == 200:
#             logger.info(f"Сообщение отправлено на chat_id {chat_id}")
#         else:
#             logger.error(f"Ошибка при отправке сообщения на chat_id {chat_id}: {response.text}")
from django.core.management.base import BaseCommand
from mainapp.models import Specialist
import requests
import logging
from django.conf import settings
import os 

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Отправляет ссылку на тест специалистам'

    def add_arguments(self, parser):
        parser.add_argument('test_id', type=int)
        parser.add_argument('specialist_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        test_id = options['test_id']
        specialist_ids = options['specialist_ids']
        for specialist_id in specialist_ids:
            try:
                specialist = Specialist.objects.get(pk=specialist_id)
                self.send_telegram_message(specialist.telegram_chat_id, test_id)
            except Specialist.DoesNotExist:
                logger.error(f'Специалист с ID {specialist_id} не найден')

    def send_telegram_message(self, chat_id, test_id):
        token = os.environ.get('TELEGRAM_TOKEN') 
        if not token:
            logger.error('Токен Telegram не найден в переменных окружения')
            return

        url = f'https://api.telegram.org/bot{token}/sendMessage'
        message = f'Привет! Пожалуйста, пройдите тест: http://127.0.0.1:8000/start_test/{test_id}/'
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logger.info(f"Сообщение отправлено на chat_id {chat_id}")
        else:
            logger.error(f"Ошибка при отправке сообщения на chat_id {chat_id}: {response.text}")


