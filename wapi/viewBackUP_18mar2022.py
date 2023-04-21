from django.shortcuts import render,redirect

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import time
from os.path import exists
import os
import io
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from .whatsapp_client import *
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from .helper import *
import datetime

#################################################################################
###################### IFA Bot By Tattva Foundation #############################
######################      Dev Aditya Shukla ###################################
################################################################################

def indexHomePlayGame(request):
    try:
        username = request.GET.get("username")
        return render(request,'index.html',{'username':username})
    except:
        return render(request,'404.html')


def redirectQuestion(request):
    try:
        username = request.GET.get("username")
        id = request.GET.get("quetion_id")
        q = request.GET.get("q")
        shown = True
        if q == '1':
            shown = False
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        question = WapiGame.objects.get(questionNo=id)
        user = WapiGameController.objects.get(place=mob)
        return render(request,'quiz.html',{'question':question,'user':user,'username':username,'shown':shown})
    except:
        return render(request,'404.html')



def quiz(request):
    print("################$$$$$$$$$$$$$$$$$")
    status = request.GET.get("status")
    status_q = request.GET.get("changeLevel")
    print("SSSSSSSSS",status_q,type(status_q))
    showAnswer = 0

    if status == '0' or status == None :
        showAnswer = 0
    else:
        showAnswer = 1

    print("################$$$$$$$$$$$$$$$$$",status)
    username = request.GET.get("username")
    user = ''
    try:
        print("ENter 1")
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        print('###################')
    except:
        print("ENter 2")
        mob = 'Anonymous'
    else:
        print("ENter 3")
        print("########################################")
        if mob != 'Anonymous':
            try:
                print("Enter 4")
                gameUser = WapiGameController.objects.get(place=mob)
                if status_q == '1':
                    gameUser.level = int(gameUser.level) + 1
                    gameUser.save()
                user = gameUser
            except:
                print("Enter 5")
                gameUser = WapiGameController(place=mob,level='1',total_score='0')
                gameUser.save()
                print("kbjkkbkjb",gameUser.place.name)
                user = gameUser
        else:
            user = 'Anonymous'
    try:
        print("gameUser.place.reg_mobile",gameUser.place.reg_mobile)
        print("gameUser.level123  == ",gameUser.level,type(gameUser.level))
        question = WapiGame.objects.get(questionNo=str(gameUser.level))
        usernameUrl = gameUser.place.reg_mobile
        questionNo = gameUser.level
        # return render(request,'quiz.html',{'question':question,'user':user})

        redirectUrl = "https://ifabot.dev-tattvafoundation.org/question?username="+ usernameUrl+"&quetion_id="+str(questionNo)+"&q="+ str(showAnswer)
        print("RRR",redirectUrl)
        return redirect(redirectUrl)
    except:
        return render(request,'404.html')



def wrong(request):
    try:
        username = request.GET.get("username")
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        gameUser = WapiGameController.objects.get(place=mob)
        countAllQuestion = WapiGame.objects.all()
        if int(gameUser.level)  ==  len(countAllQuestion):
            redirectUrl = "https://ifabot.dev-tattvafoundation.org/winner?username="+ username
            return redirect(redirectUrl)
        else:
            # gameUser.level = int(gameUser.level) + 1
            # gameUser.save()
            return render(request,'wrong.html',{'username':username,"givenAnswerWrong":'1'})
    except:
        return render(request,'404.html')

def correct(request):
    try:
        username = request.GET.get("username")
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        gameUser = WapiGameController.objects.get(place=mob)
        countAllQuestion = WapiGame.objects.all()
        if int(gameUser.level)  ==  len(countAllQuestion):
            gameUser.total_score = int(gameUser.total_score) + 1
            gameUser.save()
            redirectUrl = "https://ifabot.dev-tattvafoundation.org/winner?username="+ username
            return redirect(redirectUrl)
        else:
            gameUser.level = int(gameUser.level) + 1
            gameUser.total_score = int(gameUser.total_score) + 1
            gameUser.save()
            return render(request,'correct.html',{'username':username,"givenAnswerWrong":'0'})
    except:
        return render(request,'404.html')

def winner(request):
    try:
        username = request.GET.get("username")
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        gameUser = WapiGameController.objects.get(place=mob)
        return render(request,'win.html',{'username':username,"givenAnswerWrong":'0','gameUser':gameUser})
    except:
        return render(request,'404.html')

def send_intro_msg(request):
    import requests
    import json
    client = WhatsAppWrapper()
    numberList = ["917355177189","919918961643","919450074759","916394355568"]
    for i in numberList:
        response = client.send_media_msg("intro_rati","866097454686194", i)
        # url = "https://graph.facebook.com/v15.0/102098082798609/messages"
        # payload = json.dumps({
        # "messaging_product": "whatsapp",
        # "to": i,
        # "text": {
        #     "body": "Hello I am Rati, please send hi to continue"
        # }
        # })
        # headers = {
        # 'Authorization': 'Bearer EAAc37c8FyjEBAOhaffy8NI97DVVZByZBysH2dfBKb1auXkK7uKhHcoQZCY2alQyXOVccoQZCdWGiCwZAjrOUqiKwLPHOZB9bfr7PbxLzvTHZCGUKwZAuZBqvK9oZC83lt4xf2gB5Msv3xcKs0ZBGf5ZBO30c3GiN7IndN0WQCW3z0uZAJ6jmfFEC9yo66wrBcZBgII9AoGALGWwoMptAZDZD',
        # 'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
    return render(request,'test.html')




@api_view(['POST'])
def send_template_message(request):
    if request.method == 'POST':
        """_summary_: Send a message with a template to a phone number"""
        if "language_code" not in eval(request.body):
            return Response({"error": "Missing language_code"}, status=HTTP_404_NOT_FOUND)

        if "phone_number" not in eval(request.body):
            return Response({"error": "Missing phone_number"}, status=HTTP_404_NOT_FOUND)

        if "template_name" not in eval(request.body):
            return Response({"error": "Missing template_name"}, status=HTTP_404_NOT_FOUND)
        client = WhatsAppWrapper()
        print("eval(request.body)[",eval(request.body)["template_name"])

        response = client.send_template_message(
            template_name="introductory_message",
            language_code=eval(request.body)["language_code"],
            phone_number=eval(request.body)["phone_number"],
        )
        return Response(
            {
                "data": response,
                "status": "success",
            },
            status=status.HTTP_200_OK
        )









@api_view(['GET','POST'])
def webhook_whatsapp(request):
    """__summary__: Get message from the webhook"""
    VERIFY_TOKEN = 'tattvafoundation'
    if request.method == "GET":
        if request.query_params.get('hub.verify_token') == VERIFY_TOKEN:
            return Response(int(request.query_params.get('hub.challenge')), status=status.HTTP_200_OK)
        return Response("Authentication failed. Invalid Token.", status=status.HTTP_403_FORBIDDEN)
    client = WhatsAppWrapper()
    response = client.process_webhook_notification(request.data)
    print("GH",response, len(response))
    try:
        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
        if checkRegObject:

            ##################################################
            ############ Language Identification #############
            # ################################################
            if response[0]['msg_text'] == 'del_user':
                print("uhijhuj")
                checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                checkRegObject.delete()
                handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी मिटा दी है।",False)

            elif checkRegObject.current_stage=='LANGUAGE_SETUP_PROCESS' and checkRegObject.reg_role=='NA' and checkRegObject.language=='NA':
                if response[0]['msg_text'] == 'ગુજરાતી':
                    checkRegObject.language = 'Gujrati'
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()
                    handleGujratiTextQuery(response[0]['from'],"તમે ગુજરાતી ભાષા પસંદ કરી છે.",True)

                elif response[0]['msg_text'] == 'हिंदी':
                    checkRegObject.language = 'Hindi'
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()
                    handleHindiTextQuery(response[0]['from'],"आपने हिंदी  को पसंदीदा भाषा के रूप में चुना है",True)


                elif response[0]['msg_text'] == 'English':
                    checkRegObject.language = 'English'
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()
                    handleEnglishTextQuery(response[0]['from'],"You have selected English as prefered language",True)

                else:
                    handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                    response = client.send_media_msg("intro_rati","519795810307895", response[0]['from'])






            ##################################################
            ############ Hindi Setup Language ################
            ##################################################
            elif checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='NA':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == 'लाभार्थी':
                        checkRegObject.reg_role = 'Beneficiary'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपने लाभार्थी का चयन किया है। ",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपना नाम दर्ज करें",False)
                    elif response[0]['msg_text'] == 'स्वास्थ्य कार्यकर्ता': 
                        checkRegObject.reg_role = 'HCW'
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपने स्वास्थ्य कार्यकर्ता का चयन किया है। ",False)
                        client.sendMsgForConfirmation("आप आशा हैं या एएनएम",response[0]['from'],"एएनएम","आशा")
                        # client.send_media_msg("hwc_identification","724155319105458", response[0]['from'],'hi')
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == 'Beneficiary':
                        checkRegObject.reg_role = 'Beneficiary'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You have selected Beneficiary. ",False)
                        handleEnglishTextQuery(response[0]['from'],"Please enter your name",False)
                    elif response[0]['msg_text'] == 'Health Worker':
                        checkRegObject.reg_role = 'HCW'
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You have selected Healthworker. ",False)
                        client.sendMsgForConfirmation("Are you an Asha or ANM",response[0]['from'],"ANM","ASHA")
                    else:
                        handleEnglishTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)




            ######################################
            #### Health Worker Identification ####
            ######################################
            elif checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='HCW':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == 'एएनएम':
                        checkRegObject.reg_role = 'ANM'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपने एएनएम का चयन किया है।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपना नाम दर्ज करें",False)

                    elif response[0]['msg_text'] == 'आशा':
                        checkRegObject.reg_role = 'ASHA'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपने आशा का चयन किया है।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपना नाम दर्ज करें",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == 'ANM':
                        checkRegObject.reg_role = 'ANM'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You are ANM.",False)
                        handleEnglishTextQuery(response[0]['from'],"Please enter your name",False)

                    elif response[0]['msg_text'] == 'ASHA':
                        print("Comming 6")
                        checkRegObject.reg_role = 'ASHA'
                        checkRegObject.current_stage = "What_is_your_name"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You are ASHA.",False)
                        handleEnglishTextQuery(response[0]['from'],"Please enter your name",False)
                    else:
                        handleEnglishTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)






            # Hindi Beneficiary Registration Start
            elif checkRegObject.reg_role=='Beneficiary' and checkRegObject.current_stage=='What_is_your_name':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_age"
                    checkRegObject.save()
                    beneData = RegBeneficiary(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"कृपया अपनी उम्र दर्ज करें",False)

                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_age"
                    checkRegObject.save()
                    beneData = RegBeneficiary(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleEnglishTextQuery(response[0]['from'],"Please enter your age",False)

                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass




            elif checkRegObject.current_stage=='What_is_your_age' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"AGE")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "What_is_your_mobile"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.age = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                    elif sta == "AGE_LIMIT":
                        handleHindiTextQuery(response[0]['from'],"यह आवेदन विशेष रूप से 18-49 वर्ष की आयु वर्ग की महिलाओं के लिए है। कृपया सही आयु दर्ज करें",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपनी उम्र दर्ज करें",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपनी उम्र दर्ज करें",False)
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"AGE")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "What_is_your_mobile"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.age = response[0]['msg_text']
                        beneData.save()
                        handleEnglishTextQuery(response[0]['from'],"Please enter the mobile number you want to register",False)
                        # client.sendMsgForConfirmation("you want to move from this number" + response[0]['from'],response[0]['from'],"Yes","No")
                    elif sta == "AGE_LIMIT":
                        handleEnglishTextQuery(response[0]['from'],"This application is specifically for women between age group of 18-49 years. Please enter the correct age",False)
                        handleEnglishTextQuery(response[0]['from'],"Please enter your age",False)

                    else:
                        handleEnglishTextQuery(response[0]['from'],"You have entered wrong input",False)
                        handleEnglishTextQuery(response[0]['from'],"Please enter your age",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        print("getAllStateName('Hindi')",getAllStateName('Hindi'))
                        templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllStateName('Hindi')
                                }
                            ]
                        print(templateData)

                        client.interactivte_reply_list(templateData,"कृपया अपने राज्य का चयन करें" ,response[0]['from'],"दबाएँ")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllStateName("English")
                                }
                            ]

                        client.interactivte_reply_list(templateData,"Please select your state" ,response[0]['from'],"Click")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"Please enter a 10 digit number.",False)
                        handleHindiTextQuery(response[0]['from'],"Please enter the mobile number you want to register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data.",False)
                        handleHindiTextQuery(response[0]['from'],"Please enter the mobile number you want to register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass








            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"कृपया अपने जिले का चयन करें",False)
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllDistrctNameByID('Hindi',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने जिले का चयन करें" ,response[0]['from'],"दबाएँ")
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllDistrctNameByID('English',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your district" ,response[0]['from'],"Click")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllBlocktNameByID('Hindi',beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने ब्लॉक का चयन करें" ,response[0]['from'],"दबाएँ")
                    
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"Please select your block",False)
                    templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllBlocktNameByID("English",beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your block" ,response[0]['from'],"Click")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_village"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"कृपया अपने गांव का नाम दर्ज करें",False)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_village"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"Please enter your village name",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "asking_for_confirmation"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    beneregData = RegBeneficiary.objects.filter(place=checkRegObject)
                    datamsg = ''
                    for ii in beneregData:
                        datamsg = "नाम: " + ii.name  +"\n"+"आयु: "+ ii.age +"\n"+"मोबाइल नंबर: "+ ii.mobile_number +"\n"+"राज्य: "+ii.state +"\n"+"ज़िला: "+ ii.district +"\n"+"खंड: "+ ii.block +"\n"+"गांव: "+ ii.village
                    handleHindiTextQuery(response[0]['from'], datamsg ,False)
                    client.interactivte_reply("क्या आप यह जानकारी जमा करना चाहते हैं?", response[0]['from'],returnYesHindi(),returnNoHindi())

                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "asking_for_confirmation"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    beneregData = RegBeneficiary.objects.filter(place=checkRegObject)
                    datamsg = ''
                    for ii in beneregData:
                        datamsg = "Name: " + ii.name  +"\n"+"Age: "+ ii.age +"\n"+"Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Village: "+ ii.village
                    handleHindiTextQuery(response[0]['from'], datamsg ,False)
                    client.interactivte_reply("Do you want to submit the form?", response[0]['from'],"Yes","No")

                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "हमारे साथ पंजीकरण करने के लिए धन्यवाद।" ,False)
                        templateData = [
                                {
                                "title":  "एक विकल्प चुने",
                                "rows": [
                                    {
                                    "id": "currently_pragnant",
                                    "title": "गर्भवती महिला"
                                    },
                                    {
                                    "id": "child_age_6",
                                    "title": "शिशु 6 महीने से कम उम्र"
                                    },
                                    {
                                    "id": "reproductive_women",
                                    "title": "अन्य (आयु वर्ग 18-49)"
                                    }
                                ]
                                }
                            ]

                        # client.send__msg_button_without_media("beneficiary_identification", response[0]['from'],'hi') Template Disbale
                        client.interactivte_reply_list(templateData,"इनमें से एक विकल्प चुनें",response[0]['from'],"चुनें")
                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी मिटा दी है।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया जारी रखने के लिए कुछ लिखें।",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "Thank you for registering with us." ,False)
                        templateData = [
                                {
                                "title":  "choose an option",
                                "rows": [
                                    {
                                    "id": "currently_pragnant",
                                    "title": "Pregnant Women"
                                    },
                                    {
                                    "id": "child_age_6",
                                    "title": "Infant less than 6 month"
                                    },
                                    {
                                    "id": "reproductive_women",
                                    "title": "Other( age group 18-49)"
                                    }
                                ]
                                }
                            ]

                        # client.send__msg_button_without_media("beneficiary_identification", response[0]['from'],'hi') Template Disbale
                        client.interactivte_reply_list(templateData,"choose an option",response[0]['from'],"Choose")
                    elif response[0]['msg_text'] == "No":
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"We removed your information, please enter your information again.",False)
                        handleHindiTextQuery(response[0]['from'],"Please write something to continue.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass







            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    handleEnglishTextQuery(response[0]['from'],"आपने चुना  " + response[0]['msg_text'],False)
                    print("Commning ================ Comming")
                    if response[0]['msg_text'] ==  "गर्भवती महिला":
                        print("BJBIJBI Aditya")
                        checkRegObject.current_stage = "topic_selection_pragnant"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"903952143978601")
                        client.interactivte_reply("क्या आपके पास आरसीएच नंबर है? यह आपको आपके एएनसी कार्ड में मिल जाएगा", response[0]['from'],returnYesHindi(),returnNoHindi())

                    elif response[0]['msg_text'] == "शिशु 6 महीने से कम उम्र":
                        checkRegObject.current_stage = "topic_selection_lacting"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"903952143978601")
                        client.interactivte_reply("क्या आपके पास आरसीएच नंबर है? यह आपको आपके एएनसी कार्ड में मिल जाएगा", response[0]['from'],returnYesHindi(),returnNoHindi())

                    elif response[0]['msg_text'] ==  "अन्य (आयु वर्ग 18-49)":
                        checkRegObject.current_stage = "topic_selection_wra"
                        checkRegObject.save()
                        client.interactivte_reply("क्या आप जानते हैं आपके शरीर में कितने प्वाइंट खून है??",response[0]['from'],returnYesHindi(),returnNoHindi())
                    else:
                        handleHindiTextQuery(response[0]['from'],"कृपया मान्य विकल्प चुनें",False)
                elif checkRegObject.language=='English':
                    handleEnglishTextQuery(response[0]['from'],"You Selected " + response[0]['msg_text'],False)
                    if response[0]['msg_text'] ==  "Pregnant Women":
                        checkRegObject.current_stage = "topic_selection_pragnant"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"903952143978601")
                        client.interactivte_reply("Do you have RCH number? You will find this in your ANC card", response[0]['from'],"Yes","No")

                    elif response[0]['msg_text'] == "Infant less than 6 month":
                        checkRegObject.current_stage = "topic_selection_lacting"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"903952143978601")
                        client.interactivte_reply("Do you have RCH number? You will find this in your ANC card", response[0]['from'],"Yes","No")

                    elif response[0]['msg_text'] ==  "Other( age group 18-49)":
                        checkRegObject.current_stage = "topic_selection_wra"
                        checkRegObject.save()
                        client.interactivte_reply("Do you know your hemoglobin level in blood?",response[0]['from'],"Yes","No")
                    else:
                        handleHindiTextQuery(response[0]['from'],"Please select a valid option.",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            ##################################################################################
            #########################################  Pragnant ##############################
            ##################################################################################
            elif checkRegObject.current_stage=='topic_selection_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "asking_rch_number_pragnant"
                        checkRegObject.save()
                        # client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'hi')
                        handleHindiTextQuery(response[0]['from'],"कृपया अपना आरसीएच नंबर टाइप करें",False)


                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject.current_stage = "asking_rch_number_na_pragnant"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = "NA"
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"यदि आपने अपना एएनसी कार्ड पंजीकृत नहीं किया है या खो दिया है तो कृपया अपनी आशा या एएनएम से संपर्क करें",False)
                        handleHindiTextQuery(response[0]['from'],"आपकी अंतिम मासिक तिथि कब थी ? (उदाहरण के लिए 05/10/2022)",False)
                        # handleHindiTextQuery(response[0]['from'],"कृपया अपना आरसीएच नंबर टाइप करें,,  उदाहरण के लिए 05/10/2022",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)

                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "asking_rch_number_pragnant"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"Please type your RCH number",False)
                        # client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'en')

                    elif response[0]['msg_text'] == "No":
                        checkRegObject.current_stage = "asking_rch_number_na_pragnant"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = "NA"
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"If you have not recieved your RCH card please visit your ASHA or ANM and ask for your card.",False)
                        handleHindiTextQuery(response[0]['from'],"When did you get your last menstrual period?,( .eg 05/10/202)2",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            elif checkRegObject.current_stage=='asking_rch_number_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"RCH")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "enter_menstrual_date_pragnant"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"आपकी अंतिम मासिक तिथि कब थी ? (उदाहरण के लिए 05/10/2022)",False)
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 12 अंकों की अनुमति है।",False)
                        handleHindiTextQuery(response[0]['from'],"आपका आरसीएच नंबर क्या है?",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपका आरसीएच नंबर क्या है?",False)



                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"RCH")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "enter_menstrual_date_pragnant"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"When did you get your last menstrual period? (e.g 05/10/2022)",False)
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"A maximum of 11 digits is allowed.",False)
                        handleHindiTextQuery(response[0]['from'],"Please type your RCH number",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"Please type your RCH number",False)


                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            elif checkRegObject.current_stage=='asking_rch_number_na_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"दिनांक प्रारूप dd/mm/yy होना चाहिए, उदाहरण के लिए 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"आपकी अंतिम मासिक तिथि कब थी ?,  उदाहरण के लिए 05/10/2022",False)
                    else:
                        checkRegObject.current_stage = "cal_menstrual_date_pragnant"
                        checkRegObject.save()
                        from datetime import date
                        from dateutil.relativedelta import relativedelta
                        new_date = date_object + relativedelta(months=9,days=7)
                        print("new_date",new_date)
                        new_date = new_date.strftime("%d/%m/%Y")
                        handleHindiTextQuery(response[0]['from'],"आप गर्भावस्था के अपने " + calculateTrimester(response[0]['msg_text'],"Hindi") + " ट्राइमेस्टर में हैं। आपकी डिलीवरी की अपेक्षित तिथि "+ str(new_date) +"  है" ,False)
                        client.interactivte_reply("क्या आप जानते हैं आपके शरीर में कितने प्वाइंट खून है??",response[0]['from'],returnYesHindi(),returnNoHindi())
                elif checkRegObject.language=='English':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"Date format should be dd/mm/yy, eg 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"When did you get your last menstrual period?,( .eg 05/10/202)2",False)
                    else:
                        checkRegObject.current_stage = "cal_menstrual_date_pragnant"
                        checkRegObject.save()
                        from datetime import date
                        from dateutil.relativedelta import relativedelta
                        new_date = date_object + relativedelta(months=9,days=7)
                        print("new_date",new_date)
                        new_date = new_date.strftime("%d/%m/%Y")
                        handleHindiTextQuery(response[0]['from'],"You are in your "+ calculateTrimester(response[0]['msg_text'],"English") +" trimester of pregnancy. Your expected date of delivery is" + str(new_date),False)
                        client.interactivte_reply("Do you know your hemoglobin level in blood?",response[0]['from'],"Yes","No")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            # Reply By Bot
            elif checkRegObject.current_stage=='enter_menstrual_date_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                        import datetime
                        today = datetime.date.today()
                        year = today.year
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"दिनांक प्रारूप dd/mm/yy होना चाहिए, उदाहरण के लिए 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया अपना आरसीएच नंबर टाइप करें,,  उदाहरण के लिए 05/10/2022",False)

                    else:
                        if year == date_object.year or year - 1 == date_object.year:
                            checkRegObject.current_stage = "cal_menstrual_date_pragnant"
                            checkRegObject.save()
                            from datetime import date
                            from dateutil.relativedelta import relativedelta
                            new_date = date_object + relativedelta(months=9,days=7)
                            print("new_date",new_date)
                            new_date = new_date.strftime("%d/%m/%Y")
                            handleHindiTextQuery(response[0]['from'],"आपकी डिलीवरी की तारीख  "+    str(new_date)  +" आप अपनी -  "   +calculateTrimester(response[0]['msg_text'],"Hindi")+" में हैं",False)
                            client.interactivte_reply("क्या आप जानते हैं आपके शरीर में कितने प्वाइंट खून है??",response[0]['from'],returnYesHindi(),returnNoHindi())
                        else:
                            handleHindiTextQuery(response[0]['from'],"आपने गलत समय अवधि दर्ज की है",False)
                            handleHindiTextQuery(response[0]['from'],"कृपया अपना आरसीएच नंबर टाइप करें, ,  उदाहरण के लिए 05/10/2022",False)
                elif checkRegObject.language=='English':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                        import datetime
                        today = datetime.date.today()
                        year = today.year
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"Date format should be dd/mm/yy, eg 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"When did you get your last menstrual period?,( .eg 05/10/202)2",False)

                    else:
                        if year == date_object.year or year - 1 == date_object.year:
                            checkRegObject.current_stage = "cal_menstrual_date_pragnant"
                            checkRegObject.save()
                            from datetime import date
                            from dateutil.relativedelta import relativedelta
                            new_date = date_object + relativedelta(months=9,days=7)
                            print("new_date",new_date)
                            new_date = new_date.strftime("%d/%m/%Y")
                            handleHindiTextQuery(response[0]['from'],"Your delivery date "+ str(new_date) +" you are in your - " +calculateTrimester(response[0]['msg_text'],"English")+"",False)
                            client.interactivte_reply("Do you know your hemoglobin level in blood?",response[0]['from'],"Yes","No")
                        else:
                            handleHindiTextQuery(response[0]['from'],"You entered an incorrect time period",False)
                            handleHindiTextQuery(response[0]['from'],"When did you get your last menstrual period?,( .eg 05/10/202)2",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            elif checkRegObject.current_stage=='cal_menstrual_date_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "cal_hemoglobin_level_pragnant"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है?",False)

                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject.current_stage = "know_more_and_no_hb_pragnant"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"कृपया अपने नजदीकी आशा या एएनएम से मिलें और अपने हीमोग्लोबिन के स्तर की जांच करवाएं।",False)
                        # Hindi Else More Anything
                        ElseMoreHindi(response)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "cal_hemoglobin_level_pragnant"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"What is the hemoglobin level in your blood?",False)

                    elif response[0]['msg_text'] == "No":
                        checkRegObject.current_stage = "know_more_and_no_hb_pragnant"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"Please visit your nearest ASHA or ANM and get your hemoglobin levels checked.",False)
                        # English Else More Anything
                        ElseMoreEnglish(response)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            elif checkRegObject.current_stage=='cal_hemoglobin_level_pragnant' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"HB")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "cal_hb_levelknow_more_pragnant"
                        checkRegObject.save()
                        reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                        handleHindiTextQuery(response[0]['from'], reDtata,False)
                        client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें  👆" , "https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
                        ElseMoreHindi(response)
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 2 अंकों की अनुमति है।",False)
                        handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने बिंदु रक्त हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने पिंट रक्त है",False)
                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"HB")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "cal_hb_levelknow_more_pragnant"
                        checkRegObject.save()
                        reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                        handleHindiTextQuery(response[0]['from'], reDtata,False)
                        client.send_media_url("Click here to know more about Anemia  👆" , "https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
                        # Hindi Else More Anything
                        ElseMoreEnglish(response)
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"max  2 digit allowed.",False)
                        handleHindiTextQuery(response[0]['from'],"What is the hemoglobin level in your blood?",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"What is the hemoglobin level in your blood?",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass










            # Schedule Message Section For Animic
            #############################################

            # Section 1
            #################
            # IFA Tablet Take Or Not ::
            elif response[0]['msg_text'] == "ifa_tablet_take_or_not" and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "ifa_tablet_take_or_not_reply"
                    checkRegObject.save()
                    scheduleMessage_pragnant("ifa_tablet_take_or_not",response,'Hindi')
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "ifa_tablet_take_or_not_reply"
                    checkRegObject.save()
                    scheduleMessage_pragnant("ifa_tablet_take_or_not",response,'English')

                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            elif checkRegObject.current_stage=='ifa_tablet_take_or_not_reply'  and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")
                        time.sleep(1)
                        client.interactivte_reply("क्या आयरन की गोली लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य?",response[0]['from'],returnYesHindi(),returnNoHindi())
                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                        checkRegObject.save()
                        client.interactivte_reply("क्या आयरन की गोली लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य?",response[0]['from'],returnYesHindi(),returnNoHindi())
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                        checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")
                        time.sleep(1)
                        client.interactivte_reply("Do you feel any discomfort after taking iron pills? such as abdominal pain, vomiting, indigestion, other",response[0]['from'],"yes","No")
                    elif response[0]['msg_text'] == "No":
                        checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                        checkRegObject.save()
                        client.interactivte_reply("Do you feel any discomfort after taking iron pills? such as abdominal pain, vomiting, indigestion, other",response[0]['from'],"yes","No")
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            # Side Effect Of IFA Tablet
            elif checkRegObject.current_stage=='ifa_tablet_take_or_not_reply_yes'  and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        # client.send_image_message( response[0]['from'],"2046604365730653")
                        client.send_media_url("आयरन की गोलियों के बारे में जानने के लिए क्लिक करें","https://www.youtube.com/watch?v=I1snaZw45zU",response[0]['from'])
                        # handleHindiTextQuery(response[0]['from'],"जल्द से जल्द अपने नजदीकी स्वास्थ्य केंद्र पर जाएं और जांच कराएं !!",False)

                    elif response[0]['msg_text'] == returnNoHindi():
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        # client.send_image_message( response[0]['from'],"2046604365730653")
                        client.send_media_url("Click to know about Iron tablets","https://www.youtube.com/watch?v=I1snaZw45zU",response[0]['from'])
                        # handleHindiTextQuery(response[0]['from'],"जल्द से जल्द अपने नजदीकी स्वास्थ्य केंद्र पर जाएं और जांच कराएं !!",False)

                    elif response[0]['msg_text'] == "No":
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            # Section 2
            #################
            # Don't Forget IFA Tablet
            elif response[0]['msg_text'] == "do_not_forget_iron_tablet" and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    # checkRegObject.current_stage = "complete_msg"
                    # checkRegObject.save()
                    scheduleMessage_pragnant("do_not_forget_iron_tablet",response,"Hindi")
                elif checkRegObject.language=='English':
                    # checkRegObject.current_stage = "complete_msg"
                    # checkRegObject.save()
                    scheduleMessage_pragnant("do_not_forget_iron_tablet",response,"English")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


             # Section 3  Health Checkup
            ###############################
            # Did you go for Health Checkup
            elif response[0]['msg_text'] == "did_you_complete_health_checkup" and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "health_checkup_or_not_reply"
                    checkRegObject.save()
                    scheduleMessage_pragnant("did_you_complete_health_checkup",response,"Hindi")
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "health_checkup_or_not_reply"
                    checkRegObject.save()
                    scheduleMessage_pragnant("did_you_complete_health_checkup",response,"English")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='health_checkup_or_not_reply'  and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        # checkRegObject.current_stage = "take_or_not_reply_yes"
                        # checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up
                    elif response[0]['msg_text'] == returnNoHindi():
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        scheduleMessage_pragnant("go_quick_health_checkup",response,"Hindi")
                        client.send_media_url("क्लिक ","https://youtu.be/5qtdVD83vL8",response[0]['from'])
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        # checkRegObject.current_stage = "take_or_not_reply_yes"
                        # checkRegObject.save()
                        client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up
                    elif response[0]['msg_text'] == "No":
                        # checkRegObject.current_stage = "complete_msg"
                        # checkRegObject.save()
                        scheduleMessage_pragnant("go_quick_health_checkup",response,"English")
                        client.send_media_url("Click ","https://youtu.be/5qtdVD83vL8",response[0]['from'])
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




              # Section 3  Calcium Take Or Not Checkup
            ##################################
            elif response[0]['msg_text'] == "calcium_medicine_take" and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    scheduleMessage_pragnant("iromMdecine",response,"Hindi")
                elif checkRegObject.language=='English':
                    scheduleMessage_pragnant("iromMdecine",response,"English")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            





            ##################################################################################
            #########################################  Lactating ##############################
            ##################################################################################

            elif checkRegObject.current_stage=='topic_selection_lacting' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "asking_rch_number_lacting"
                        checkRegObject.save()
                        client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'hi')

                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject.current_stage = "asking_rch_number_lacting"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = "NA"
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"यदि आपने अपना एएनसी कार्ड पंजीकृत नहीं किया है या खो दिया है तो कृपया अपनी आशा या एएनएम से संपर्क करें",False)
                        handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक,  उदाहरण के लिए 05/10/2022",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "asking_rch_number_lacting"
                        checkRegObject.save()
                        client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'en')

                    elif response[0]['msg_text'] == "No":
                        checkRegObject.current_stage = "asking_rch_number_lacting"
                        checkRegObject.save()
                        beneData = RegBeneficiary.objects.get(place=checkRegObject)
                        beneData.rch_number = "NA"
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"If you have not registered or lost your ANC card, please contact your ASHA or ANM",False)
                        handleHindiTextQuery(response[0]['from'],"Child's date of birth, eg 05/10/2022",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            elif checkRegObject.current_stage=='asking_rch_number_lacting' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "enter_child_date_lacting"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.rch_number = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक उदाहरण के लिए 05/10/2022",False)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "enter_child_date_lacting"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.rch_number = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"Date of birth of the child eg 05/10/2022",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass





            elif checkRegObject.current_stage=='enter_child_date_lacting' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                        import datetime
                        today = datetime.date.today()
                        year = today.year
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"दिनांक प्रारूप dd/mm/yy होना चाहिए, उदाहरण के लिए 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक उदाहरण के लिए 05/10/2022",False)

                    else:
                        if year == date_object.year or year - 1 == date_object.year:
                            from datetime import date
                            from dateutil.relativedelta import relativedelta
                            new_date = date_object + relativedelta(months=9,days=7)
                            print("new_date",new_date)
                            reD = checkBirthCalculation(date_object)
                            if reD == 'A_6':
                                checkRegObject.current_stage = "child_after_6"
                                checkRegObject.save()
                                handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने से अधिक है।",False)
                                client.interactivte_reply("क्या आप जानते हैं आपके शरीर में कितने प्वाइंट खून है??",response[0]['from'],returnYesHindi(),returnNoHindi())

                            if reD == 'B_6':
                                checkRegObject.current_stage = "child_before_6"
                                checkRegObject.save()
                                handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने से कम है।",False)
                                handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!!",False)
                                client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],returnYesHindi(),returnNoHindi())
                            if reD == 'E_6':
                                handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने का है।",False)
                                client.interactivte_reply("क्या आप जानते हैं आपके शरीर में कितने प्वाइंट खून है??",response[0]['from'],returnYesHindi(),returnNoHindi())
                        else:
                            handleHindiTextQuery(response[0]['from'],"आपने गलत समय अवधि दर्ज की है",False)
                            handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक उदाहरण के लिए 05/10/2022",False)
                elif checkRegObject.language=='English':
                    try:
                        from datetime import datetime
                        date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                        import datetime
                        today = datetime.date.today()
                        year = today.year
                    except ValueError as err:
                        handleHindiTextQuery(response[0]['from'],"Date format should be dd/mm/yy, eg 05/10/2022",False)
                        handleHindiTextQuery(response[0]['from'],"Date of birth of the child eg 05/10/2022",False)

                    else:
                        if year == date_object.year or year - 1 == date_object.year:
                            from datetime import date
                            from dateutil.relativedelta import relativedelta
                            new_date = date_object + relativedelta(months=9,days=7)
                            print("new_date",new_date)
                            reD = checkBirthCalculation(date_object)
                            if reD == 'A_6':
                                checkRegObject.current_stage = "child_after_6"
                                checkRegObject.save()
                                handleHindiTextQuery(response[0]['from'],"Your baby is over 6 months old.",False)
                                client.interactivte_reply("Do you know your hemoglobin level in blood?",response[0]['from'],"Yes","No")

                            if reD == 'B_6':
                                checkRegObject.current_stage = "child_before_6"
                                checkRegObject.save()
                                handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने से कम है।",False)
                                handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!!",False)
                                client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],returnYesHindi(),returnNoHindi())
                            if reD == 'E_6':
                                handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने का है।",False)
                                client.interactivte_reply("Do you know your hemoglobin level in blood?",response[0]['from'],"Yes","No")
                        else:
                            handleHindiTextQuery(response[0]['from'],"You entered an incorrect time period",False)
                            handleHindiTextQuery(response[0]['from'],"Date of birth of the child eg 05/10/2022",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            #########################################################
            ############ Child After 6 Question #######################
            ###########################################################

            elif checkRegObject.current_stage=='child_after_6' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "cal_hemoglobin_level_lacting"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है?",False)

                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject.current_stage = "know_more_and_no_hb_lacting"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                        ElseMoreHindi(response)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "cal_hemoglobin_level_lacting"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"What is the hemoglobin level in your blood?",False)

                    elif response[0]['msg_text'] == "No":
                        checkRegObject.current_stage = "know_more_and_no_hb_lacting"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"Please visit your nearest ASHA or ANM and check your hemoglobin level",False)
                        ElseMoreEnglish(response)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass






            elif checkRegObject.current_stage=='cal_hemoglobin_level_lacting' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "cal_hemoglobin_level_amt_lacting"
                    checkRegObject.save()
                    reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                    handleHindiTextQuery(response[0]['from'], reDtata,False)
                    ElseMoreHindi(response)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "cal_hemoglobin_level_amt_lacting"
                    checkRegObject.save()
                    reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                    handleHindiTextQuery(response[0]['from'], reDtata,False)
                    ElseMoreEnglish(response)

                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            #########################################################
            ############ Child Before 6 Question #######################
            ###########################################################

            # elif checkRegObject.current_stage=='child_before_6' and checkRegObject.reg_role=='Beneficiary':
            #     if checkRegObject.language=='Hindi':
            #         checkRegObject.current_stage = "child_before_6_level_lacting"
            #         checkRegObject.save()
            #         handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!!",False)
            #         client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],returnYesHindi(),returnNoHindi())
            #     elif checkRegObject.language=='English':
            #         checkRegObject.current_stage = "child_before_6_level_lacting"
            #         checkRegObject.save()
            #         handleHindiTextQuery(response[0]['from'],"Don't forget to take your iron pill!!!!",False)
            #         client.interactivte_reply("did you take calcium tablet today??",response[0]['from'],"Yes","No")
            #     elif checkRegObject.language=='Gujrati':
            #         handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

            #     else:
            #         pass


            elif checkRegObject.current_stage=='child_before_6' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        client.send_image_message( response[0]['from'],"583006833411655")
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')

                    elif  response[0]['msg_text'] == returnNoHindi():
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                    else:
                        # handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        client.send_image_message( response[0]['from'],"583006833411655")
                        AboutSomthingMore(response,response[0]['msg_text'],'English')

                    elif response[0]['msg_text'] == "No":
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                    else:
                        # handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




        ##################################################################################
        #########################################  WRA ##############################
        ##################################################################################



            elif checkRegObject.current_stage=='topic_selection_wra' and checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "cal_hemoglobin_level_wra"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है?",False)

                    elif response[0]['msg_text'] == returnNoHindi():
                        handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                        ElseMoreHindi(response)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "cal_hemoglobin_level_wra"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'],"how many points of blood in your body है",False)

                    elif response[0]['msg_text'] == "No":
                        handleHindiTextQuery(response[0]['from'],"Please visit your nearest ASHA or ANM and check your hemoglobin level",False)
                        ElseMoreEnglish(response)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass
                    
            



            elif checkRegObject.current_stage=='cal_hemoglobin_level_wra' and checkRegObject.reg_role=='Beneficiary':
                print('#$$$$$$$$$$$$$########')
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "cal_hemoglobin_level_wra_com"
                    checkRegObject.save()
                    print("jkln####################################################")
                    reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                    print("reDtata",reDtata)
                    handleHindiTextQuery(response[0]['from'], reDtata,False)
                    ElseMoreHindi(response)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "cal_hemoglobin_level_wra_com"
                    checkRegObject.save()
                    reDtata = countingHBLevel(response[0]['msg_text'],"English")
                    handleHindiTextQuery(response[0]['from'], reDtata,False)
                    ElseMoreEnglish(response)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    # if checkRegObject.language=='Hindi':
                    #     AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                    # elif checkRegObject.language=='English':
                    #     AboutSomthingMore(response,response[0]['msg_text'],'English')
                    # else:
                    pass


            elif checkRegObject.reg_status == "REGISTRATION_COMPLETED" and  checkRegObject.reg_role=='Beneficiary':
                if checkRegObject.language=='Hindi':
                    AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                elif checkRegObject.language=='English':
                    AboutSomthingMore(response,response[0]['msg_text'],'English')
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

             # Section 4
            #################
            

            # Hindi  Beneficiary Registration End

           ###############################################################################################################################################################



            # Hindi ANM Registration Start
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_mobile"
                    checkRegObject.save()
                    beneData = RegANM(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं ",False)
                    # client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_mobile"
                    checkRegObject.save()
                    beneData = RegANM(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"Please enter the mobile number you want to register",False)
                    # client.sendMsgForConfirmation("you want to move from this number" + response[0]['from'],response[0]['from'],"Yes","No")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass
                # handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं ",False)



            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllStateName('Hindi')
                                }
                            ]

                        client.interactivte_reply_list(templateData,"कृपया अपने राज्य का चयन करें" ,response[0]['from'],"दबाएँ")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllStateName("English")
                                }
                            ]

                        client.interactivte_reply_list(templateData,"Which is you state name ?" ,response[0]['from'],"Click")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"Please enter a 10 digit number.",False)
                        handleHindiTextQuery(response[0]['from'],"enter your number",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"enter your number",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"कृपया अपने जिले का चयन करें",False)
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllDistrctNameByID('Hindi',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने जिले का चयन करें" ,response[0]['from'],"दबाएँ")
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllDistrctNameByID('English',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your district" ,response[0]['from'],"Click")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllBlocktNameByID('Hindi',beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने ब्लॉक का चयन करें" ,response[0]['from'],"दबाएँ")
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"what block are you from ?",False)
                    templateData = [
                                {
                                "title": "Please select one option",
                                "rows": getAllBlocktNameByID("English",beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your block" ,response[0]['from'],"दबाएँ")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_facility"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"आपके स्वास्थ्य केंद्र का नाम दर्ज करें",False)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_facility"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"What is the name of your health care facility?",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            # elif checkRegObject.current_stage=='What_is_your_facility' and checkRegObject.reg_role=='ANM':
            #     if checkRegObject.language=='Hindi':
            #         checkRegObject.current_stage = "What_is_your_id_number"
            #         checkRegObject.save()
            #         beneData = RegANM.objects.get(place=checkRegObject)
            #         beneData.facility_name = response[0]['msg_text']
            #         beneData.save()
            #         handleHindiTextQuery(response[0]['from'],"आईडी नंबर",False)
            #     elif checkRegObject.language=='English':
            #         checkRegObject.current_stage = "What_is_your_id_number"
            #         checkRegObject.save()
            #         beneData = RegANM.objects.get(place=checkRegObject)
            #         beneData.facility_name = response[0]['msg_text']
            #         beneData.save()
            #         handleHindiTextQuery(response[0]['from'],"ID Number",False)
            #     elif checkRegObject.language=='Gujrati':
            #         handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

            #     else:
            #         pass



            elif checkRegObject.current_stage=='What_is_your_facility' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "asking_for_confirmation"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.facility_name = response[0]['msg_text']
                    beneData.save()
                    beneregData = RegANM.objects.filter(place=checkRegObject)
                    datamsg = ''
                    print("************************************************************************")
                    print("beneregDatabeneregData",beneregData)
                    for ii in beneregData:
                        datamsg = "नाम: " + ii.name  +"\n" + "\n"+"मोबाइल नंबर: "+ ii.mobile_number +"\n"+"राज्य: "+ii.state +"\n"+"ज़िला: "+ ii.district +"\n"+"खंड: "+ ii.block +"\n"+"स्वास्थ्य केंद्र "+ ii.facility_name
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

                    handleHindiTextQuery(response[0]['from'], datamsg ,False)
                    client.interactivte_reply("क्या आप यह जानकारी जमा करना चाहते हैं?", response[0]['from'],returnYesHindi(),returnNoHindi())
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "asking_for_confirmation"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.facility_name = response[0]['msg_text']
                    beneData.save()
                    beneregData = RegANM.objects.filter(place=checkRegObject)
                    datamsg = ''
                    print("************************************************************************")
                    print("beneregDatabeneregData",beneregData)
                    for ii in beneregData:
                        datamsg = "Name: " + ii.name  +"\n"+"Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Facility Name: "+ ii.facility_name

                    handleHindiTextQuery(response[0]['from'], datamsg ,False)
                    client.interactivte_reply("Do you want to submit the form??", response[0]['from'],"Yes","No")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            elif checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "हमारे साथ पंजीकरण करने के लिए धन्यवाद।" ,False)

                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )
                        templateData = [
                                {
                                "title":  "एक विकल्प चुनें",
                                "rows": listData
                                }
                            ]

                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी हटा दी है, कृपया अपनी जानकारी फिर से डालें।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया जारी रखने के लिए कुछ लिखें।",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "Thank you for registering with us." ,False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")
                    elif response[0]['msg_text'] == "No":
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"We removed your information, please enter your information again.",False)
                        handleHindiTextQuery(response[0]['from'],"Please write something to continue.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass





            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            

            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage  in ['profile_submit_successfully','final_result'] and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == questionHindiMore('stock_est'):
                        checkRegObject.current_stage = "stock_calculation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"आपने चुना " + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)
                    elif response[0]['msg_text'] == questionHindiMore('demand_est'):
                        checkRegObject.current_stage = questionHindiMore('demand_est')
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"आपने चुना " + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार अनुमानित रूप  से आपके क्षेत्र में सालाना कितनी गर्भवती महिलाएं हैं?",False)

                    elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        
                    
                    elif response[0]['msg_text'] == questionHindiMore('cal_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        

                    elif response[0]['msg_text'] == questionHindiMore('health_food'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        

                    elif response[0]['msg_text'] == questionHindiMore('playGame'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')


                    else:
                        # handleHindiTextQuery(response[0]['from'],"कृपया कोई मान्य विकल्प चुनें.",False)
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == questionEnglishMore('stock_est'):
                        checkRegObject.current_stage = "stock_calculation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You selected" + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)
                    elif response[0]['msg_text'] == questionEnglishMore('demand_est'):
                        checkRegObject.current_stage = "demand_estimation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You selected" + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a annual as per your register ",False)

                    elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        
                    
                    elif response[0]['msg_text'] == questionHindiMore('cal_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        

                    elif response[0]['msg_text'] == questionHindiMore('health_food'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        

                    elif response[0]['msg_text'] == questionHindiMore('playGame'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')

                    else:
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            # STOCK CALCULATION
            ######################
            elif checkRegObject.current_stage=='stock_calculation' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)


                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)




                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='no_lactating_calculation' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक महीने में आपके क्षेत्र में प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)   
                
                
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "final_stock_cal"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)



                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass
                

          

            elif checkRegObject.current_stage=='no_lactating_wra' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं.",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock ",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='existing_stock' and checkRegObject.reg_role=='ANM':
                sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                if checkRegObject.language=='Hindi':
                    if sta == "TRUE":
                        print("KJBJKBJKBJK")
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 45
                        B = int(beneData.no_lactating_women) * 30
                        C = int(beneData.no_wra_women) * 4
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        
                        handleHindiTextQuery(response[0]['from'],"एनीमिया मुक्त भारत दिशानिर्देश के आधार पर आपके लिए आवश्यक मासिक स्टॉक " +str(estimated_cal_stk) + " है",False)
                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )
                        templateData = [
                                {
                                "title":  "एक विकल्प चुनें",
                                "rows": listData
                                }
                            ]

                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 45
                        B = int(beneData.no_lactating_women) * 30
                        C = int(beneData.no_wra_women) * 4
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        
                        handleHindiTextQuery(response[0]['from'],"Based on the Anemia Mukt bharat guideline the monthly stock required for you is " + str(estimated_cal_stk),False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass



                



            # Demand Calculation
            ###########################
            elif checkRegObject.current_stage=='demand_stock_calculation' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार अनुमानित रूप  से आपके क्षेत्र में सालाना कितनी गर्भवती महिलाएं हैं?",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार अनुमानित रूप  से आपके क्षेत्र में सालाना कितनी गर्भवती महिलाएं हैं?",False)


                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a annual as per your register",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a annual as per your register ",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a annual as per your register ",False)




                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='demand_no_lactating_calculation' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)   
                
                
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)



                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass
                

          

            elif checkRegObject.current_stage=='demand_no_lactating_wra' and checkRegObject.reg_role=='ANM':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_existing_stock"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_existing_stock"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock ",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a annual as per your register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a annual as per your register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='demand_existing_stock' and checkRegObject.reg_role=='ANM':
                sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                if checkRegObject.language=='Hindi':
                    if sta == "TRUE":
                        checkRegObject.current_stage = "final_result"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 270
                        B = int(beneData.no_lactating_women) * 180
                        C = int(beneData.no_wra_women) * 52
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"एनीमिया मुक्त भारत दिशानिर्देश के आधार पर आपके लिए आवश्यक वार्षिक स्टॉक " +str(estimated_cal_stk) + " है ",False)
                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )
                        templateData = [
                                {
                                "title":  "एक विकल्प चुनें",
                                "rows": listData
                                }
                            ]

                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")

                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegANM.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 270
                        B = int(beneData.no_lactating_women) * 180
                        C = int(beneData.no_wra_women) * 52
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"Based on the Anemia Mukt bharat guideline the annual stock required for you is " + str(estimated_cal_stk),False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass







            # Hindi ASHA Registration Start
           
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role =='ASHA':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_mobile"
                    checkRegObject.save()
                    beneData = RegASHA(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं ",False)
                    # client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())
                    pass
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_mobile"
                    checkRegObject.save()
                    beneData = RegASHA(place=checkRegObject,name=response[0]['msg_text'])
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"Please enter the mobile number you want to register ",False)
                    # client.sendMsgForConfirmation("You want to move on from this number " + response[0]['from'],response[0]['from'],"Yes","No")
                    pass
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


           


            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllStateName('Hindi')
                                }
                            ]

                        client.interactivte_reply_list(templateData,"कृपया अपने राज्य का चयन करें" ,response[0]['from'],"दबाएँ")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया वह मोबाइल नंबर दर्ज करें जिसे आप पंजीकृत करना चाहते हैं",False)
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "What_is_your_state"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.mobile_number = response[0]['msg_text']
                        beneData.save()
                        templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllStateName("English")
                                }
                            ]

                        client.interactivte_reply_list(templateData,"Please select your state" ,response[0]['from'],"Click")
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"Please enter a 10 digit number.",False)
                        handleHindiTextQuery(response[0]['from'],"enter your number",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"enter your number",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"कृपया अपने जिले का चयन करें",False)
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllDistrctNameByID('Hindi',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने जिले का चयन करें" ,response[0]['from'],"दबाएँ")

                    
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_district"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.state = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllDistrctNameByID('English',beneData.state)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your district" ,response[0]['from'],"Click")
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                                {
                                "title": "एक विकल्प चुनें",
                                "rows": getAllBlocktNameByID('Hindi',beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"कृपया अपने ब्लॉक का चयन करें" ,response[0]['from'],"दबाएँ")






                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_block"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.district = response[0]['msg_text']
                    beneData.save()
                    # handleHindiTextQuery(response[0]['from'],"Please select your block",False)
                    templateData = [
                                {
                                "title": "State Name",
                                "rows": getAllBlocktNameByID("English",beneData.state,beneData.district)
                                }
                            ]

                    client.interactivte_reply_list(templateData,"Please select your block" ,response[0]['from'],"Click")



                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_your_village"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"कृपया अपने गांव का नाम दर्ज करें",False)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_your_village"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.block = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"enter your village name",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    checkRegObject.current_stage = "What_is_village_population"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"आपके गांव की आबादी कितनी है",False)
                elif checkRegObject.language=='English':
                    checkRegObject.current_stage = "What_is_village_population"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    handleHindiTextQuery(response[0]['from'],"village population ??",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            elif checkRegObject.current_stage=='What_is_village_population' and checkRegObject.reg_role=='ASHA':
                print("kjbjbjbjibk")
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"POPULATION")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "asking_for_confirmation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.village_population = response[0]['msg_text']
                        beneData.save()
                        beneregData = RegASHA.objects.filter(place=checkRegObject)
                        datamsg = ''
                        for ii in beneregData:
                            datamsg = "नाम: " + ii.name  +"\n" + "\n"+"मोबाइल नंबर: "+ ii.mobile_number +"\n"+"राज्य: "+ii.state +"\n"+"ज़िला: "+ ii.district +"\n"+"खंड: "+ ii.block +"\n"+"गांव: "+ ii.village + "\n" +"गांव की आबादी: "+ ii.village_population

                        handleHindiTextQuery(response[0]['from'], datamsg ,False)
                        client.interactivte_reply("क्या आप यह जानकारी जमा करना चाहते हैं?", response[0]['from'],returnYesHindi(),returnNoHindi())
                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति है।",False)
                        handleHindiTextQuery(response[0]['from'],"आपके गांव की आबादी कितनी है",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके गांव की आबादी कितनी है",False)
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"POPULATION")
                    if sta == 'TRUE':
                        checkRegObject.current_stage = "asking_for_confirmation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.village_population = response[0]['msg_text']
                        beneData.save()
                        beneregData = RegASHA.objects.filter(place=checkRegObject)
                        datamsg = ''
                        for ii in beneregData:
                            datamsg = "Name: " + ii.name  +"\n"+ "Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Village: "+ ii.village + "\n" +"Village Population: "+ ii.village_population

                        handleHindiTextQuery(response[0]['from'], datamsg ,False)
                        client.interactivte_reply("Do you want to submit this information?", response[0]['from'],"Yes","No")

                    elif sta == 'DIGIT_ISSUE':
                        handleHindiTextQuery(response[0]['from'],"max  5 digit allowed.",False)
                        handleHindiTextQuery(response[0]['from'],"village population ??",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"village population ??",False)


                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass




            elif checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == returnYesHindi():
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "हमारे साथ पंजीकरण करने के लिए धन्यवाद।" ,False)
                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "एक विकल्प चुने",
                                "rows": listData
                                }
                            ]
                        # print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")
                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")

                    elif response[0]['msg_text'] == returnNoHindi():
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी हटा दी है, कृपया अपनी जानकारी फिर से डालें।",False)
                        handleHindiTextQuery(response[0]['from'],"कृपया जारी रखने के लिए कुछ लिखें।",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत डेटा दर्ज किया है, कृपया पुनः प्रयास करें",False)
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == "Yes":
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                        checkRegObject.save()
                        handleHindiTextQuery(response[0]['from'], "Thank you for registering with us." ,False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")

                    elif response[0]['msg_text'] == "No":
                        checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                        checkRegObject.delete()
                        handleHindiTextQuery(response[0]['from'],"We removed your information, please enter your information again.",False)
                        handleHindiTextQuery(response[0]['from'],"Please write something to continue.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"You have entered incorrect data, please try again",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass



            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage in ['profile_submit_successfully','final_result'] and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    if response[0]['msg_text'] == questionHindiMore('stock_est'):
                        checkRegObject.current_stage = "stock_calculation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"आपने चुना " + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)
                    elif response[0]['msg_text'] == questionHindiMore('demand_est'):
                        checkRegObject.current_stage = "demand_estimation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"आपने चुना " + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)

                    # Other Added
                    elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        
                    
                    elif response[0]['msg_text'] == questionHindiMore('cal_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        

                    elif response[0]['msg_text'] == questionHindiMore('health_food'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        

                    elif response[0]['msg_text'] == questionHindiMore('playGame'):
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                        


                    else:
                        # handleHindiTextQuery(response[0]['from'],"कृपया कोई मान्य विकल्प चुनें.",False)
                        AboutSomthingMore(response,response[0]['msg_text'],'Hindi')
                elif checkRegObject.language=='English':
                    if response[0]['msg_text'] == questionEnglishMore('stock_est'):
                        checkRegObject.current_stage = "stock_calculation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You selected" + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)
                    elif response[0]['msg_text'] == questionHindiMore('demand_est'):
                        checkRegObject.current_stage = "demand_estimation"
                        checkRegObject.save()
                        handleEnglishTextQuery(response[0]['from'],"You selected" + response[0]['msg_text'],False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)

                    elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        
                    
                    elif response[0]['msg_text'] == questionHindiMore('cal_info'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        

                    elif response[0]['msg_text'] == questionHindiMore('health_food'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                        

                    elif response[0]['msg_text'] == questionHindiMore('playGame'):
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                    else:
                        # handleHindiTextQuery(response[0]['from'],"Please select a valid option.",False)
                        AboutSomthingMore(response,response[0]['msg_text'],'English')
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)

                else:
                    pass


            # STOCK CALCULATION
            ######################
            elif checkRegObject.current_stage=='stock_calculation' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)


                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a month as per your register ",False)




                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='no_lactating_calculation' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक महीने में आपके क्षेत्र में प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं",False)   
                
                
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "final_stock_cal"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a month as per your register",False)



                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass
                

          

            elif checkRegObject.current_stage=='no_lactating_wra' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में 6 माह से कम शिशु वाली  कितनी महिलाएँ हैं.",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock ",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a month as per your register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='existing_stock' and checkRegObject.reg_role=='ASHA':
                sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                if checkRegObject.language=='Hindi':
                    if sta == "TRUE":
                        print("KJBJKBJKBJK")
                        checkRegObject.current_stage = "final_result"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 45
                        B = int(beneData.no_lactating_women) * 30
                        C = int(beneData.no_wra_women) * 4
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"एनीमिया मुक्त भारत दिशानिर्देश के आधार पर आपके लिए आवश्यक मासिक स्टॉक " +str(estimated_cal_stk) + " है",False)
                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )
                        templateData = [
                                {
                                "title":  "एक विकल्प चुनें",
                                "rows": listData
                                }
                            ]

                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"आपके रजिस्टर के अनुसार एक माह में आपके क्षेत्र में कितनी गर्भवती महिलाएं हैं.",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "existing_stock"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                     


                        A = int(beneData.no_pragnant_women) * 45
                        B = int(beneData.no_lactating_women) * 30
                        C = int(beneData.no_wra_women) * 4
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"Based on the Anemia Mukt bharat guideline the monthly stock required for you is " + str(estimated_cal_stk),False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")

                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass



                



            # Demand Calculation
            ###########################
            elif checkRegObject.current_stage=='demand_stock_calculation' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार अनुमानित रूप  से आपके क्षेत्र में सालाना कितनी गर्भवती महिलाएं हैं?",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार अनुमानित रूप  से आपके क्षेत्र में सालाना कितनी गर्भवती महिलाएं हैं?",False)


                    
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_PRAGNANT")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_calculation"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_pragnant_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a annual as per your register",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a annual as per your register ",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many pregnant women are there in your area in a annual as per your register ",False)




                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='demand_no_lactating_calculation' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में अनुमानित रूप से 6 महीने से कम शिशु वाली सालाना  कितनी महिलाएँ हैं",False)   
                
                
                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_LACTATING")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_no_lactating_wra"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_lactating_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a annual as per your register",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a annual as per your register",False)

                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women with infant less than 6 months are there in your area in a annual as per your register",False)



                    
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass
                

          

            elif checkRegObject.current_stage=='demand_no_lactating_wra' and checkRegObject.reg_role=='ASHA':
                if checkRegObject.language=='Hindi':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_existing_stock"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"एचएमआईएस लक्ष्य के अनुसार आपके क्षेत्र में सालाना  प्रजनन आयु वर्ग में कितनी महिलाएं हैं",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_WRA")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "demand_existing_stock"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.no_wra_women = response[0]['msg_text']
                        beneData.save()
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock ",False)
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a annual as per your register",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"How many women in reproductive age group are there in your area in a annual as per your register",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

            elif checkRegObject.current_stage=='demand_existing_stock' and checkRegObject.reg_role=='ASHA':
                sta = inputNumber(response[0]['msg_text'],"profile_submit_successfully")
                if checkRegObject.language=='Hindi':
                    if sta == "TRUE":
                        checkRegObject.current_stage = "final_result"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 270
                        B = int(beneData.no_lactating_women) * 180
                        C = int(beneData.no_wra_women) * 52
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"एनीमिया मुक्त भारत दिशानिर्देश के आधार पर आपके लिए आवश्यक वार्षिक स्टॉक " +str(estimated_cal_stk) + " है",False)
                        listData = []
                        for i in range(len(ElseMoreHindiHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreHindiHealthWorker()[i],
                                    "title": ElseMoreHindiHealthWorker()[i]
                                    }
                                )
                        templateData = [
                                {
                                "title":  "एक विकल्प चुनें",
                                "rows": listData
                                }
                            ]

                        client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                        
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"अधिकतम 5 अंकों की अनुमति",False)
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                        handleHindiTextQuery(response[0]['from'],"मौजूदा स्टॉक कितना है",False)

                elif checkRegObject.language=='English':
                    sta = inputNumber(response[0]['msg_text'],"NO_EXISTING_STCOK")
                    if sta == "TRUE":
                        checkRegObject.current_stage = "profile_submit_successfully"
                        checkRegObject.save()
                        beneData = RegASHA.objects.get(place=checkRegObject)
                        beneData.existing_stock = response[0]['msg_text']
                        beneData.save()
                        A = int(beneData.no_pragnant_women) * 270
                        B = int(beneData.no_lactating_women) * 180
                        C = int(beneData.no_wra_women) * 52
                        F = int(beneData.existing_stock)
                        R = A + B + C
                        R_E = R * 1.1
                        estimated_cal_stk = R_E - F
                        estimated_cal_stk = round(estimated_cal_stk)
                        handleHindiTextQuery(response[0]['from'],"Based on the Anemia Mukt bharat guideline the annual stock required for you is " + str(estimated_cal_stk),False)
                        listData = []
                        for i in range(len(ElseMoreEnglishHealthWorker())):
                            listData.append(
                                {
                                    "id": ElseMoreEnglishHealthWorker()[i],
                                    "title": ElseMoreEnglishHealthWorker()[i]
                                    }
                                )

                        print("listData",listData)
                        templateData = [
                                {
                                "title":  "Please select one option",
                                "rows": listData
                                }
                            ]
                        client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")
                    elif sta == "DIGIT_ISSUE":
                        handleHindiTextQuery(response[0]['from'],"max 5 digit allow",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                    else:
                        handleHindiTextQuery(response[0]['from'],"you have given wrong input",False)
                        handleHindiTextQuery(response[0]['from'],"how much is the exisiting stock",False)
                elif checkRegObject.language=='Gujrati':
                    handleGujratiTextQuery(response[0]['from'],"સ્વાગત ifa bot અમે તમારા માટે કામ કરી રહ્યા છીએ",False)
                else:
                    pass

          

    except ObjectDoesNotExist:
        print("Registration Process Start")
        resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
        resObject.save()
        handleHindiTextQuery(response[0]['from'],"नमस्ते, मैं रति हूं। मैं एक व्हाट्सएप चैटबॉट हूं जिसे एनीमिया और इससे संबंधित समस्याओं पर काबू पाने में आपकी सहायता करने के लिए डिज़ाइन किया गया है. एनीमिया भारत में एक प्रमुख सार्वजनिक स्वास्थ्य समस्या है जो व्यक्तियों के मानसिक और शारीरिक स्वास्थ्य को प्रभावित करती है। मैं एनीमिया और पोषण प्रबंधन के बारे में समझने और सीखने में आपकी सहायता करुंगी।",False)
        handleHindiTextQuery(response[0]['from'],"Hi, I am RATI. I am a WhatsApp chatbot designed to assist you with overcoming anemia and its related problems. Anemia is a major public health problem in India that impacts the mental and physical health of individuals. I will support you in understanding and learning about anemia and nutrition management.",False)
        response = client.send_media_msg("intro_rati","866097454686194", response[0]['from'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)


