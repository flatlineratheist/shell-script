from django.apps import AppConfig
from django.core.signals import setting_changed
from .whatsapp_client import *

# def my_callback(sender, **kwargs):
#     import requests
#     import json
#     client = WhatsAppWrapper()
#     numberList = ["917355177189"]
#     for i in numberList:
#         response = client.send_media_msg("intro_rati","866097454686194", i)


class WapiConfig(AppConfig):
    name = 'wapi'
    # def ready(self):
    #     setting_changed.connect(my_callback)
