from django.shortcuts import render
from twilio.rest import Client 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
import time
from os.path import exists
import os
import io
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def webhook(request):
    if request.method == 'GET':
        print("Comming Response Aditya Shukla")
        resp = {}
        resp['data'] = {}
        mode = request.GET['hub.mode']
        challenge = request.GET['hub.challenge']
        verify_token = request.GET['hub.verify_token']
        my_token = 'tattvafoundation'
        if(mode == 'subscribe' and verify_token == my_token):
            return  Response(challenge, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'POST':
        data = request.POST
        accessToken = 'EAAMJgVQNkgoBAB2mJZA3TnVEiWFT7tjUkZCR1pV4YZBAKkAE7IZCdwDfBC4jCZBAOTt6vK39zN6wQZCvjLCFWxkMgJdanoDozn3cB1ywmfuicQNZBBBSKesdZARKnSVWVekGb0EGo48yCuGRC2sJt1m9bkKRO8A5JkQKOxMLyHasacPV3Ms9ZBFCOE5NIHOiXC4kNBpVynfnLtQZDZD'
        if data.object:
            if data.entry and data.entry[0].changes and data.entry[0].changes.value.message and data.entry[0].changes.value.message[0]:
                phomeNoID = data.entry[0].changes.value.metadata.phone_number_id
                sendFrom = data.entry[0].changes.value.message[0]['from']
                textBody = data.entry[0].changes.value.message[0].text.body

                url = "https://graph.facebook.com/v15.0/"+phomeNoID+"/messages?access_token=" + accessToken
                dataPayload = {
                            "messaging_product": "whatsapp", 
                            "to": sendFrom, 
                            "text":{'body':"Hi, I am Aditya Shukla"}
                             }
                heders = {'Content-Type': 'application/json'}
                response = requests.request("POST", url, headers=headers, data=dataPayload)
                pass
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)


    else:
        return Response("Method Not Allow",status=status.HTTP_403_FORBIDDEN)