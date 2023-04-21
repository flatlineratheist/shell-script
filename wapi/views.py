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
        username = request.GET.get("username",checkRegObject.language)
        return render(request,'index.html',{'username':username})
    except:
        return render(request,'404.html')


def redirectQuestion(request):
    try:
        username = request.GET.get("username",checkRegObject.language)
        id = request.GET.get("quetion_id",checkRegObject.language)
        q = request.GET.get("q",checkRegObject.language)
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
    # print("################$$$$$$$$$$$$$$$$$",checkRegObject.language)
    status = request.GET.get("status",checkRegObject.language)
    status_q = request.GET.get("changeLevel",checkRegObject.language)
    # print("SSSSSSSSS",status_q,type(status_q))
    showAnswer = 0

    if status == '0' or status == None:
        showAnswer = 0
    else:
        showAnswer = 1

    # print("################$$$$$$$$$$$$$$$$$",status)
    username = request.GET.get("username",checkRegObject.language)
    user = ''
    try:
        # print("ENter 1",checkRegObject.language)
        mob = WAPIRegistration.objects.get(reg_mobile=username)
        print('###################')
    except:
        # print("ENter 2",checkRegObject.language)
        mob = 'Anonymous'
    else:
        # print("ENter 3",checkRegObject.language)
        # print("########################################",checkRegObject.language)
        if mob != 'Anonymous':
            try:
                # print("Enter 4",checkRegObject.language)
                gameUser = WapiGameController.objects.get(place=mob)
                if status_q == '1':
                    gameUser.level = int(gameUser.level) + 1
                    gameUser.save()
                user = gameUser
            except:
                # print("Enter 5",checkRegObject.language)
                gameUser = WapiGameController(place=mob,level='1',total_score='0')
                gameUser.save()
                # print("kbjkkbkjb",gameUser.place.name)
                user = gameUser
        else:
            user = 'Anonymous'
    try:
        # print("gameUser.place.reg_mobile",gameUser.place.reg_mobile)
        # print("gameUser.level123  == ",gameUser.level,type(gameUser.level))
        question = WapiGame.objects.get(questionNo=str(gameUser.level))
        usernameUrl = gameUser.place.reg_mobile
        questionNo = gameUser.level
        # return render(request,'quiz.html',{'question':question,'user':user})

        redirectUrl = "https://ifabot.dev-tattvafoundation.org/question?username="+ usernameUrl+"&quetion_id="+str(questionNo)+"&q="+ str(showAnswer)
        # print("RRR",redirectUrl)
        return redirect(redirectUrl)
    except:
        return render(request,'404.html')



def wrong(request):
    try:
        username = request.GET.get("username",checkRegObject.language)
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
        username = request.GET.get("username",checkRegObject.language)
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
        username = request.GET.get("username",checkRegObject.language)
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
        # print("eval(request.body)[",eval(request.body)["template_name"])

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


def getQuestionFromText(questTextCode,lang="Hindi"):
    if lang == 'Hindi':
        import json
        f = open('./wapi/hindi_question.json')
        data = json.load(f)
        text = data[questTextCode]
        f.close()
        return text

    elif lang == 'English':
        import json
        f = open('./wapi/english_question.json')
        data = json.load(f)
        text = data[questTextCode]
        f.close()
        return text

    elif lang == 'Gujrati':
        import json
        f = open('./wapi/gujrati_question.json')
        data = json.load(f)
        text = data[questTextCode]
        f.close()
        return text
    else:
        pass






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
        if len(response) != 0:
            checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
            if response[0]['msg_text'] == 'del_user':
                checkRegObject = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                bkj = getQuestionFromText("remove_knowldege",checkRegObject.language)
                print("bkj",bkj)
                checkRegObject.delete()
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("remove_knowldege",checkRegObject.language),False)



            # User Identification
            ##################################
            ##################################
            elif checkRegObject.current_stage=='LANGUAGE_SETUP_PROCESS' and checkRegObject.reg_role=='NA' and checkRegObject.language=='NA':
                if response[0]['msg_text'] == returnHindi() and response[0]['msg_type'] == "interactive":
                    checkRegObject.language = 'Hindi'
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("langSelectHindi",checkRegObject.language),False)
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("registration_intro",checkRegObject.language),False)
                    templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pragnant_women",
                                        "title": getQuestionFromText("pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id": "chile_6_age",
                                        "title": getQuestionFromText("chile_6_age",checkRegObject.language)
                                    },
                                    {
                                        "id": "eligible_pragnant_women",
                                        "title": getQuestionFromText("eligible_pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id":"health_worker",
                                        "title":getQuestionFromText("health_worker",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()
                elif response[0]['msg_text'] == returnEnglish() and response[0]['msg_type'] == "interactive":
                    checkRegObject.language = 'English'
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("langSelectHindi",checkRegObject.language),False)
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("registration_intro",checkRegObject.language),False)
                    templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pragnant_women",
                                        "title": getQuestionFromText("pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id": "chile_6_age",
                                        "title": getQuestionFromText("chile_6_age",checkRegObject.language)
                                    },
                                    {
                                        "id": "eligible_pragnant_women",
                                        "title": getQuestionFromText("eligible_pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id":"health_worker",
                                        "title":getQuestionFromText("health_worker",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                    print("templateData",templateData)
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()
                elif response[0]['msg_text'] == returnGujrati() and response[0]['msg_type'] == "interactive":
                    checkRegObject.language = 'Gujrati'
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("langSelectHindi",checkRegObject.language),False)
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("registration_intro",checkRegObject.language),False)
                    templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pragnant_women",
                                        "title": getQuestionFromText("pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id": "chile_6_age",
                                        "title": getQuestionFromText("chile_6_age",checkRegObject.language)
                                    },
                                    {
                                        "id": "eligible_pragnant_women",
                                        "title": getQuestionFromText("eligible_pragnant_women",checkRegObject.language)
                                    },
                                    {
                                        "id":"health_worker",
                                        "title":getQuestionFromText("health_worker",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                    checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                    checkRegObject.save()

                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)




            # According To Selecting User 
            ##############################
            elif response[0]['msg_text'] == getQuestionFromText("pragnant_women",checkRegObject.language) and checkRegObject.current_stage == "LANGUAGE_SETUP_COMPLETE":
                if response[0]['msg_type'] == "interactive":
                    client.interactivte_reply(getQuestionFromText("who_pragnant",checkRegObject.language), response[0]['from'],getQuestionFromText("another",checkRegObject.language),getQuestionFromText("self",checkRegObject.language))
                    checkRegObject.current_stage = "pragnant_in_family"
                    checkRegObject.reg_role = "Beneficiary"
                    checkRegObject.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)
            
            
            elif response[0]['msg_text'] == getQuestionFromText("chile_6_age",checkRegObject.language) and checkRegObject.current_stage == "LANGUAGE_SETUP_COMPLETE":
                if response[0]['msg_type'] == "interactive":
                    client.interactivte_reply(getQuestionFromText("who_child_6",checkRegObject.language), response[0]['from'],getQuestionFromText("another",checkRegObject.language),getQuestionFromText("self",checkRegObject.language))
                    checkRegObject.current_stage = "family_in_child_6"
                    checkRegObject.reg_role = "Beneficiary"
                    checkRegObject.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)
            
            
            elif response[0]['msg_text'] == getQuestionFromText("eligible_pragnant_women",checkRegObject.language) and checkRegObject.current_stage == "LANGUAGE_SETUP_COMPLETE":
                if response[0]['msg_type'] == "interactive":
                    client.interactivte_reply(getQuestionFromText("eligible_pragent",checkRegObject.language), response[0]['from'],getQuestionFromText("another",checkRegObject.language),getQuestionFromText("self",checkRegObject.language))
                    checkRegObject.current_stage = "eligible_pragent"
                    checkRegObject.reg_role = "Beneficiary"
                    checkRegObject.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)
            
            
            elif response[0]['msg_text'] == getQuestionFromText("health_worker",checkRegObject.language) and checkRegObject.current_stage == "LANGUAGE_SETUP_COMPLETE":
                if response[0]['msg_type'] == "interactive":
                    pass
                    client.interactivte_reply(getQuestionFromText("who_hcw",checkRegObject.language), response[0]['from'],getQuestionFromText("asha",checkRegObject.language),getQuestionFromText("anm",checkRegObject.language))
                    checkRegObject.current_stage = "who_hcw"
                    checkRegObject.reg_role = "HCW"
                    checkRegObject.save()
                else:
                    pass
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)



   







##################################################################################################################################################################
######################################################## Pragnant Women In Family Start  #######################################################################################
##################################################################################################################################################################
       


            # Self Women Pragnant in Family
            #####################################
            elif response[0]['msg_text'] == getQuestionFromText("self",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "Beneficiary"  and checkRegObject.current_stage == "pragnant_in_family":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("congratulation_self_pragnant",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("month_of_pgranancy",checkRegObject.language),False)
                templateData = [
                    {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                               
                                    {
                                        "id": "second",
                                        "title": getQuestionFromText("second",checkRegObject.language)
                                    },
                                    {
                                        "id": "third",
                                        "title": getQuestionFromText("third",checkRegObject.language)
                                    },
                                    {
                                        "id":"fourth",
                                        "title":getQuestionFromText("fourth",checkRegObject.language)
                                    },
                                    {
                                        "id": "fifth",
                                        "title": getQuestionFromText("fifth",checkRegObject.language)
                                    },
                                    {
                                        "id": "sixth",
                                        "title": getQuestionFromText("sixth",checkRegObject.language)
                                    },
                                    {
                                        "id": "seventh",
                                        "title": getQuestionFromText("seventh",checkRegObject.language)
                                    },
                                    {
                                        "id":"eighth",
                                        "title":getQuestionFromText("eighth",checkRegObject.language)
                                    },
                                    {
                                        "id":"nineth",
                                        "title":getQuestionFromText("nineth",checkRegObject.language)
                                    },
                                    {
                                        "id":"more_nineth",
                                        "title":getQuestionFromText("more_nineth",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_month_pragnant_self"
                checkRegObject.save()
                
            elif response[0]['msg_text'] in getQuestionFromText("monthList",checkRegObject.language)  and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_month_pragnant_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "pragnant_in_family_name_self"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,pragnancy_month=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()

            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "pragnant_in_family_name_self":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "pragnant_in_family_district_self"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_district_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_block_self"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_block_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "pragnant_in_family_village_self"
                checkRegObject.save()
                
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "pragnant_in_family_village_self":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    # print(",checkRegObject.language))))))))))))))))))))))))")
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "pragnant_in_family_form_submit_self"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)


            # After Confirm Form Detail
            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_form_submit_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_self",checkRegObject.language), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_self"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                print("templateData",templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_no_self"
                checkRegObject.save()


                  ################# PURU ADDED CODE ################################################################
            elif response[0]['msg_text'] == getQuestionFromText("pargnancy_problem",checkRegObject.language) and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_yes":
                client.send_image_message( response[0]['from'],"3408723766109903")
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_yes"
                checkRegObject.reg_role = "Beneficiary"
                checkRegObject.save()

            # elif response[0]['msg_text'] == getQuestionFromText("chile_6_age",checkRegObject.language) and checkRegObject.current_stage == "LANGUAGE_SETUP_COMPLETE":
            #     if response[0]['msg_type'] == "interactive":
            #         client.interactivte_reply(getQuestionFromText("who_child_6",checkRegObject.language), response[0]['from'],getQuestionFromText("another",checkRegObject.language),getQuestionFromText("self",checkRegObject.language))
            #         checkRegObject.current_stage = "family_in_child_6"
            #         checkRegObject.reg_role = "Beneficiary"
            #         checkRegObject.save()
            #     else:
            #         handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_button_error",checkRegObject.language),False)
            



                 ##################################################################################################

            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_else_more_self"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                

            

            # After Reject Form Detail
            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_form_submit_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
                # print("============================")
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())
                



            # Another Women Pragnant in Family
            elif response[0]['msg_text'] == getQuestionFromText("another",checkRegObject.language) and response[0]['msg_type'] == "interactive"and checkRegObject.reg_role == "Beneficiary" and checkRegObject.current_stage == "pragnant_in_family":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("congratulation_another_pragnant",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("month_of_another_pgranancy",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                {
                                        "id": "second",
                                        "title": getQuestionFromText("second",checkRegObject.language)
                                    },
                                    {
                                        "id": "third",
                                        "title": getQuestionFromText("third",checkRegObject.language)
                                    },
                                    {
                                        "id":"fourth",
                                        "title":getQuestionFromText("fourth",checkRegObject.language)
                                    },
                                    {
                                        "id": "fifth",
                                        "title": getQuestionFromText("fifth",checkRegObject.language)
                                    },
                                    {
                                        "id": "sixth",
                                        "title": getQuestionFromText("sixth",checkRegObject.language)
                                    },
                                    {
                                        "id": "seventh",
                                        "title": getQuestionFromText("seventh",checkRegObject.language)
                                    },
                                    {
                                        "id":"eighth",
                                        "title":getQuestionFromText("eighth",checkRegObject.language)
                                    },
                                    {
                                        "id":"nineth",
                                        "title":getQuestionFromText("nineth",checkRegObject.language)
                                    },
                                    {
                                        "id":"more_nineth",
                                        "title":getQuestionFromText("more_nineth",checkRegObject.language)
                                    }
                                    
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_month_pragnant_another"
                checkRegObject.save()

####### Check for code (Puru)
            elif response[0]['msg_text'] in getQuestionFromText("monthList",checkRegObject.language)  and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_month_pragnant_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("another_user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "pragnant_in_family_name_another"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,pragnancy_month=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()

            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "pragnant_in_family_name_another":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_another_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "pragnant_in_family_district_another"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_district_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_another_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_block_another"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_block_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_another_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "pragnant_in_family_village_another"
                checkRegObject.save()
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "pragnant_in_family_village_another":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_another_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "pragnant_in_family_form_submit_another"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_form_submit_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_another",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_another"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_no_another"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_else_more_another"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                

            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_form_submit_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                # print("ojhjkhjkbkjl1256")
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
           
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())
       


##################################################################################################################################################################
######################################################## Pragnant Women In Family End  #######################################################################################
##################################################################################################################################################################








##################################################################################################################################################################
######################################################## Child Age 6 Start  #######################################################################################
##################################################################################################################################################################

            # Self
            ########
            elif response[0]['msg_text'] == getQuestionFromText("self",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "Beneficiary"  and checkRegObject.current_stage == "family_in_child_6":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("congratulation_self_child",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("self_child",checkRegObject.language),False)
                templateData = [
                    {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                               
                                    {
                                        "id": "first_month_child_less",
                                        "title": getQuestionFromText("first_month_child_less",checkRegObject.language)
                                    },
                                    {
                                        "id": "first_month_child",
                                        "title": getQuestionFromText("first_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"second_month_child",
                                        "title":getQuestionFromText("second_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "third_month_child",
                                        "title": getQuestionFromText("third_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "fourth_month_child",
                                        "title": getQuestionFromText("fourth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "fifth_month_child",
                                        "title": getQuestionFromText("fifth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"sixth_month_child",
                                        "title":getQuestionFromText("sixth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"sixth_more_month_child",
                                        "title":getQuestionFromText("sixth_more_month_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_month_self"
                checkRegObject.save()
                
            elif response[0]['msg_text'] in getQuestionFromText("child_age",checkRegObject.language)  and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_month_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "family_in_child_6_name_self"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,pragnancy_month=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()

            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "family_in_child_6_name_self":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "family_in_child_6_district_self"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)


            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_district_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_block_self"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_block_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "family_in_child_6_village_self"
                checkRegObject.save()
                
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "family_in_child_6_village_self":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "family_in_child_6_submit_form_self"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_submit_form_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_self",checkRegObject.language), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_self"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_no_self"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_else_more_self"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                



            #Reject Form
            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_submit_form_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
              
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())

                


                
                

            #Another
            ############
            elif response[0]['msg_text'] == getQuestionFromText("another",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "Beneficiary"  and checkRegObject.current_stage == "family_in_child_6":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("congratulation_another_child",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("another_child",checkRegObject.language),False)
                templateData = [
                    {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                               
                                    {
                                        "id": "first_month_child_less",
                                        "title": getQuestionFromText("first_month_child_less",checkRegObject.language)
                                    },
                                    {
                                        "id": "first_month_child",
                                        "title": getQuestionFromText("first_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"second_month_child",
                                        "title":getQuestionFromText("second_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "third_month_child",
                                        "title": getQuestionFromText("third_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "fourth_month_child",
                                        "title": getQuestionFromText("fourth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id": "fifth_month_child",
                                        "title": getQuestionFromText("fifth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"sixth_month_child",
                                        "title":getQuestionFromText("sixth_month_child",checkRegObject.language)
                                    },
                                    {
                                        "id":"sixth_more_month_child",
                                        "title":getQuestionFromText("sixth_more_month_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_month_another"
                checkRegObject.save()
                
            elif response[0]['msg_text'] in getQuestionFromText("child_age",checkRegObject.language)  and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_month_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("another_child_name",checkRegObject.language),False)
                checkRegObject.current_stage = "family_in_child_6_name_another"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,pragnancy_month=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()

            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "family_in_child_6_name_another":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "family_in_child_6_district_another"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_district_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_block_another"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_block_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "family_in_child_6_village_another"
                checkRegObject.save()
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "family_in_child_6_village_another":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_another_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "family_in_child_6_submit_form_another"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)


            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_submit_form_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_self",checkRegObject.language), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_self"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_beneficiary_problems_no_another"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "family_in_child_6_else_more_another"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))


            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "family_in_child_6_submit_form_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
              
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())


##################################################################################################################################################################
######################################################## Child Age 6 End  #######################################################################################
##################################################################################################################################################################



##################################################################################################################################################################
######################################################## Eligible Pragnant Start  #######################################################################################
##################################################################################################################################################################
            # Eligible Pragnant Self
            #############################
            elif response[0]['msg_text'] == getQuestionFromText("self",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "Beneficiary"  and checkRegObject.current_stage == "eligible_pragent":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("eligible_pragent_intro",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("eligible_pragent_self_age",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_self_age"
                checkRegObject.reg_role = "Beneficiary"
                checkRegObject.save()
                
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_self_age":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_self_name"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,age=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()



            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_self_name":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "eligible_pragent_self_district"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_self_district":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_self_block"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_self_block":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "eligible_pragent_self_village"
                checkRegObject.save()
                
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_self_village":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "eligible_pragent_form_submit_self"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_form_submit_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_self",checkRegObject.language), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_beneficiary_problems_self"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_self":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_beneficiary_problems_no_self"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_else_more_self"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_no_self":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                




            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_self_submit_form":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
            
            
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())
           
                

            # Another Eligible Pragnant
            ####################################
            elif response[0]['msg_text'] == getQuestionFromText("another",checkRegObject.language) and response[0]['msg_type'] == "interactive"and checkRegObject.reg_role == "Beneficiary" and checkRegObject.current_stage == "eligible_pragent":
               

                handleHindiTextQuery(response[0]['from'],getQuestionFromText("eligible_pragent_intro_another",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("eligible_pragent_another_age",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_another_age"
                checkRegObject.save()

            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_another_age":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("another_user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_another_name"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,age=response[0]['msg_text'],mobile_number=response[0]['from'])
                beneData.save()


            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_another_name":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_another_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "eligible_pragent_another_district"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.name = response[0]['msg_text']
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)


            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_another_district":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_another_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_another_block"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_another_block":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_another_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "eligible_pragent_another_village"
                checkRegObject.save()
                
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "eligible_pragent_another_village":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("confirmation_another_detail",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.pragnancy_month)
                    checkRegObject.current_stage = "eligible_pragent_form_submit_another"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_form_submit_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                client.interactivte_reply(getQuestionFromText("beneficiary_problems_self",checkRegObject.language), response[0]['from'],getQuestionFromText("yes_ok",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "pragnant_in_family_beneficiary_problems_another"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("yes_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "pragnant_in_family_beneficiary_problems_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("blood_test",checkRegObject.language),False)
                checkRegObject.current_stage = "eligible_pragent_beneficiary_problems_yes"
                checkRegObject.save()
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_another":
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                client.interactivte_reply(getQuestionFromText("blood_test_ok",checkRegObject.language).replace("{{1}}",beneData.name), response[0]['from'],getQuestionFromText("yes",checkRegObject.language),getQuestionFromText("no",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_beneficiary_problems_no_another"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("yes",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragancy_videos",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "eligible_pragent_else_more_another"
                checkRegObject.save()
                
                

            elif response[0]['msg_text'] == getQuestionFromText("no",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_beneficiary_problems_no_another":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_test",checkRegObject.language),False)
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("pragnancy_help",checkRegObject.language),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                

            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "eligible_pragent_another_submit_form":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())


##################################################################################################################################################################
######################################################## Eligible Pragnant End  #######################################################################################
##################################################################################################################################################################
            



    ############################################################################################################################################
    ############################################# Health Worker Start ##########################################################################
    ############################################################################################################################################

             # Health Worker {Self Or Another Having Child Age 6}
            # ASHA
            elif response[0]['msg_text'] == getQuestionFromText("asha",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "HCW"  and checkRegObject.current_stage == "who_hcw":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("stock_help",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "asha_name"
                checkRegObject.reg_role = "ASHA"
                checkRegObject.save()

                
            elif checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "asha_name":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "asha_district"
                    checkRegObject.save()
                    beneData = RegASHA(place=checkRegObject,name=response[0]['msg_text'],mobile_number=response[0]['from'])
                    beneData.save()
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "asha_district":
                
                beneData = RegASHA.objects.get(place=checkRegObject)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                # print("listBlock#######",listBlock)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":   getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "asha_block"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "asha_block":
                beneData = RegASHA.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("subcenter_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "asha_subcenter"
                checkRegObject.save()
                beneData.block = response[0]['msg_text']
                beneData.save()


            elif checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "asha_subcenter":
                beneData = RegASHA.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("village_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "asha_village"
                checkRegObject.save()
                beneData.facility_name = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "asha_village":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.village = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("asha_confirmation_text",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.village).replace("{{5}}",beneData.facility_name)
                    checkRegObject.current_stage = "asha_submit_form"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "asha_submit_form":
                beneData = RegASHA.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("else_more_text",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                {
                                        "id": "know_anemia",
                                        "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                    },
                                    {
                                        "id": "pragnant_women_care",
                                        "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                    },
                                    {
                                        "id":"child_women_less_6",
                                        "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                    },
                                    {
                                        "id": "stock_calculation",
                                        "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                    }
                                    # ,
                                    # {
                                    #     "id": "add_more_beneficiary",
                                    #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                    # }
                                    
                                ]
                        }
                    ]
                # print("templateData",templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "select_option_asha"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("know_anemia",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "blood_qty_issue",
                                        "title": getQuestionFromText("blood_qty_issue",checkRegObject.language)
                                    },
                                    {
                                        "id": "blood_qty_indentity_issue",
                                        "title": getQuestionFromText("blood_qty_indentity_issue",checkRegObject.language)
                                    },
                                    {
                                        "id": "blood_qty_effect_issue",
                                        "title": getQuestionFromText("blood_qty_effect_issue",checkRegObject.language)
                                    },
                                    {
                                        "id":"blood_qty_treatment",
                                        "title":getQuestionFromText("blood_qty_treatment",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                print("templateData",templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))

            elif response[0]['msg_text'] == getQuestionFromText("pragnant_women_care",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
                client.send_image_message( response[0]['from'],"3408723766109903")
                

            elif response[0]['msg_text'] == getQuestionFromText("child_women_less_6",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
                client.send_image_message( response[0]['from'],"2450978455052420")

            elif response[0]['msg_text'] == getQuestionFromText("stock_calculation",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
              
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("first_third_pranant_women_no",checkRegObject.language),False)
                checkRegObject.current_stage = "stock_calculation"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("add_more_beneficiary",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
                pass


            # Stock Calulation
            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("second_third_pranant_women_no",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_1"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.first_trimester = response[0]['msg_text']
                    beneData.save()
                    
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_1":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("less_than_child_6_women",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_2"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.second_third_trimester = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_2":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("lachit_dumpati",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_3"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.no_lactating_women = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_3":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_iron_mdeicine",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_4"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.lakshit_dumpati = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)
            
            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_4":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_calcium_mdeicine",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_5"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.no_ifa = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_5":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_folic_acid",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_6"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.no_cal = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            # Calculating Final Results (Monthly)
            ##########################################
            elif  checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_6":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "stock_calculation_7"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.no_folic_acid = response[0]['msg_text']
                    beneData.save()
                   
                   
                    # IFA Calculation
                    s1IFA = int(beneData.second_third_trimester) * 45
                    s2IFA = int(beneData.no_lactating_women) * 30
                    s3IFA = int(beneData.lakshit_dumpati) * 4
                    sumIFA = s1IFA + s2IFA + s3IFA
                    sumIFA = sumIFA * 1.1
                    sumIFA = str(round(sumIFA - int(beneData.no_ifa)))
                   

                    # Calcium Calculation
                    s1Cal = int(beneData.second_third_trimester) * 60
                    s2Cal = int(beneData.no_lactating_women) * 60
                    sumCal = s1Cal + s2Cal
                    sumCal = sumCal * 1.1
                    sumCal = str(round(sumCal - int(beneData.no_cal)))
                    



                    # Folic  Calculation
                    s1Folic = int(beneData.first_trimester) * 30
                    sumFolic = s1Folic * 1.1
                    sumFolic = str(round(sumFolic - int(beneData.no_folic_acid)))
                    
                    fnalR = getQuestionFromText("stock_cal_result",checkRegObject.language).replace("{{1}}",sumIFA).replace("{{2}}",sumCal).replace("{{3}}",sumFolic)

                    handleHindiTextQuery(response[0]['from'],fnalR,False)

                    time.sleep(3)

                    templateData = [
                            {
                                "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                                "rows": [
                                    {
                                            "id": "know_anemia",
                                            "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                        },
                                        {
                                            "id": "pragnant_women_care",
                                            "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                        },
                                        {
                                            "id":"child_women_less_6",
                                            "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                        },
                                        {
                                            "id": "stock_calculation",
                                            "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                        }
                                        # ,
                                        # {
                                        #     "id": "add_more_beneficiary",
                                        #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                        # }
                                        
                                    ]
                            }
                        ]
                    
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "select_option_asha"
                    checkRegObject.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)



            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "ASHA" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "asha_submit_form":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
               
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())


          
            # Health Worker
            # Anm
            elif response[0]['msg_text'] == getQuestionFromText("anm",checkRegObject.language) and response[0]['msg_type'] == "interactive" and checkRegObject.reg_role == "HCW"  and checkRegObject.current_stage == "who_hcw":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("stock_help",checkRegObject.language),False)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("user_name",checkRegObject.language),False)
                checkRegObject.current_stage = "anm_name"
                checkRegObject.reg_role = "ANM"
                checkRegObject.save()
                
                
            elif checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "anm_name":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_district",checkRegObject.language).replace("{{1}}",response[0]['msg_text']),False)
                    templateData = [
                        {
                                "title":   getQuestionFromText("select_one",checkRegObject.language),
                                 "rows": [
                                    {
                                        "id": getQuestionFromText("damoh",checkRegObject.language),
                                        "title": getQuestionFromText("damoh",checkRegObject.language)
                                    },
                                    {
                                        "id": getQuestionFromText("vadodra",checkRegObject.language),
                                        "title": getQuestionFromText("vadodra",checkRegObject.language)
                                    }
                                ]
                            }
                            ]

                            

                            

                    client.interactivte_reply_list(templateData,getQuestionFromText("select_district",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                    checkRegObject.current_stage = "anm_district"
                    checkRegObject.save()
                    beneData = RegANM(place=checkRegObject,name=response[0]['msg_text'],mobile_number=response[0]['from'])
                    beneData.save()
                    # print("========################===========",checkRegObject.language)
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)



            elif checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "anm_district":
                
                beneData = RegANM.objects.get(place=checkRegObject)
                # print("beneData",beneData)
                if response[0]['msg_text'] == getQuestionFromText("damoh",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("damoh",checkRegObject.language),
                                    "title": getQuestionFromText("damoh",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("tendukheda",checkRegObject.language),
                                    "title": getQuestionFromText("tendukheda",checkRegObject.language)
                                }
                            ]
                
                if response[0]['msg_text'] == getQuestionFromText("vadodra",checkRegObject.language):
                    listBlock = [
                                {
                                    "id": getQuestionFromText("vadodra",checkRegObject.language),
                                    "title": getQuestionFromText("vadodra",checkRegObject.language)
                                },
                                {
                                    "id": getQuestionFromText("savli",checkRegObject.language),
                                    "title": getQuestionFromText("savli",checkRegObject.language)
                                }
                            ]
                

                handleHindiTextQuery(response[0]['from'],getQuestionFromText("select_your_block",checkRegObject.language).replace("{{1}}",beneData.name),False)
                templateData = [
                    {
                            "title":  getQuestionFromText("select_one",checkRegObject.language),
                                "rows": listBlock
                        }
                        ]


                client.interactivte_reply_list(templateData,getQuestionFromText("select_block",checkRegObject.language) ,response[0]['from'],getQuestionFromText("click",checkRegObject.language))
                checkRegObject.current_stage = "anm_block"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "anm_block":
                beneData = RegANM.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("subcenter_name",checkRegObject.language).replace("{{1}}",beneData.name),False)
                checkRegObject.current_stage = "anm_subcenter"
                checkRegObject.save()
                
                beneData.block = response[0]['msg_text']
                beneData.save()
            
            
            elif checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "anm_subcenter":
                if response[0]['msg_text'].replace(" ","").isalpha():
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.facility_name = response[0]['msg_text']
                    beneData.save()
                    text = getQuestionFromText("anm_confirmation_text",checkRegObject.language).replace("{{1}}",beneData.name).replace("{{2}}",beneData.district).replace("{{3}}",beneData.block).replace("{{4}}",beneData.facility_name)
                    checkRegObject.current_stage = "anm_submit_form"
                    checkRegObject.save()
                    client.interactivte_reply(text, response[0]['from'],getQuestionFromText("form_data_ok",checkRegObject.language),getQuestionFromText("from_data_not_ok",checkRegObject.language))
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("validation_hindi_text",checkRegObject.language),False)

            elif response[0]['msg_text'] == getQuestionFromText("form_data_ok",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "anm_submit_form":
                beneData = RegANM.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("form_submit_successfully",checkRegObject.language),False)
               
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("else_more_text",checkRegObject.language).replace("{{1}}",beneData.name),False)
              

                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                {
                                        "id": "know_anemia",
                                        "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                    },
                                    {
                                        "id": "pragnant_women_care",
                                        "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                    },
                                    {
                                        "id":"child_women_less_6",
                                        "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                    },
                                    {
                                        "id": "stock_calculation",
                                        "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                    },
                                    {
                                        "id": "annual_stock_calculation",
                                        "title": getQuestionFromText("annual_stock_calculation",checkRegObject.language)
                                    }
                                    # ,
                                    # {
                                    #     "id": "add_more_beneficiary",
                                    #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                    # }
                                     
                                ]
                        }
                    ]
                # print("templateData",templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                checkRegObject.current_stage = "select_option_anm"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_COMPLETED"
                checkRegObject.save()


            elif response[0]['msg_text'] == getQuestionFromText("know_anemia",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_anm":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "blood_qty_issue",
                                        "title": getQuestionFromText("blood_qty_issue",checkRegObject.language) 
                                    },
                                    {
                                        "id": "blood_qty_indentity_issue",
                                        "title": getQuestionFromText("blood_qty_indentity_issue",checkRegObject.language)
                                    },
                                    {
                                        "id": "blood_qty_effect_issue",
                                        "title": getQuestionFromText("blood_qty_effect_issue",checkRegObject.language)
                                    },
                                    {
                                        "id":"blood_qty_treatment",
                                        "title":getQuestionFromText("blood_qty_treatment",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))

            elif response[0]['msg_text'] == getQuestionFromText("pragnant_women_care",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_anm":
                client.send_image_message( response[0]['from'],"3408723766109903")

            elif response[0]['msg_text'] == getQuestionFromText("child_women_less_6",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_anm":
                client.send_image_message( response[0]['from'],"2450978455052420")
                

            elif response[0]['msg_text'] == getQuestionFromText("stock_calculation",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_anm":
               
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("first_third_pranant_women_no",checkRegObject.language),False)
                checkRegObject.current_stage = "stock_calculation"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("annual_stock_calculation",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_anm":
               
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("annual_pragant_no",checkRegObject.language),False)
                checkRegObject.current_stage = "annual_stock_calculation"
                checkRegObject.save()

            elif response[0]['msg_text'] == getQuestionFromText("add_more_beneficiary",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "select_option_asha":
                pass


            # Stock Calulation Monthly
            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("second_third_pranant_women_no",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_1"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.first_trimester = response[0]['msg_text']
                    beneData.save()
                    # print("UUUUUUUUUUUUUUUUUUUUU",checkRegObject.language)
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)
                    

            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_1":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("less_than_child_6_women",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_2"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.second_third_trimester = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_2":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("lachit_dumpati",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_3"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.no_lactating_women = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_3":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_iron_mdeicine",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_4"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.lakshit_dumpati = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)
                
            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_4":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_calcium_mdeicine",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_5"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.no_ifa = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_5":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("no_folic_acid",checkRegObject.language),False)
                    checkRegObject.current_stage = "stock_calculation_6"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.no_cal = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)



            # Calculating Final Results (Monthly)
            ##########################################
            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "stock_calculation_6":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "stock_calculation_7"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.no_folic_acid = response[0]['msg_text']
                    beneData.save()
                    
                    # IFA Calculation
                    s1IFA = int(beneData.second_third_trimester) * 45
                    s2IFA = int(beneData.no_lactating_women) * 30
                    s3IFA = int(beneData.lakshit_dumpati) * 4
                    sumIFA = s1IFA + s2IFA + s3IFA
                    sumIFA = sumIFA * 1.1
                    sumIFA = str(round(sumIFA - int(beneData.no_ifa)))
                    

                    # Calcium Calculation
                    s1Cal = int(beneData.second_third_trimester) * 60
                    s2Cal = int(beneData.no_lactating_women) * 60
                    sumCal = s1Cal + s2Cal
                    sumCal = sumCal * 1.1
                    sumCal = str(round(sumCal - int(beneData.no_cal)))
                    



                    # Folic  Calculation
                    s1Folic = int(beneData.first_trimester) * 30
                    sumFolic = s1Folic * 1.1
                    sumFolic = str(round(sumFolic - int(beneData.no_folic_acid)))
                   



                    fnalR = getQuestionFromText("stock_cal_result",checkRegObject.language).replace("{{1}}",sumIFA).replace("{{2}}",sumCal).replace("{{3}}",sumFolic)

                    handleHindiTextQuery(response[0]['from'],fnalR,False)

                    time.sleep(5)

                    templateData = [
                            {
                                "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                                "rows": [
                                    {
                                            "id": "know_anemia",
                                            "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                        },
                                        {
                                            "id": "pragnant_women_care",
                                            "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                        },
                                        {
                                            "id":"child_women_less_6",
                                            "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                        },
                                        {
                                            "id": "stock_calculation",
                                            "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                        },
                                        {
                                            "id": "annual_stock_calculation",
                                            "title": getQuestionFromText("annual_stock_calculation",checkRegObject.language)
                                        }
                                        # ,
                                        # {
                                        #     "id": "add_more_beneficiary",
                                        #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                        # }
                                        
                                    ]
                            }
                        ]
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "select_option_anm"
                    checkRegObject.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)



            # Annual Stock Calulation Monthly
            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "annual_stock_calculation":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("annual_lcatating_no",checkRegObject.language),False)
                    checkRegObject.current_stage = "annual_stock_calculation_1"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.annual_pragnant_women = response[0]['msg_text']
                    beneData.save()
                   
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "annual_stock_calculation_1":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("annual_lakshit_no",checkRegObject.language),False)
                    checkRegObject.current_stage = "annual_stock_calculation_2"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.annual_lactating_women = response[0]['msg_text']
                    beneData.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)

          
            # Calculating Final Results (Monthly)
            ##########################################
            elif  checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "text" and checkRegObject.current_stage == "annual_stock_calculation_2":
                sta = inputNumber(response[0]['msg_text'],"POPULATION")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "annual_stock_calculation_7"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.annual_lakshit_women = response[0]['msg_text']
                    beneData.save()
                    

                    '''
                    IFA
                    [(Pregnant women in 2&3rd trimester*270)+(Lactating women*180)+Lakshit Dampati*52]*1.1
                    Calcium
                    [(Pregnant women in 2&3rd trimester*360)+(Lactating women*360)]*1.1
                    Folic Acid
                    (Pregnant women in 1st trimester*90)*1.1
                    '''



                    # IFA Calculation
                    s1IFA = int(beneData.annual_pragnant_women) * 270
                    s2IFA = int(beneData.annual_lactating_women) * 180
                    s3IFA = int(beneData.annual_lakshit_women) * 52
                    sumIFA = s1IFA + s2IFA + s3IFA
                    sumIFA = sumIFA * 1.1
                    sumIFA = str(round(sumIFA))
                    # print("==================1",checkRegObject.language)

                    # Calcium Calculation
                    s1Cal = int(beneData.annual_pragnant_women) * 360
                    s2Cal = int(beneData.annual_lactating_women) * 360
                    sumCal = s1Cal + s2Cal
                    sumCal = sumCal * 1.1
                    sumCal = str(round(sumCal))
                    # print("==================2",checkRegObject.language)



                    # Folic  Calculation
                    s1Folic = int(beneData.annual_pragnant_women) * 90
                    sumFolic = s1Folic * 1.1
                    sumFolic = str(round(sumFolic))
                    # print("==================3",checkRegObject.language)



                    fnalR = getQuestionFromText("annual_final_result",checkRegObject.language).replace("{{1}}",sumIFA).replace("{{2}}",sumCal).replace("{{3}}",sumFolic)

                    handleHindiTextQuery(response[0]['from'],fnalR,False)


                    time.sleep(5)

                    templateData = [
                            {
                                "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                                "rows": [
                                    {
                                            "id": "know_anemia",
                                            "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                        },
                                        {
                                            "id": "pragnant_women_care",
                                            "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                        },
                                        {
                                            "id":"child_women_less_6",
                                            "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                        },
                                        {
                                            "id": "stock_calculation",
                                            "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                        },
                                        {
                                            "id": "annual_stock_calculation",
                                            "title": getQuestionFromText("annual_stock_calculation",checkRegObject.language)
                                        }
                                        # ,
                                        # {
                                        #     "id": "add_more_beneficiary",
                                        #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                        # }
                                        
                                    ]
                            }
                        ]
                    # print("templateData",templateData)
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    checkRegObject.current_stage = "select_option_anm"
                    checkRegObject.save()
                elif sta =='DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("max_four_digit",checkRegObject.language),False)
                
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valueError_INT",checkRegObject.language),False)



            elif response[0]['msg_text'] == getQuestionFromText("from_data_not_ok",checkRegObject.language) and checkRegObject.reg_role == "ANM" and response[0]['msg_type'] == "interactive" and checkRegObject.current_stage == "anm_submit_form":
                handleHindiTextQuery(response[0]['from'],getQuestionFromText("from_submit_not_ok",checkRegObject.language),False)
                beneData = WAPIRegistration.objects.get(reg_mobile=response[0]['from'])
                beneData.delete()
                resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
                resObject.save()
               
                client.interactivte_reply_one_button(getQuestionFromText("intrro_question",checkRegObject.language), response[0]['from'],returnHindi())
            

############################################################################################################################################
############################################# Health Worker End ##########################################################################
############################################################################################################################################




############################################################################################################################################
############################################# Else More Need Start ##########################################################################
############################################################################################################################################
            elif response[0]['msg_text'] == getQuestionFromText("pargnancy_problem",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pragnancy_problem_1",
                                        "title": getQuestionFromText("pragnancy_problem_1",checkRegObject.language)
                                    },
                                    {
                                        "id": "pragnancy_problem_2",
                                        "title": getQuestionFromText("pragnancy_problem_2",checkRegObject.language)
                                    },
                                    {
                                        "id": "pragnancy_problem_3",
                                        "title": getQuestionFromText("pragnancy_problem_3",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                # print("templateData",templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
            
            
            elif response[0]['msg_text'] == getQuestionFromText("pargnancy_health",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "parg_health_prob_1",
                                        "title": getQuestionFromText("parg_health_prob_1",checkRegObject.language)
                                    },
                                    {
                                        "id": "parg_health_prob_2",
                                        "title": getQuestionFromText("parg_health_prob_2",checkRegObject.language)
                                    },
                                    {
                                        "id": "parg_health_prob_3",
                                        "title": getQuestionFromText("parg_health_prob_3",checkRegObject.language)
                                    },
                                    {
                                        "id":"parg_health_prob_4",
                                        "title":getQuestionFromText("parg_health_prob_4",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                print(templateData)
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
            
            
            elif response[0]['msg_text'] == getQuestionFromText("dadi_ke_nukhe",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"584888763696912")
            
            
            elif response[0]['msg_text'] == getQuestionFromText("pargnancy_action_child",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pragnancy_child_movement",
                                        "title": getQuestionFromText("pragnancy_child_movement",checkRegObject.language)
                                    },
                                    {
                                        "id": "pragnancy_child_develop_monthly",
                                        "title": getQuestionFromText("pragnancy_child_develop_monthly",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))

                
            # Option 1
            elif response[0]['msg_text'] == getQuestionFromText("pragnancy_problem_1",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"241922364922725")

            elif response[0]['msg_text'] == getQuestionFromText("pragnancy_problem_2",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"122768773990347")


            elif response[0]['msg_text'] == getQuestionFromText("pragnancy_problem_3",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"528225266135084")



            # Option 2
            elif response[0]['msg_text'] == getQuestionFromText("parg_health_prob_1",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "blood_qty_issue",
                                        "title": getQuestionFromText("blood_qty_issue",checkRegObject.language)
                                    },
                                    {
                                        "id": "blood_qty_indentity_issue",
                                        "title": getQuestionFromText("blood_qty_indentity_issue",checkRegObject.language)
                                    },
                                    {
                                        "id": "blood_qty_effect_issue",
                                        "title": getQuestionFromText("blood_qty_effect_issue",checkRegObject.language)
                                    },
                                    {
                                        "id":"blood_qty_treatment",
                                        "title":getQuestionFromText("blood_qty_treatment",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))

            elif response[0]['msg_text'] == getQuestionFromText("parg_health_prob_2",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_two",checkRegObject.language),response[0]['from'])


            elif response[0]['msg_text'] == getQuestionFromText("parg_health_prob_3",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "parg_health_prob_3f",
                                        "title": getQuestionFromText("parg_health_prob_3f",checkRegObject.language)
                                    },
                                    {
                                        "id": "iron_food",
                                        "title": getQuestionFromText("iron_food",checkRegObject.language)
                                    },
                                    {
                                        "id": "cal_food",
                                        "title": getQuestionFromText("cal_food",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))

            elif response[0]['msg_text'] == getQuestionFromText("parg_health_prob_4",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_one",checkRegObject.language),response[0]['from'])


            # Option 4
            elif response[0]['msg_text'] == getQuestionFromText("pragnancy_child_movement",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"758751415758055")

            elif response[0]['msg_text'] == getQuestionFromText("pragnancy_child_develop_monthly",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"740242837631061")



            # # Option 2.1.1
            elif response[0]['msg_text'] == getQuestionFromText("blood_qty_issue",checkRegObject.language) and checkRegObject.reg_role in ["Beneficiary","ASHA","ANM"] and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_three"),response[0]['from'])
            # # Option 2.1.2
            elif response[0]['msg_text'] == getQuestionFromText("blood_qty_indentity_issue",checkRegObject.language) and checkRegObject.reg_role in ["Beneficiary","ASHA","ANM"] and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"514389247563956")

            # # Option 2.1.3
            elif response[0]['msg_text'] == getQuestionFromText("blood_qty_effect_issue",checkRegObject.language) and checkRegObject.reg_role in ["Beneficiary","ASHA","ANM"] and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_four",checkRegObject.language),response[0]['from'])

            # # Option 2.1.4
            elif response[0]['msg_text'] == getQuestionFromText("blood_qty_treatment",checkRegObject.language) and checkRegObject.reg_role in ["Beneficiary","ASHA","ANM"] and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_five",checkRegObject.language),response[0]['from'])


            # # Option 2.3.1
            elif response[0]['msg_text'] == getQuestionFromText("parg_health_prob_3f",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_six",checkRegObject.language),response[0]['from'])

            # # Option 2.3.2
            elif response[0]['msg_text'] == getQuestionFromText("iron_food",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_image_message( response[0]['from'],"1548195309040794")

            # # Option 2.3.2
            elif response[0]['msg_text'] == getQuestionFromText("cal_food",checkRegObject.language) and checkRegObject.reg_role == "Beneficiary" and response[0]['msg_type'] == "interactive":
                client.send_media_url("👆" , getQuestionFromText("video_url_seven",checkRegObject.language),response[0]['from'])


############################################################################################################################################
############################################# Else More Need End ##########################################################################
############################################################################################################################################



            
            else:
                if checkRegObject.reg_status == "REGISTRATION_PROCESS_COMPLETED" and checkRegObject.reg_role == "Beneficiary":
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("ask_more",checkRegObject.language),False)
                    templateData = [
                        {
                            "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                            "rows": [
                                    {
                                        "id": "pargnancy_problem",
                                        "title": getQuestionFromText("pargnancy_problem",checkRegObject.language)
                                    },
                                    {
                                        "id": "pargnancy_health",
                                        "title": getQuestionFromText("pargnancy_health",checkRegObject.language)
                                    },
                                    {
                                        "id": "dadi_ke_nukhe",
                                        "title": getQuestionFromText("dadi_ke_nukhe",checkRegObject.language)
                                    },
                                    {
                                        "id":"pargnancy_action_child",
                                        "title":getQuestionFromText("pargnancy_action_child",checkRegObject.language)
                                    }
                                ]
                        }
                    ]
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                elif checkRegObject.reg_status == "REGISTRATION_PROCESS_COMPLETED" and checkRegObject.reg_role == "ANM":
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("ask_more",checkRegObject.language),False)
                    templateData = [
                            {
                                "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                                "rows": [
                                    {
                                            "id": "know_anemia",
                                            "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                        },
                                        {
                                            "id": "pragnant_women_care",
                                            "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                        },
                                        {
                                            "id":"child_women_less_6",
                                            "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                        },
                                        {
                                            "id": "stock_calculation",
                                            "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                        },
                                        {
                                            "id": "annual_stock_calculation",
                                            "title": getQuestionFromText("annual_stock_calculation",checkRegObject.language)
                                        }
                                        # ,
                                        # {
                                        #     "id": "add_more_beneficiary",
                                        #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                        # }
                                        
                                    ]
                            }
                        ]
                    # print("templateData",templateData)
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                elif checkRegObject.reg_status == "REGISTRATION_PROCESS_COMPLETED" and checkRegObject.reg_role == "ASHA":
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("ask_more",checkRegObject.language),False)
                    templateData = [
                            {
                                "title":  getQuestionFromText("select_one_option",checkRegObject.language),
                                "rows": [
                                    {
                                            "id": "know_anemia",
                                            "title": getQuestionFromText("know_anemia",checkRegObject.language)
                                        },
                                        {
                                            "id": "pragnant_women_care",
                                            "title": getQuestionFromText("pragnant_women_care",checkRegObject.language)
                                        },
                                        {
                                            "id":"child_women_less_6",
                                            "title":getQuestionFromText("child_women_less_6",checkRegObject.language)
                                        },
                                        {
                                            "id": "stock_calculation",
                                            "title": getQuestionFromText("stock_calculation",checkRegObject.language)
                                        }
                                        # ,
                                        # {
                                        #     "id": "add_more_beneficiary",
                                        #     "title": getQuestionFromText("add_more_beneficiary",checkRegObject.language)
                                        # }
                                        
                                    ]
                            }
                        ]
                    # print("templateData",templateData)
                    client.interactivte_reply_list(templateData,getQuestionFromText("select_one_option",checkRegObject.language),response[0]['from'],getQuestionFromText("select",checkRegObject.language))
                    
                else:
                    handleHindiTextQuery(response[0]['from'],getQuestionFromText("valid_entry_error",checkRegObject.language),False)

    except ObjectDoesNotExist:
        resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
        resObject.save()

        intro_text = getQuestionFromText("intrro_question","Hindi") + "\n \n" + getQuestionFromText("intrro_question","English") + "\n \n" + getQuestionFromText("intrro_question","Gujrati")
        print(intro_text)
        client.interactivte_reply_one_button(intro_text, response[0]['from'],returnHindi(),returnEnglish(),returnGujrati())
        # print("========================",checkRegObject.language)
        return Response({"status": "success"}, status=status.HTTP_200_OK)


