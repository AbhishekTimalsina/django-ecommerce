from django.apps import AppConfig
import threading
from keepawake import keep_service_awake




class StoreConfig(AppConfig):
    name = 'store'
    def ready(self):
        threading.Thread(target=keep_service_awake, daemon=True).start()