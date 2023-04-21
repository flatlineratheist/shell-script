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

        redirectUrl = "https://adityatattva.pythonanywhere.com/question?username="+ usernameUrl+"&quetion_id="+str(questionNo)+"&q="+ str(showAnswer)
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
            redirectUrl = "https://adityatattva.pythonanywhere.com/winner?username="+ username
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
            redirectUrl = "https://adityatattva.pythonanywhere.com/winner?username="+ username
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

def test(request):
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
        print("checkRegObject",checkRegObject)
        if checkRegObject:
            if response[0]['msg_text'] == 'ગુજરાતી' and checkRegObject.current_stage=='LANGUAGE_SETUP_PROCESS' and checkRegObject.reg_role=='NA' and checkRegObject.language=='NA' :
                checkRegObject.language = 'Gujrati'
                checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleGujratiTextQuery(response[0]['from'],"તમે ગુજરાતી ભાષા પસંદ કરી છે.",True)



            elif response[0]['msg_text'] == 'हिंदी'  and checkRegObject.current_stage=='LANGUAGE_SETUP_PROCESS' and checkRegObject.reg_role=='NA' and checkRegObject.language=='NA':
                checkRegObject.language = 'Hindi'
                checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],getLangText('select_lang_hindi'),True)


            elif response[0]['msg_text'] == 'English' and checkRegObject.current_stage=='LANGUAGE_SETUP_PROCESS' and checkRegObject.reg_role=='NA' and checkRegObject.language=='NA':
                checkRegObject.language = 'English'
                checkRegObject.current_stage = "LANGUAGE_SETUP_COMPLETE"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You have selected English Language.",True)






            # Hindi Language Setup
            # ################################
            #################################
            elif checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='NA' and checkRegObject.language=='Hindi':
                print("Comming 5 ###################################")
                if response[0]['msg_text'] == 'लाभार्थी':
                    checkRegObject.reg_role = 'Beneficiary'
                    checkRegObject.current_stage = "What_is_your_name"
                    checkRegObject.save()
                    handleHindiTextQuery(response[0]['from'],getLangText('bene_hindi'),False)
                    datatxt = getLangText('name_proceed_hindi')
                    # datatxt = "क्या आप {{1}} का नाम आगे बढ़ाना चाहते हैं ?"
                    datatxt = datatxt.replace('{{1}}',checkRegObject.name)
                    client.sendMsgForConfirmation(datatxt,response[0]['from'],returnYesHindi(),returnNoHindi())
                elif response[0]['msg_text'] == 'स्वास्थ्य कर्मी':
                    checkRegObject.reg_role = 'HCW'
                    checkRegObject.save()
                    handleHindiTextQuery(response[0]['from'],getLangText('hcw_hindi'),False)
                    client.send_media_msg("hwc_identification","724155319105458", response[0]['from'],'hi')
                else:
                    pass




            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_age"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,name=checkRegObject.name)
                beneData.save()
                handleHindiTextQuery(response[0]['from'],getLangText('q_age_hindi'),False)

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],getLangText('q_name_hindi'),False)




            elif response[0]['msg_text'] == 'एएनएम' and checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='HCW' and checkRegObject.language=='Hindi':
                print("Comming 6")
                checkRegObject.reg_role = 'ANM'
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आप एएनएम हैं",False)
                datatxt = "क्या आप {{1}} का नाम आगे बढ़ाना चाहते हैं ?"
                datatxt = datatxt.replace('{{1}}',checkRegObject.name)
                client.sendMsgForConfirmation(datatxt,response[0]['from'],returnYesHindi(),returnNoHindi())
                # handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)

            elif response[0]['msg_text'] == 'आशा' and checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='HCW' and checkRegObject.language=='Hindi':
                print("Comming 6")
                checkRegObject.reg_role = 'ASHA'
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आप आशा हैं",False)
                datatxt = "क्या आप {{1}} का नाम आगे बढ़ाना चाहते हैं ?"
                datatxt = datatxt.replace('{{1}}',checkRegObject.name)
                client.sendMsgForConfirmation(datatxt,response[0]['from'],returnYesHindi(),returnNoHindi())
                # handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)





            # Hindi Beneficiary Registration Start
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_age"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आपकी उम्र क्या हैं",False)


            elif checkRegObject.current_stage=='What_is_your_age' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                sta = inputNumber(response[0]['msg_text'],"AGE")
                if sta == "TRUE":
                    checkRegObject.current_stage = "What_is_your_mobile"
                    print("&UU&7777777777777777777777777777777777777777777777777777")
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.age = response[0]['msg_text']
                    beneData.save()
                    client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())
                elif sta == "AGE_LIMIT":
                    handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है,कृपया आयु 18 - 49 दर्ज करें",False)
                    handleHindiTextQuery(response[0]['from'],"आपकी उम्र क्या हैं",False)

                else:
                    handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                    handleHindiTextQuery(response[0]['from'],"आपकी उम्र क्या हैं",False)



            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],"हमने आपका नंबर पंजीकृत कर लिया है",False)
                beneData.mobile_number = response[0]['from']
                beneData.save()
                # handleHindiTextQuery(response[0]['from'],"आप किस राज्य के हैं",False)
                templateData = [
                        {
                          "title": "राज्य का नाम",
                          "rows": [
                            {
                              "id": "madhya_pradesh",
                              "title": "मध्य प्रदेश"
                            },
                            {
                              "id": "gujarat",
                              "title": "गुजरात"
                            }
                          ]
                        }
                      ]

                client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")




            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)




            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "What_is_your_state"
                    checkRegObject.save()
                    beneData = RegBeneficiary.objects.get(place=checkRegObject)
                    beneData.mobile_number = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                            {
                              "title": "राज्य का नाम",
                              "rows": [
                                {
                                  "id": "madhya_pradesh",
                                  "title": "मध्य प्रदेश"
                                },
                                {
                                  "id": "gujarat",
                                  "title": "गुजरात"
                                }
                              ]
                            }
                          ]

                    client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")
                elif sta == 'DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)
                else:
                    handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)







            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस जिले के हैं",False)



            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस ब्लॉक के हैं",False)


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_village"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"गांव का नाम",False)


            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_for_confirmation"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.village = response[0]['msg_text']
                beneData.save()
                beneregData = RegBeneficiary.objects.filter(place=checkRegObject)
                datamsg = ''
                print("beneregDatabeneregData",beneregData)
                for ii in beneregData:
                    datamsg = "नाम: " + ii.name  +"\n"+"आयु: "+ ii.age +"\n"+"मोबाइल नंबर: "+ ii.mobile_number +"\n"+"राज्य: "+ii.state +"\n"+"ज़िला: "+ ii.district +"\n"+"खंड: "+ ii.block +"\n"+"गांव: "+ ii.village
                handleHindiTextQuery(response[0]['from'], datamsg ,False)
                client.interactivte_reply("क्या आप फॉर्म जमा करना चाहते हैं ??", response[0]['from'],returnYesHindi(),returnNoHindi())


            elif response[0]['msg_text'] == returnYesHindi()  and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'], "आपका पंजीकरण सफलतापूर्वक पूरा हुआ।" ,False)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": [
                            {
                              "id": "currently_pragnant",
                              "title": "इस समय गर्भवती"
                            },
                            {
                              "id": "child_age_6",
                              "title": "शिशु 6 महीने से कम"
                            },
                            {
                              "id": "reproductive_women",
                              "title": "प्रजनन आयु समूह"
                            }
                          ]
                        }
                      ]

                # client.send__msg_button_without_media("beneficiary_identification", response[0]['from'],'hi') Template Disbale
                client.interactivte_reply_list(templateData,"इनमें से एक विकल्प चुनें",response[0]['from'],"चुनें")


                print("=================@@@@@@@@@@@=======================")

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी हटा दी है, कृपया अपनी जानकारी फिर से डालें।",False)
                handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)





            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                handleEnglishTextQuery(response[0]['from'],"आपने चुना  " + response[0]['msg_text'],False)
                if response[0]['msg_text'] ==  "इस समय गर्भवती":
                    checkRegObject.current_stage = "question_topic_selection_pragnant"
                    checkRegObject.save()
                    client.interactivte_reply("क्या आपके पास आरसीएच नंबर है", response[0]['from'],returnYesHindi(),returnNoHindi())
                    # client.send_media_msg("beneficiary_profile","3347506832153472", response[0]['from'],'hi')

                elif response[0]['msg_text'] == "शिशु 6 महीने से कम":
                    checkRegObject.current_stage = "question_topic_selection_lacting"
                    checkRegObject.save()
                    client.interactivte_reply("क्या आपके पास आरसीएच नंबर है", response[0]['from'],returnYesHindi(),returnNoHindi())

                elif response[0]['msg_text'] ==  "प्रजनन आयु समूह":
                    checkRegObject.current_stage = "question_topic_selection_wra"
                    checkRegObject.save()
                    client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())
                else:
                    handleHindiTextQuery(response[0]['from'],"कृपया मान्य विकल्प चुनें",False)


            ##################################################################################
            #########################################  Pragnant ##############################
            ##################################################################################
            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='question_topic_selection_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_rch_number_pragnant"
                checkRegObject.save()
                client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'hi')

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='question_topic_selection_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_rch_number_na_pragnant"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.rch_number = "NA"
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"यदि आपने अपना एएनसी कार्ड पंजीकृत नहीं किया है या खो दिया है तो कृपया अपनी आशा या एएनएम से संपर्क करें",False)
                handleHindiTextQuery(response[0]['from'],"अंतिम मासिक तिथि कब थी,  उदाहरण के लिए 05/10/2022",False)



            elif checkRegObject.current_stage=='asking_rch_number_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "enter_menstrual_date_pragnant"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.rch_number = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"अंतिम मासिक तिथि कब थी उदाहरण के लिए 05/10/2022",False)

            elif checkRegObject.current_stage=='asking_rch_number_na_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':

                try:
                    from datetime import datetime
                    date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                except ValueError as err:
                    handleHindiTextQuery(response[0]['from'],"दिनांक प्रारूप dd/mm/yy होना चाहिए, उदाहरण के लिए 05/10/2022",False)
                    handleHindiTextQuery(response[0]['from'],"अंतिम मासिक तिथि कब थी,  उदाहरण के लिए 05/10/2022",False)
                else:
                    checkRegObject.current_stage = "cal_menstrual_date_pragnant"
                    checkRegObject.save()
                    from datetime import date
                    from dateutil.relativedelta import relativedelta
                    new_date = date_object + relativedelta(months=9,days=7)
                    print("new_date",new_date)
                    new_date = new_date.strftime("%d/%m/%Y")
                    handleHindiTextQuery(response[0]['from'],"आपकी डिलीवरी की तारीख  "+    str(new_date)  +" आप अपनी -  "   +calculateTrimester(response[0]['msg_text'],"Hindi")+" में हैं",False)
                    client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())


            # Reply By Bot
            elif checkRegObject.current_stage=='enter_menstrual_date_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                try:
                    from datetime import datetime
                    date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                    import datetime
                    today = datetime.date.today()
                    year = today.year
                except ValueError as err:
                    handleHindiTextQuery(response[0]['from'],"दिनांक प्रारूप dd/mm/yy होना चाहिए, उदाहरण के लिए 05/10/2022",False)
                    handleHindiTextQuery(response[0]['from'],"अंतिम मासिक तिथि कब थी,  उदाहरण के लिए 05/10/2022",False)

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
                        client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत समय अवधि दर्ज की है",False)
                        handleHindiTextQuery(response[0]['from'],"अंतिम मासिक तिथि कब थी ,  उदाहरण के लिए 05/10/2022",False)




            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='cal_menstrual_date_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_pragnant"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है",False)

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='cal_menstrual_date_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "know_more_and_no_hb_pragnant"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                listData = []
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")



            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='check_reminder_to_visithb_checkup_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_pragnant"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है",False)


            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='check_reminder_to_visithb_checkup_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "not_visit_center_and_asking_question_pragnant"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                listData = []
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")





            elif response[0]['msg_text'] == questionHindiMore("qa") and checkRegObject.current_stage=='know_more_and_no_hb_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('anemia_info') and checkRegObject.current_stage=='know_more_and_no_hb_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('health_food') and checkRegObject.current_stage=='know_more_and_no_hb_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('cal_info') and checkRegObject.current_stage=='know_more_and_no_hb_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('playGame') and checkRegObject.current_stage=='know_more_and_no_hb_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])


            elif checkRegObject.current_stage=='cal_hemoglobin_level_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hb_levelknow_more_pragnant"
                checkRegObject.save()
                reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                handleHindiTextQuery(response[0]['from'], reDtata,False)
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें  👆" , "https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
                print("ERERRRFFFFFFFFFFFFF")
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")




            elif response[0]['msg_text'] == questionHindiMore("qa") and checkRegObject.current_stage=='cal_hb_levelknow_more_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें 👆" ,"https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('anemia_info') and checkRegObject.current_stage=='cal_hb_levelknow_more_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('health_food') and checkRegObject.current_stage=='cal_hb_levelknow_more_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('cal_info') and checkRegObject.current_stage=='cal_hb_levelknow_more_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])
            elif response[0]['msg_text'] == questionHindiMore('playGame') and checkRegObject.current_stage=='cal_hb_levelknow_more_pragnant' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_media_url("एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])



            ######################################################
            ########### Condtion For All Type Query ##############
            ######################################################

            elif checkRegObject.reg_status=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_pragnant"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है",False)








            # Schedule Message Section For Animic
            #############################################

            # Section 1
            #################
            elif response[0]['msg_text'] == "ifa_tablet_take_or_not" and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "ifa_tablet_take_or_not_reply"
                checkRegObject.save()
                scheduleMessage_pragnant("ifa_tablet_take_or_not",response)


            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='ifa_tablet_take_or_not_reply'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                checkRegObject.save()
                client.send_image_message( response[0]['from'],"583006833411655")
                time.sleep(1)
                client.interactivte_reply("क्या आयरन की गोलियां लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य",response[0]['from'],returnYesHindi(),returnNoHindi())

            elif response[0]['msg_text'] == returnNoHindi()  and checkRegObject.current_stage=='ifa_tablet_take_or_not_reply'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                checkRegObject.save()
                client.interactivte_reply("क्या आयरन की गोलियां लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य",response[0]['from'],returnYesHindi(),returnNoHindi())


            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='ifa_tablet_take_or_not_reply_yes'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "complete_msg"
                checkRegObject.save()
                # client.send_image_message( response[0]['from'],"2046604365730653")
                client.send_media_url("आयरन की गोलियों के बारे में जानने के लिए क्लिक करें","https://www.youtube.com/watch?v=I1snaZw45zU",response[0]['from'])
                # handleHindiTextQuery(response[0]['from'],"जल्द से जल्द अपने नजदीकी स्वास्थ्य केंद्र पर जाएं और जांच कराएं !!",False)

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='ifa_tablet_take_or_not_reply_yes'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "complete_msg"
                checkRegObject.save()
                client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up


            # Section 2
            #################
            elif response[0]['msg_text'] == "do_not_forget_iron_tablet" and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "complete_msg"
                checkRegObject.save()
                scheduleMessage_pragnant("do_not_forget_iron_tablet",response)


             # Section 3  Health Checkup
            ###############################
            elif response[0]['msg_text'] == "did_you_complete_health_checkup" and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "did_you_complete_health_checkup_or_not_reply"
                checkRegObject.save()
                scheduleMessage_pragnant("did_you_complete_health_checkup",response)


            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='did_you_complete_health_checkup_or_not_reply'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "ifa_tablet_take_or_not_reply_yes"
                checkRegObject.save()
                client.send_image_message( response[0]['from'],"583006833411655")  #Thumb Up
            elif response[0]['msg_text'] == returnNoHindi()  and checkRegObject.current_stage=='did_you_complete_health_checkup_or_not_reply'  and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "complete_msg"
                checkRegObject.save()
                scheduleMessage_pragnant("go_quick_health_checkup",response)
                client.send_media_url("क्लिक ","https://youtu.be/5qtdVD83vL8",response[0]['from'])




              # Section 3  Calcium Take Or Not Checkup
            ##################################
            elif response[0]['msg_text'] == "calcium_medicine_take" and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                # checkRegObject.current_stage = "calcium_medicine_take"
                # checkRegObject.save()
                scheduleMessage_pragnant("iromMdecine",response)






















             # Section 4
            #################
            elif response[0]['msg_text']  =='do_you_know_something_more' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                print("ERERRRFFFFFFFFFFFFF")
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")




             # Section 5
            #################
            elif checkRegObject.reg_status == "REGISTRATION_COMPLETED" and  checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                if response[0]['msg_text'] == "SEND_GAME_LINK":
                    client.send_media_url("आओ खेले","https://adityatattva.pythonanywhere.com?username="+response[0]['from'],response[0]['from'])

                elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                    listData = []
                    for i in range(len(what_do_you_want_animia_hindi())):
                        listData.append(
                            {
                                "id": what_do_you_want_animia_hindi()[i],
                                  "title": what_do_you_want_animia_hindi()[i]
                                }
                            )

                    print("listData",listData)
                    templateData = [
                            {
                              "title":  "एक विकल्प चुने",
                              "rows": listData
                            }
                          ]
                    client.interactivte_reply_list(templateData,"एनीमिया के बारे में",response[0]['from'],"चुनें")
                elif response[0]['msg_text'] == questionHindiMore('anemia_info'):
                    listData = []
                    for i in range(len(what_do_you_want_cal_hindi())):
                        listData.append(
                            {
                                "id": what_do_you_want_cal_hindi()[i],
                                  "title": what_do_you_want_cal_hindi()[i]
                                }
                            )

                    print("listData",listData)
                    templateData = [
                            {
                              "title":  "एक विकल्प चुने",
                              "rows": listData
                            }
                          ]
                    client.interactivte_reply_list(templateData,"कैल्शियम के बारे में",response[0]['from'],"चुनें")

                elif response[0]['msg_text'] == questionHindiMore('cal_info'):
                    client.send_document_message(response[0]['from'],"1131182871608893","स्वस्थ भोजन सूची","healthy_food")

                elif response[0]['msg_text'] == questionHindiMore('playGame'):
                    client.send_media_url("आओ खेले","https://adityatattva.pythonanywhere.com?username="+response[0]['from'],response[0]['from'])

                elif response[0]['msg_text'] == questionHindiCalMore('cal_need'):
                    client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiCalMore('cal_good_resource'):
                    client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiCalMore('cal_medicine_take'):
                    client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiCalMore('other'):
                    client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
                    handleHindiTextQuery(response[0]['from'],"अधिक जानकारी के लिए कृपया अपनी आशा दीदी या एएनएम से संपर्क करें",False)

                elif response[0]['msg_text'] == questionHindiAnimiaMore('what_animia'):
                    client.send_media_url("एनीमिया क्या है","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])

                elif response[0]['msg_text'] == questionHindiAnimiaMore('animia_def'):
                    client.send_image_message( response[0]['from'],"1260219784852086")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiAnimiaMore('animia_effect'):
                    client.send_media_url("एनीमिया का प्रभाव","https://www.youtube.com/watch?v=IUTob1tMdck",response[0]['from'])

                elif response[0]['msg_text'] == questionHindiAnimiaMore('animia_do_not'):
                    client.send_image_message( response[0]['from'],"959279025480160")  #Thumb Up


                elif response[0]['msg_text'] == questionHindiAnimiaMore('iron_food'):
                    client.send_image_message( response[0]['from'],"664704058742018")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiAnimiaMore('iron_tablet_info'):
                    client.send_image_message( response[0]['from'],"1037169314353036")  #Thumb Up

                elif response[0]['msg_text'] == questionHindiAnimiaMore('iron_tablet_sol'):
                    client.send_media_url("एनीमिया की रोकथाम और उपचार ", "https://youtu.be/Cz6yhxJg5OA",response[0]['from'])

                elif response[0]['msg_text'] == questionHindiAnimiaMore('other'):
                    client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
                    handleHindiTextQuery(response[0]['from'],"अधिक जानकारी के लिए कृपया अपनी आशा दीदी या एएनएम से संपर्क करें",False)







                else:
                    print("ERERRRFFFFFFFFFFFFF")
                    checkRegObject.current_stage = "do_you_know_reply_status"
                    checkRegObject.save()
                    listData = []
                    print("RRRRRRRRRRRRRR")
                    for i in range(len(what_do_you_want_else_hindi())):
                        listData.append(
                            {
                                "id": what_do_you_want_else_hindi()[i],
                                  "title": what_do_you_want_else_hindi()[i]
                                }
                            )

                    print("listData",listData)
                    templateData = [
                            {
                              "title":  "एक विकल्प चुने",
                              "rows": listData
                            }
                          ]
                    client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")






            ##################################################################################
            #########################################  Lactating ##############################
            ##################################################################################

            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='question_topic_selection_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_rch_number_lacting"
                checkRegObject.save()
                client.send_media_msg("beneficiary_profile","903952143978601", response[0]['from'],'hi')

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='question_topic_selection_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_rch_number_lacting"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.rch_number = "NA"
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"यदि आपने अपना एएनसी कार्ड पंजीकृत नहीं किया है या खो दिया है तो कृपया अपनी आशा या एएनएम से संपर्क करें",False)
                handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक,  उदाहरण के लिए 05/10/2022",False)



            elif checkRegObject.current_stage=='asking_rch_number_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "enter_child_date_lacting"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.rch_number = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक उदाहरण के लिए 05/10/2022",False)





            elif checkRegObject.current_stage=='enter_child_date_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
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
                            client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())

                        if reD == 'B_6':
                            checkRegObject.current_stage = "child_before_6"
                            checkRegObject.save()
                            handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने से कम है।",False)
                        if reD == 'E_6':
                            handleHindiTextQuery(response[0]['from'],"आपका बच्चा 6 महीने का है।",False)
                            client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())
                    else:
                        handleHindiTextQuery(response[0]['from'],"आपने गलत समय अवधि दर्ज की है",False)
                        handleHindiTextQuery(response[0]['from'],"शिशु के जन्म की तारिक उदाहरण के लिए 05/10/2022",False)




            #########################################################
            ############ Child After 6 Question #######################
            ###########################################################

            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='child_after_6' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_lacting"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है",False)

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='child_after_6' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "know_more_and_no_hb_lacting"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")





            elif checkRegObject.current_stage=='cal_hemoglobin_level_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_amt_lacting"
                checkRegObject.save()
                reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                handleHindiTextQuery(response[0]['from'], reDtata,False)
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")



            #########################################################
            ############ Child Before 6 Question #######################
            ###########################################################

            elif checkRegObject.current_stage=='child_before_6' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "child_before_6_level_lacting"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!!",False)
                client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],returnYesHindi(),returnNoHindi())


            elif  response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='child_before_6_level_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                client.send_image_message( response[0]['from'],"583006833411655")
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")

            elif  response[0]['msg_text'] == returnNoHindi() and  checkRegObject.current_stage=='child_before_6_level_lacting' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")
































        ##################################################################################
        #########################################  WRA ##############################
        ##################################################################################



            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='question_topic_selection_wra' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "cal_hemoglobin_level_wra"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"आपके शरीर में कितने प्वाइंट खून है",False)

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='question_topic_selection_wra' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                # checkRegObject.current_stage = "cal_hb_levelknow_more_wra"
                # checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"कृपया अपनी नजदीकी आशा या एएनएम से मिलें और अपना हीमोग्लोबिन स्तर जांचें",False)
                print("ERERRRFFFFFFFFFFFFF")
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")

            elif checkRegObject.current_stage=='cal_hemoglobin_level_wra' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='Hindi':
                # checkRegObject.current_stage = "cal_hb_levelknow_more_wra"
                # checkRegObject.save()
                reDtata = countingHBLevel(response[0]['msg_text'],"Hindi")
                handleHindiTextQuery(response[0]['from'], reDtata,False)
                print("ERERRRFFFFFFFFFFFFF")
                checkRegObject.current_stage = "do_you_know_reply_status"
                checkRegObject.save()
                listData = []
                print("RRRRRRRRRRRRRR")
                for i in range(len(what_do_you_want_else_hindi())):
                    listData.append(
                        {
                            "id": what_do_you_want_else_hindi()[i],
                              "title": what_do_you_want_else_hindi()[i]
                            }
                        )

                print("listData",listData)
                templateData = [
                        {
                          "title":  "एक विकल्प चुने",
                          "rows": listData
                        }
                      ]
                client.interactivte_reply_list(templateData,"क्या आप कुछ पूछना चाहते हैं?",response[0]['from'],"चुनें")










            # Hindi  Beneficiary Registration End

           ###############################################################################################################################################################



            # Hindi ANM Registration Start

            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegANM(place=checkRegObject,name=checkRegObject.name)
                beneData.save()
                client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())


            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)



            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegANM(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())
                # handleHindiTextQuery(response[0]['from'],"कृपया अपना फोन नम्बर दर्ज ",False)



            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],"हमने आपका नंबर पंजीकृत कर लिया है",False)
                beneData.mobile_number = response[0]['from']
                beneData.save()
                # handleHindiTextQuery(response[0]['from'],"आप किस राज्य के हैं",False)
                templateData = [
                        {
                          "title": "राज्य का नाम",
                          "rows": [
                            {
                              "id": "madhya_pradesh",
                              "title": "मध्य प्रदेश"
                            },
                            {
                              "id": "gujarat",
                              "title": "गुजरात"
                            }
                          ]
                        }
                      ]

                client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")




            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)



            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "What_is_your_state"
                    checkRegObject.save()
                    beneData = RegANM.objects.get(place=checkRegObject)
                    beneData.mobile_number = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                            {
                              "title": "राज्य का नाम",
                              "rows": [
                                {
                                  "id": "madhya_pradesh",
                                  "title": "मध्य प्रदेश"
                                },
                                {
                                  "id": "gujarat",
                                  "title": "गुजरात"
                                }
                              ]
                            }
                          ]

                    client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")
                elif sta == 'DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)
                else:
                    handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)

            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस जिले के हैं",False)

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस ब्लॉक के हैं",False)


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_facility"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"स्वास्थ्य केंद्र का नाम",False)

            elif checkRegObject.current_stage=='What_is_your_facility' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_id_number"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.facility_name = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आईडी नंबर",False)



            elif checkRegObject.current_stage=='What_is_your_id_number' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "asking_for_confirmation"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.id_number = response[0]['msg_text']
                beneData.save()
                beneregData = RegANM.objects.filter(place=checkRegObject)
                datamsg = ''
                print("************************************************************************")
                print("beneregDatabeneregData",beneregData)
                for ii in beneregData:
                    datamsg = "नाम: " + ii.name  +"\n" + "\n"+"मोबाइल नंबर: "+ ii.mobile_number +"\n"+"राज्य: "+ii.state +"\n"+"ज़िला: "+ ii.district +"\n"+"खंड: "+ ii.block +"\n"+"स्वास्थ्य केंद्र "+ ii.facility_name + "\n" +"आईडी नंबर: "+ ii.id_number
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

                handleHindiTextQuery(response[0]['from'], datamsg ,False)
                client.interactivte_reply("क्या आप फॉर्म जमा करना चाहते हैं ??", response[0]['from'],returnYesHindi(),returnNoHindi())




            elif response[0]['msg_text'] == returnYesHindi()  and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'], "आपका पंजीकरण सफलतापूर्वक पूरा हुआ।" ,False)
                templateData = [
                        {
                          "title": "Select one question",
                          "rows": [
                            {
                              "id": "q_1",
                              "title": "स्टॉक गणना"
                            },
                            {
                              "id": "q_2",
                              "title": "एनीमियाे सम्बंधित"
                            },
                            {
                              "id": "q_3",
                              "title": "मांग का अनुमान"
                            },
                            {
                              "id": "q_4",
                              "title": "प्रश्न और उत्तर"
                            }
                          ]
                        }
                      ]
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")
                client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")


                print("=================@@@@@@@@@@@=======================")




            # jkbkj




            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी हटा दी है, कृपया अपनी जानकारी फिर से डालें।",False)
                handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)




            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='Hindi':
                print("COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                # checkRegObject.current_stage = "question_topic_selection"
                # checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"आपने चुना  " + response[0]['msg_text'],False)
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            # Hindi  ANM Registration Start









            # Hindi ASHA Registration Start



            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegASHA(place=checkRegObject,name=checkRegObject.name)
                beneData.save()
                client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)



            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegASHA(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                client.sendMsgForConfirmation("आप इस नंबर से आगे बढ़ना चाहते हैं " + response[0]['from'],response[0]['from'],returnYesHindi(),returnNoHindi())
                pass


            elif response[0]['msg_text'] == returnYesHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                handleHindiTextQuery(response[0]['from'],"हमने आपका नंबर पंजीकृत कर लिया है",False)
                beneData.mobile_number = response[0]['from']
                beneData.save()
                # handleHindiTextQuery(response[0]['from'],"आप किस राज्य के हैं",False)
                templateData = [
                        {
                          "title": "राज्य का नाम",
                          "rows": [
                            {
                              "id": "madhya_pradesh",
                              "title": "मध्य प्रदेश"
                            },
                            {
                              "id": "gujarat",
                              "title": "गुजरात"
                            }
                          ]
                        }
                      ]

                client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")




            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)



            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                sta = inputNumber(response[0]['msg_text'],"MOBILE_NUMBER")
                if sta == 'TRUE':
                    checkRegObject.current_stage = "What_is_your_state"
                    checkRegObject.save()
                    beneData = RegASHA.objects.get(place=checkRegObject)
                    beneData.mobile_number = response[0]['msg_text']
                    beneData.save()
                    templateData = [
                            {
                              "title": "राज्य का नाम",
                              "rows": [
                                {
                                  "id": "madhya_pradesh",
                                  "title": "मध्य प्रदेश"
                                },
                                {
                                  "id": "gujarat",
                                  "title": "गुजरात"
                                }
                              ]
                            }
                          ]

                    client.interactivte_reply_list(templateData,"आप किस राज्य के है" ,response[0]['from'],"दबाएँ")
                elif sta == 'DIGIT_ISSUE':
                    handleHindiTextQuery(response[0]['from'],"कृपया 10 अंकों की संख्या डालें।",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)
                else:
                    handleHindiTextQuery(response[0]['from'],"आपने गलत इनपुट दिया है",False)
                    handleHindiTextQuery(response[0]['from'],"अपना नंबर दर्ज करें",False)




            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस जिले के हैं",False)

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"आप किस ब्लॉक के हैं",False)


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_village"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"गांव का नाम",False)


            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_village_population"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.village = response[0]['msg_text']
                beneData.save()
                handleHindiTextQuery(response[0]['from'],"गाँव की जनसंख्या",False)


            elif checkRegObject.current_stage=='What_is_village_population' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
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
                client.interactivte_reply("क्या आप फॉर्म जमा करना चाहते हैं ??", response[0]['from'],returnYesHindi(),returnNoHindi())




            elif response[0]['msg_text'] == returnYesHindi()  and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'], "आपका पंजीकरण सफलतापूर्वक पूरा हुआ।" ,False)
                templateData = [
                        {
                          "title": "Select one question",
                          "rows": [
                            {
                              "id": "q_1",
                              "title": "स्टॉक गणना"
                            },
                            {
                              "id": "q_2",
                              "title": "एनीमियाे सम्बंधित"
                            },
                            {
                              "id": "q_3",
                              "title": "मांग का अनुमान"
                            },
                            {
                              "id": "q_4",
                              "title": "प्रश्न और उत्तर"
                            }
                          ]
                        }
                      ]
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")
                client.interactivte_reply_list(templateData, "आपको किस जानकारी की ज़रूरत है?" ,response[0]['from'],"दबाएँ")
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")


                print("=================@@@@@@@@@@@=======================")

            elif response[0]['msg_text'] == returnNoHindi() and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleHindiTextQuery(response[0]['from'],"हमने आपकी जानकारी हटा दी है, कृपया अपनी जानकारी फिर से डालें।",False)
                handleHindiTextQuery(response[0]['from'],"अपना नाम दर्ज करें",False)

            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='Hindi':
                print("COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                # checkRegObject.current_stage = "question_topic_selection"
                # checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"आपने चुना  "   + response[0]['msg_text'],False)
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            # Hindi  ASHA Registration Start



















            # English Language Setup
            # ################################
            #################################
            elif checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='NA' and checkRegObject.language=='English':
                print("Comming 5")
                if response[0]['msg_text'] == 'Beneficiary':
                    checkRegObject.reg_role = 'Beneficiary'
                    checkRegObject.current_stage = "What_is_your_name"
                    checkRegObject.save()
                    handleEnglishTextQuery(response[0]['from'],"You are Beneficiary",False)
                    handleEnglishTextQuery(response[0]['from'],"Enter your name",False)

                elif response[0]['msg_text'] == 'Healthworker':
                    checkRegObject.reg_role = 'HCW'
                    checkRegObject.save()
                    handleEnglishTextQuery(response[0]['from'],"You are Healthworker",False)
                    client.send_media_msg("hwc_identification","724155319105458", response[0]['from'])
                else:
                    pass


            elif response[0]['msg_text'] == 'ANM' and checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='HCW' and checkRegObject.language=='English':
                print("Comming 6")
                checkRegObject.reg_role = 'ANM'
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You are ANM",False)
                handleEnglishTextQuery(response[0]['from'],"Enter your name",False)

            elif response[0]['msg_text'] == 'ASHA' and checkRegObject.current_stage=='LANGUAGE_SETUP_COMPLETE' and checkRegObject.reg_role=='HCW' and checkRegObject.language=='English':
                print("Comming 6")
                checkRegObject.reg_role = 'ASHA'
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You are ASHA",False)
                handleEnglishTextQuery(response[0]['from'],"Enter your name",False)





            # Beneficiary Registration Start
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_age"
                checkRegObject.save()
                beneData = RegBeneficiary(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"What is your age",False)
                pass


            elif checkRegObject.current_stage=='What_is_your_age' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                # rStatus = validationMsg("INT",response[0]['msg_text'],"AGE")
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.age = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Phone Number",False)

            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.mobile_number = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your State",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your District",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your Block",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your Village Name",False)
            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your District",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your Block",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your Village Name",False)
            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Block",False)
                # handleEnglishTextQuery(response[0]['from'],"Enter Your Village Name",False)
            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_village"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Village Name",False)
            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "asking_for_confirmation"
                checkRegObject.save()
                beneData = RegBeneficiary.objects.get(place=checkRegObject)
                beneData.village = response[0]['msg_text']
                beneData.save()
                beneregData = RegBeneficiary.objects.filter(place=checkRegObject)
                datamsg = ''
                print("beneregDatabeneregData",beneregData)
                for ii in beneregData:
                    datamsg = "Name: " + ii.name  +"\n"+"Age: "+ ii.age +"\n"+"Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Village: "+ ii.village
                handleEnglishTextQuery(response[0]['from'], datamsg ,False)
                client.interactivte_reply("Do you want to submit ??", response[0]['from'],"Yes","No")

            elif response[0]['msg_text'] == "submit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'], "Your Registration Successfully Completed" ,False)
                client.send__msg_button_without_media("beneficiary_identification", response[0]['from'],'en')


            elif response[0]['msg_text'] == "edit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"Enter your name",False)


            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "question_topic_selection"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You are selected  " + response[0]['msg_text'],False)
                if response[0]['msg_text'] == "Currently Pregnant":
                    client.send_media_msg("beneficiary_profile","3347506832153472", response[0]['from'],'en')



            elif checkRegObject.current_stage=='question_topic_selection' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "enter_menstrual_date"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"What was your Last menstrual period date",False)


            # Reply By Bot
            elif checkRegObject.current_stage=='enter_menstrual_date' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "cal_menstrual_date"
                print("--------------------------------------------------------------")
                checkRegObject.save()
                date_object = datetime.strptime(response[0]['msg_text'], '%d/%m/%Y').date()
                new_date = date_object + relativedelta(months=9,days=7)
                print("KHJK",calculateTrimester(response[0]['msg_text']))
                print("KHJK",new_date)
                print("--------------------------------------------------------------")
                handleEnglishTextQuery(response[0]['from'],"your expected EDD is this...."+  str(new_date)  +" and you are in " + calculateTrimester(response[0]['msg_text'],"English"),False)
                print("--------------------------------------------------------------")
                handleEnglishTextQuery(response[0]['from'],"what is your Hemoglobin level",False)


            elif checkRegObject.current_stage=='cal_menstrual_date' and checkRegObject.reg_role=='Beneficiary' and checkRegObject.language=='English':
                checkRegObject.current_stage = "cal_hb_level"
                checkRegObject.save()
                reDtata = countingHBLevel(response[0]['msg_text'],"English")
                handleEnglishTextQuery(response[0]['from'],reDtata,False)
                client.send_media_msg("beneficiary_engagement_question","3347506832153472", response[0]['from'],'hi')



            # Beneficiary Registration End






            # ANM Registration Start
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegANM(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Phone Number",False)


            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.mobile_number = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your State",False)

            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your District",False)

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Block",False)


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_facility"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Facility Name",False)

            elif checkRegObject.current_stage=='What_is_your_facility' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_id_number"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.facility_name = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your ID Number",False)



            elif checkRegObject.current_stage=='What_is_your_id_number' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "asking_for_confirmation"
                checkRegObject.save()
                beneData = RegANM.objects.get(place=checkRegObject)
                beneData.id_number = response[0]['msg_text']
                beneData.save()
                beneregData = RegANM.objects.filter(place=checkRegObject)
                datamsg = ''
                print("beneregDatabeneregData",beneregData)
                for ii in beneregData:
                    datamsg = "Name: " + ii.name  +"\n"+"Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Facility Name: "+ ii.facility_name +"\n"+"ID Number: "+ ii.id_number
                handleEnglishTextQuery(response[0]['from'], datamsg ,False)
                client.interactivte_reply("Do you want to submit ??", response[0]['from'],"Yes","No")

            elif response[0]['msg_text'] == "submit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'], "Your Registration Successfully Completed" ,False)
                templateData = [
                        {
                          "title": "Select one question",
                          "rows": [
                            {
                              "id": "q_1",
                              "title": "Stock calculation"
                            },
                            {
                              "id": "q_2",
                              "title": "Anemia related "
                            },
                            {
                              "id": "q_3",
                              "title": "Demand estimation"
                            },
                            {
                              "id": "q_4",
                              "title": "Q n A"
                            }
                          ]
                        }
                      ]
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")
                client.interactivte_reply_list(templateData,"What information do you need?" ,response[0]['from'],"Click")
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")

            elif response[0]['msg_text'] == "edit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"Enter your name",False)

            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage=='profile_submit_successfully' and checkRegObject.reg_role=='ANM' and checkRegObject.language=='English':
                print("COOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                checkRegObject.current_stage = "question_topic_selection"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You are selected  " + response[0]['msg_text'],False)
                print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
            # ANM Registration Complete









            # ASHA Registration Start
            elif checkRegObject.current_stage=='What_is_your_name' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_mobile"
                checkRegObject.save()
                beneData = RegASHA(place=checkRegObject,name=response[0]['msg_text'])
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"What is your mobile number",False)
                pass


            elif checkRegObject.current_stage=='What_is_your_mobile' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_state"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.mobile_number = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your State",False)


            elif checkRegObject.current_stage=='What_is_your_state' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_district"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.state = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your District",False)

            elif checkRegObject.current_stage=='What_is_your_district' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_block"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.district = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Block",False)


            elif checkRegObject.current_stage=='What_is_your_block' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_your_village"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.block = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Village Name",False)


            elif checkRegObject.current_stage=='What_is_your_village' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "What_is_village_population"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.village = response[0]['msg_text']
                beneData.save()
                handleEnglishTextQuery(response[0]['from'],"Enter Your Village Population",False)


            elif checkRegObject.current_stage=='What_is_village_population' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "asking_for_confirmation"
                checkRegObject.save()
                beneData = RegASHA.objects.get(place=checkRegObject)
                beneData.village_population = response[0]['msg_text']
                beneData.save()
                beneregData = RegASHA.objects.filter(place=checkRegObject)
                datamsg = ''
                for ii in beneregData:
                    datamsg = "Name: " + ii.name  +"\n"+ "Mobile Number: "+ ii.mobile_number +"\n"+"State: "+ii.state +"\n"+"District: "+ ii.district +"\n"+"Block: "+ ii.block +"\n"+"Village: "+ ii.village + "\n" +"Village Population: "+ ii.village_population
                handleEnglishTextQuery(response[0]['from'], datamsg ,False)
                client.interactivte_reply("Do you want to submit  ??", response[0]['from'],"Yes","No")

            elif response[0]['msg_text'] == "submit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "profile_submit_successfully"
                checkRegObject.reg_status = "REGISTRATION_COMPLETED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'], "Your Registration Successfully Completed" ,False)

                templateData = [
                        {
                          "title": "Select one question",
                          "rows": [
                            {
                              "id": "q_1",
                              "title": "Stock calculation"
                            },
                            {
                              "id": "q_2",
                              "title": "Anemia related "
                            },
                            {
                              "id": "q_3",
                              "title": "Demand estimation"
                            },
                            {
                              "id": "q_4",
                              "title": "Q n A"
                            }
                          ]
                        }
                      ]
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")
                client.interactivte_reply_list(templateData, "What information do you need?",response[0]['from'],"Click")
                print("OOOOOOOOOOOOPPPPPPPPPPPPPPPPPPPPPPPADITYA SGUGUGUG PPPPPPPPPP")

            elif response[0]['msg_text'] == "edit" and checkRegObject.current_stage=='asking_for_confirmation' and checkRegObject.reg_role=='ASHA' and checkRegObject.language =='English':
                checkRegObject.current_stage = "What_is_your_name"
                checkRegObject.reg_status = "REGISTRATION_PROCESS_STARTED"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"Enter your name",False)



            ##########################################################
            ########## Registration Complete And Q/A Start ##########################
            ###########################################################
            elif checkRegObject.current_stage =='profile_submit_successfully' and checkRegObject.reg_role=='ASHA' and checkRegObject.language=='English':
                checkRegObject.current_stage = "question_topic_selection"
                checkRegObject.save()
                handleEnglishTextQuery(response[0]['from'],"You are selected  " + response[0]['msg_text'],False)
            else:
                print(checkRegObject.current_stage,checkRegObject.reg_role,checkRegObject.language)
            return Response({"status": "success"}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        print("Registration Process Start")
        resObject = WAPIRegistration(name=response[0]['contacts'],reg_role='NA',reg_mobile=response[0]['from'],language='NA',reg_status='NA',current_stage='LANGUAGE_SETUP_PROCESS',request_for_previous_stage='No')
        resObject.save()
        response = client.send_media_msg("intro_rati","519795810307895", response[0]['from'])
        return Response({"status": "success"}, status=status.HTTP_200_OK)










