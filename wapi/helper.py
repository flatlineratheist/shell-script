from .whatsapp_client import *
import os
from .models import *


def getAllStateName(lang):
    if lang == 'Hindi':
        stateDict = []
        stateList = [['मध्य प्रदेश',"मध्य प्रदेश"],['गुजरात','गुजरात']]
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        print("stateDict",stateDict)
        return stateDict
    elif lang == 'English':
        stateDict = []
        stateList = [['Madhya Pradesh',"Madhya Pradesh"],['Gujarat','Gujarat']]
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        print("stateDict",stateDict)
        return stateDict
         
    else:
        pass


def getAllDistrctNameByID(lang,state_id):
    if lang == 'Hindi':
        stateDict = []
        print("jkblkj")
        districtList = {
            'मध्य प्रदेश':[['दमोह',"दमोह"],['भोपाल','भोपाल'],['छतरपुर',"छतरपुर"],['इंदौर','इंदौर']],
            'गुजरात':[['दाहोद',"दाहोद"],['जामनगर','जामनगर'],['गांधीनगर',"गांधीनगर"],['वडोदरा','वडोदरा']],
            }
        stateList = districtList[state_id]
        print("stateList")
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        return stateDict
    elif lang == 'English':
        stateDict = []
        districtList = {
            'Madhya Pradesh':[['Damoh',"Damoh"],['Bhopal','Bhopal'],['Chhatarpur',"Chhatarpur"],['Indore','Indore']],
            'Gujarat':[['Dahod',"Dahod"],['Jamnagar','Jamnagar'],['Gandhinagar',"Gandhinagar"],['Vadodara','Vadodara']],
            }
        stateList = districtList[state_id]
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        return stateDict
         
    else:
        pass

def getAllBlocktNameByID(lang,state_id,district_id):
    if lang == 'Hindi':
        stateDict = []
        districtList = {
            "मध्य प्रदेश":{'दमोह':[['दमोह',"दमोह"],['पथरिया','पथरिया'],['बटियागढ़',"बटियागढ़"],['हट्टा','हट्टा'],['पटेरा','पटेरा'],['तेंदूखेड़ा','तेंदूखेड़ा'],['जबेरा','जबेरा']],
            'भोपाल':[['हुजूर',"हुजूर"],['कोलार','कोलार'],['बैरसिया',"बैरसिया"]],
            'छतरपुर':[['छतरपुर',"छतरपुर"],['बड़ा मल्हेरा','बड़ा मल्हेरा'],['बिजावर',"बिजावर"],['बक्सवाहा','बक्सवाहा'],['चंदला','चंदला'],['गौरिहार',"गौरिहार"],
            ['घुवारा','घुवारा'],['लौंडी','लौंडी'],['महाराजपुर',"महाराजपुर"],['नौगांव','नौगांव']],
            'इंदौर':[['राजनगर',"राजनगर"],['कनाड़िया','कनाड़िया'],['बिचौली हपसी',"बिचौली हपसी"],['मल्हारगंज','मल्हारगंज'],
                ['खुदैल',"खुदैल"],['राव','राव'],['डॉ. अम्बेडकर नगर',"डॉ. अम्बेडकर नगर"],['सांवेर','सांवेर'],['देपालपुर','देपालपुर'],['हातोद','हातोद']]},
                "गुजरात":{
                    'दाहोद':[['दाहोद',"दाहोद"],['देवगढ़','देवगढ़'],['बैरिया',"बैरिया"],['धनपुर','धनपुर'],['फतेपुरा','फतेपुरा'],['गरबाड़ा','गरबाड़ा'],
                    ['लिमखेड़ा','लिमखेड़ा'],['संजेली','संजेली'],['झालोद','झालोद'],['सिंगवाड','सिंगवाड']],
            'जामनगर':[['जामनगर',"जामनगर"],['ध्रोल','ध्रोल'],['जामजोधपुर',"जामजोधपुर",["जोड़िया","जोड़िया"],["कलावड़","कलावड़"],["लालपुर","लालपुर"]]],
            'गांधीनगर':[['गांधीनगर',"गांधीनगर"],['देहगाम','देहगाम'],['कलोल',"कलोल"],['मनसा','मनसा']],
            'वडोदरा':[['वड़ोदरा',"वड़ोदरा"],['दभोई','दभोई'],['देसर',"देसर"],['कर्जन','कर्जन'],
                ['पदरा',"पदरा"],['सावली','सावली'],['सिनोर',"सिनोर"],['वाघोडिया','वाघोडिया']]
                }
            
            }
        stateList = districtList[state_id][district_id]
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        return stateDict
    elif lang == 'English':
        stateDict = []
        districtList = {
            "Madhya Pradesh":{'Damoh':[['Damoh',"Damoh"],['Patharia','Patharia'],['Batiagarh',"Batiagarh"],
                        ['Hatta','Hatta'],['Patera','Patera'],['Tendukheda','Tendukheda'],['Jabera','Jabera']],
            'Bhopal':[['Huzur',"Huzur"],['Kolar','Kolar'],['Berasia',"Berasia"]],
            'Chhatarpur':[['Chhatarpur',"Chhatarpur"],['Bada Malhera','Bada Malhera'],['Bijawar',"Bijawar"],['Buxwaha','Buxwaha'],
            ['Chandla','Chandla'],['Gaurihar',"Gaurihar"],['Ghuwara','Ghuwara'],
            
            ['Laundi','Laundi'],['Maharajpur',"Maharajpur"],['Nowgong','Nowgong']],
            'Indore':[['Rajnagar',"Rajnagar"],['Kanadiya','Kanadiya'],['Bicholi Hapsi',"Bicholi Hapsi"],['Malharganj','Malharganj'],
                ['Khudail',"Khudail"],['Rau','Rau'],['Dr. Ambedkar Nagar',"Dr. Ambedkar Nagar"],['Sanwer','Sanwer'],
                ['Depalpur',"Depalpur"],['Hatod','Hatod']]},

            "Gujarat":{'Dahod':[['Dahod',"Dahod"],['Devgadh baria','Devgadh baria'],['Dhanpur',"Dhanpur"],
                        ['Fatepura','Fatepura'],['Garbada','Garbada'],['Limkheda','Limkheda'],['Sanjeli','Sanjeli'],
                        ['Jhalod','Jhalod'],['Singvad','Singvad']],
            'Jamnagar':[['Jamnagar',"Jamnagar"],['Dhrol','Dhrol'],['Jamjodhpur',"Jamjodhpur"],['Jodiya','Jodiya'],['Kalavad',"Kalavad"],['Lalpur',"Lalpur"]],
            'Gandhinagar':[['Gandhinagar',"Gandhinagar"],['Dehgam','Dehgam'],['Kalol',"Kalol"],['Mansa','Mansa']],
            'Vadodara':[['Vadodara',"Vadodara"],['Dabhoi','Dabhoi'],['Desar',"Desar"],['Karjan','Karjan'],
                ['Padra',"Padra"],['Savli','Savli'],['Sinor',"Sinor"],['Vaghodia','Vaghodia']]}
            
            }
        stateList = districtList[state_id][district_id]
        for i in range(len(stateList)):
            stateDict.append({'id':stateList[i][0],'title':stateList[i][1]})
        return stateDict
         
    else:
        pass


def returnHindi():
    return "हिंदी"

def returnEnglish():
    return "English"

def returnGujrati():
    return "ગુજરાતી"





def getLangText(code):
    dataT = RegQuestion.objects.get(question_code=code)
    return dataT.question_text


def AboutSomthingMore(response,qtext,lang):
    print("kbcekbkbvkje",qtext)
    client = WhatsAppWrapper()
    if lang == 'Hindi':
        print("(*********************",qtext)
        if qtext == "SEND_GAME_LINK":
            client.send_media_url("आओ खेले  ","https://ifabot.dev-tattvafoundation.org/?username="+response[0]['from'],response[0]['from'])

        elif qtext == questionHindiMore('anemia_info'):
            print("lknk")
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
        elif qtext == questionHindiMore('cal_info'):
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

        elif qtext == questionHindiMore('cal_info'):
            client.send_document_message(response[0]['from'],"1131182871608893","स्वादिष्ट और स्वास्थ्यवर्धक भोजन देखें जो तैयार किया जा सकता है।","healthy_food")

        elif qtext == questionHindiMore('playGame'):
            client.send_media_url("आओ खेले   ","https://ifabot.dev-tattvafoundation.org/?username="+response[0]['from'],response[0]['from'])

        elif qtext == questionHindiCalMore('cal_need'):
            client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

        elif qtext == questionHindiCalMore('cal_good_resource'):
            client.send_media_url("कैल्शियम युक्त भोजन के अच्छे स्रोत   ","https://www.youtube.com/watch?v=7U7KybN5CLQ",response[0]['from'])
            

        elif qtext == questionHindiCalMore('cal_medicine_take'):
            client.send_image_message( response[0]['from'],"218512910669678")  #Thumb Up

        elif qtext == questionHindiCalMore('other'):
            client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
            handleHindiTextQuery(response[0]['from'],"अधिक जानकारी के लिए कृपया अपनी आशा दीदी या एएनएम से संपर्क करें",False)

        elif qtext == questionHindiAnimiaMore('what_animia'):
            client.send_media_url("एनीमिया क्या है- एनीमिया के बारे में जानने के लिए यह वीडियो देखें   ","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])

        elif qtext == questionHindiAnimiaMore('animia_def'):
            client.send_image_message( response[0]['from'],"1260219784852086")  #Thumb Up

        elif qtext == questionHindiAnimiaMore('animia_effect'):
            client.send_media_url(" एनीमिया का प्रभाव- जानें कि एनीमिया आपको कैसे प्रभावित करता है   ","https://www.youtube.com/watch?v=IUTob1tMdck",response[0]['from'])

        elif qtext == questionHindiAnimiaMore('animia_do_not'):
            client.send_image_message( response[0]['from'],"959279025480160")  #Thumb Up


        elif qtext == questionHindiAnimiaMore('iron_food'):
            client.send_image_message( response[0]['from'],"664704058742018")  #Thumb Up

        elif qtext == questionHindiAnimiaMore('iron_tablet_info'):
            client.send_image_message( response[0]['from'],"1037169314353036")  #Thumb Up

        elif qtext == questionHindiAnimiaMore('iron_tablet_sol'):
            client.send_media_url("एनीमिया की रोकथाम और उपचार " , "https://youtu.be/Cz6yhxJg5OA",response[0]['from'])

        elif qtext == questionHindiAnimiaMore('other'):
            client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
            handleHindiTextQuery(response[0]['from'],"अधिक जानकारी के लिए कृपया अपनी आशा दीदी या एएनएम से संपर्क करें",False)

        elif qtext == questionHindiMore('health_food'):
            client.send_document_message(response[0]['from'],"1131182871608893","स्वादिष्ट और स्वास्थ्यवर्धक भोजन देखें जो तैयार किया जा सकता है।","healthy_food")

        else:
            ElseMoreHindi(response)

    elif lang == 'English':
        if qtext == "SEND_GAME_LINK":
            client.send_media_url("let's play  ","https://ifabot.dev-tattvafoundation.org/?username="+response[0]['from'],response[0]['from'])

        elif qtext == questionEnglishMore('anemia_info'):
            listData = []
            for i in range(len(what_do_you_want_animia_English())):
                listData.append(
                    {
                        "id": what_do_you_want_animia_English()[i],
                        "title": what_do_you_want_animia_English()[i]
                        }
                    )

            print("listData",listData)
            templateData = [
                    {
                    "title":  "Select an option",
                    "rows": listData
                    }
                ]
            client.interactivte_reply_list(templateData,"about anemia",response[0]['from'],"choose")
        elif qtext == questionEnglishMore('cal_info'):
            listData = []
            for i in range(len(what_do_you_want_cal_English())):
                listData.append(
                    {
                        "id": what_do_you_want_cal_English()[i],
                        "title": what_do_you_want_cal_English()[i]
                        }
                    )

            print("listData",listData)
            templateData = [
                    {
                    "title":  "Select an option",
                    "rows": listData
                    }
                ]
            client.interactivte_reply_list(templateData,"about calcium",response[0]['from'],"choose")

        elif qtext == questionEnglishMore('cal_info'):
            client.send_document_message(response[0]['from'],"1131182871608893","See the tasty and healthy food which can be prepared. ","healthy_food")

        elif qtext == questionEnglishMore('playGame'):
            client.send_media_url("let's play  ","https://ifabot.dev-tattvafoundation.org/?username="+response[0]['from'],response[0]['from'])

        elif qtext == questionEnglishCalMore('cal_need'):
            client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

        elif qtext == questionEnglishCalMore('cal_good_resource'):
            client.send_media_url("Good sources of calcium rich food   ","https://www.youtube.com/watch?v=7U7KybN5CLQ",response[0]['from'])

        elif qtext == questionEnglishCalMore('cal_medicine_take'):
            client.send_image_message( response[0]['from'],"1150780058917815")  #Thumb Up

        elif qtext == questionEnglishCalMore('other'):
            client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
            handleEnglishTextQuery(response[0]['from'],"For more details please contact your ASHA Didi or ANM",False)

        elif qtext == questionEnglishAnimiaMore('what_animia'):
            client.send_media_url("What is anemia - See this video to learn about anemia  ","https://youtu.be/_aTUoRMGKDQ",response[0]['from'])

        elif qtext == questionEnglishAnimiaMore('animia_def'):
            client.send_image_message( response[0]['from'],"1260219784852086")  #Thumb Up

        elif qtext == questionEnglishAnimiaMore('animia_effect'):
            client.send_media_url("Impact of anemia - Learn how anemia impacts your ","https://www.youtube.com/watch?v=IUTob1tMdck",response[0]['from'])

        elif qtext == questionEnglishAnimiaMore('animia_do_not'):
            client.send_image_message( response[0]['from'],"959279025480160")  #Thumb Up


        elif qtext == questionEnglishAnimiaMore('iron_food'):
            client.send_image_message( response[0]['from'],"664704058742018")  #Thumb Up

        elif qtext == questionEnglishAnimiaMore('iron_tablet_info'):
            client.send_image_message( response[0]['from'],"1037169314353036")  #Thumb Up

        elif qtext == questionEnglishAnimiaMore('iron_tablet_sol'):
            client.send_media_url("Prevention and treatment of anemia " , "https://youtu.be/Cz6yhxJg5OA",response[0]['from'])

        elif qtext == questionEnglishAnimiaMore('other'):
            client.send_image_message( response[0]['from'],"588993259465555")  #Thumb Up
            handleEnglishTextQuery(response[0]['from'],"For more details please contact your ASHA Didi or ANM",False)

        elif qtext == questionEnglishMore('health_food'):
            client.send_document_message(response[0]['from'],"1131182871608893","See the tasty and healthy food which can be prepared. ","healthy_food")

        else:
            ElseMoreEnglish(response)










def ElseMoreHindi(response):
    client = WhatsAppWrapper()
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
    client.interactivte_reply_list(templateData,"कुछ पूछना चाहते है?",response[0]['from'],"चुनें")

def ElseMoreEnglish(response):
    client = WhatsAppWrapper()
    listData = []
    for i in range(len(what_do_you_want_else_English())):
        listData.append(
            {
            "id": what_do_you_want_else_English()[i],
            "title": what_do_you_want_else_English()[i]
            }
        )

    print("listData",listData)
    templateData = [
        {
        "title":  "Select an option",
        "rows": listData
        }
    ]
    print("bhjk========================")
    client.interactivte_reply_list(templateData,"Want to ask something?",response[0]['from'],"click")
    print("lkbk")






'''
def questionForMildAnemia():
    anemia_def_english = "The Hemoglobin level in your blood is low. This condition is called Anemia."
    anemia_def_hindi = "आपके शरीर में खून की कमी है। इस स्थिति को एनीमिया कहा जाता है"
    anemia_def_gujrati = "તમારા શરીરમાં લોહીની ઉણપ છે. આ સ્થિતિને એનિમિયા કહેવામાં આવે છે"
    know_more_anemia_hindi = "एनीमिया के बारे में अधिक जानने के लिए यहां क्लिक करें"
    know_more_anemia_gujrati = "એનિમિયા વિશે વધુ જાણવા માટે અહીં ક્લિક કરો"
    ifa_tablet_english = "Did you take IFA tablet today?"
    side_effect_ifa_tablet_english = "Do u experience any discomfort after taking IFA tablet? like stomach pain,vomitting, indigestion, others?"
    side_effect_ifa_tablet_hindi = "क्या आयरन की गोलियां लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य"
    side_effect_ifa_tablet_gujrati = "આયર્ન ગોળીઓ લીધા પછી શું તમને કોઈ અગવડતા લાગે છે? જેમ કે પેટમાં દુખાવો, ઉલ્ટી, અપચો, અન્ય"

    iron_tablet_take_english = "Dont forget to take your tablets today!!!!"
    iron_tablet_hindi = "अपनी आयरन की गोली लेना न भूलें!!!"
    forget_reminder_checkup_english = "Did you complete your health checkup?"
    forget_reminder_checkup_hindi =  "क्या आपने अपना मासिक स्वास्थ्य परीक्षण पूरा किया ?"
    forget_reminder_checkup_gujrati = "શું તમે તમારું સ્વાસ્થ્ય તપાસ પૂર્ણ કર્યું છે?"

    visit_health_center_english = "visit your nearest healthcenter soon!!"
    visit_health_center_hindi = "जल्द से जल्द अपने नजदीकी स्वास्थ्य केंद्र पर जाएं और जांच कराएं !!"
    visit_health_center_gujrati = "શક્ય તેટલી વહેલી તકે તમારા નજીકના આરોગ્ય કેન્દ્રની મુલાકાત લો અને પરીક્ષણ કરાવો"

    no_ifa_tablet_hindi = "क्या आपने आज आयरन की गोली खाई?"
    no_ifa_tablet_english = "how many IFA tablet"
    no_cal_tablet_eng = "Did you take your calcium tablet today??"
    no_cal_tablet_hindi = "क्या आपने आज कैल्शियम की गोली ली ??"
    no_cal_tablet_gujrati = "શું તમે આજે તમારી કેલ્શિયમની ગોળી લીધી??"
'''



def scheduleMessage_pragnant(qLable,response,lang):
    client = WhatsAppWrapper()
    if lang == 'Hindi':
        if qLable == 'reminder_to_visithb_checkup':
            client.interactivte_reply("क्या आपने अपना एचबी चेक किया हां नहीं",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'do_not_forget_iron_tablet':
            handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!",False)
            client.send_image_message( response[0]['from'],"760452812157139")
            client.send_media_url("आयरन की गोलियों के बारे में जानने के लिए क्लिक करें ","https://youtu.be/qX4yD2h5a9c",response[0]['from'])

        if qLable == 'do_you_know_your_hemoglobin':
            client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],returnYesHindi(),returnNoHindi())


        if qLable == 'did_you_complete_health_checkup':
            client.interactivte_reply("क्या आपने अपना मासिक स्वास्थ्य परीक्षण पूरा किया",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'go_quick_health_checkup':
            handleHindiTextQuery(response[0]['from'],"जल्द से जल्द अपने नजदीकी स्वास्थ्य केंद्र पर जाएं और जांच कराएं !!",False)
            pass
        if qLable == 'iron_side_effect':
            client.interactivte_reply("क्या आयरन की गोलियां लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'ifa_side_effect':
            client.interactivte_reply("क्या आपने आज आयरन की गोली खाई?",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'calcium_medicine_take':
            client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'ifa_tablet_take_or_not':
            client.interactivte_reply("क्या आपने आज अपनी कैल्शियम की गोली ली?",response[0]['from'],returnYesHindi(),returnNoHindi())
        if qLable == 'iromMdecine':
            handleHindiTextQuery(response[0]['from'],"अपनी आयरन की गोली लेना न भूलें!!!",False)
    elif lang == 'English':
        if qLable == 'reminder_to_visithb_checkup':
            client.interactivte_reply("क्या आपने अपना एचबी चेक किया हां नहीं",response[0]['from'],"Yes","No")
        if qLable == 'do_not_forget_iron_tablet':
            handleHindiTextQuery(response[0]['from'],"Don't forget to take your iron pill!!!",False)
            client.send_image_message( response[0]['from'],"760452812157139")
            client.send_media_url("आयरन की गोलियों के बारे में जानने के लिए क्लिक करें ","https://youtu.be/qX4yD2h5a9c",response[0]['from'])

        if qLable == 'do_you_know_your_hemoglobin':
            client.interactivte_reply("क्या आप रक्त में अपने हीमोग्लोबिन स्तर को जानते हैं?",response[0]['from'],"Yes","No")


        if qLable == 'did_you_complete_health_checkup':
            client.interactivte_reply("Have you completed your monthly health checkup?",response[0]['from'],"Yes","No")
        if qLable == 'go_quick_health_checkup':
            handleHindiTextQuery(response[0]['from'],"Go to your nearest health center as soon as possible and get tested!!",False)
            pass
        if qLable == 'iron_side_effect':
            client.interactivte_reply("क्या आयरन की गोलियां लेने के बाद आपको कोई परेशानी महसूस होती है? जैसे पेट दर्द, उल्टी, अपच, अन्य",response[0]['from'],"Yes","No")
        if qLable == 'ifa_side_effect':
            client.interactivte_reply("क्या आपने आज आयरन की गोली खाई?",response[0]['from'],"Yes","No")
        if qLable == 'calcium_medicine_take':
            client.interactivte_reply("क्या आपने आज कैल्शियम की गोली ली ??",response[0]['from'],"Yes","No")
        if qLable == 'ifa_tablet_take_or_not':
            client.interactivte_reply("Did you take ifa tablet today?",response[0]['from'],"Yes","No")
        if qLable == 'iromMdecine':
            handleHindiTextQuery(response[0]['from'],"Don't forget to take your iron pill!!!!",False)
    else:
        pass






# Create your views here.











def retuenQuestionText(filterText):
    qText = RegQuestion.objects.get(question_code=filterText)
    return qText.question_text


def ifButtonAlreadyClicked(lngFor,setpDone):
    if lngFor == '':
        pass
    elif lngFor == '':
        pass
    elif lngFor == '':
        pass
    else:
        pass


def languageTranslate(langfor):
    reText = ''
    if langfor == 'Hindi':
        reText = 'हिंदी भाषा '
    elif langfor == 'English':
        reText = 'English language'
    elif langfor == 'Gujrati':
        reText = 'ગુજરાતી ભાષા'
    else:
        pass
    return reText

def returnYesHindi():
    return "हाँ"


def returnNoHindi():
    return "नहीं"


def retuenStateName(stateName,lang):
    if lang == 'Hindi' and stateName == 'Madhya Pradesh':
        return "मध्य प्रदेश"
    if lang == 'Hindi' and stateName == 'Gujrat':
        return "गुजरात"
    if lang == 'English' and stateName == "मध्य प्रदेश":
        return "Madhya Pradesh"
    if lang == 'English' and stateName == "गुजरात":
        return "Gujrat"


def validateDateFormat(date_text):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except:
        return Falsek


def questionHindiMore(qLabel):
    if qLabel == 'stock_est':
        return "मासिक स्टॉक गणना"
    if qLabel == 'demand_est':
        return "वार्षिक मांग का अनुमान"
    if qLabel == 'qa':
        return 'प्रश्न और उत्तर'
    if qLabel == 'anemia_info':
        return 'एनीमिया जानकारी'
    if qLabel == 'cal_info':
        return 'कैल्शियम जानकारी'
    if qLabel == 'health_food':
        return 'पौष्टिक आहार'
    if qLabel == 'playGame':
        return 'आओ खेले'



def what_do_you_want_else_hindi():
    return [questionHindiMore('anemia_info'),questionHindiMore('cal_info'),questionHindiMore('health_food'),questionHindiMore('playGame')]

def questionEnglishMore(qLabel):
    if qLabel == 'stock_est':
        return "Monthly stock estimation"
    if qLabel == 'demand_est':
        return "Annual Demand estimation"
    if qLabel == 'qa':
        return 'Qusestion/Answer'
    if qLabel == 'anemia_info':
        return 'Anemia information'
    if qLabel == 'cal_info':
        return 'Calcium information'
    if qLabel == 'health_food':
        return 'Healthy food'
    if qLabel == 'playGame':
        return 'Lets play'

def what_do_you_want_else_English():
    return [questionEnglishMore('anemia_info'),questionEnglishMore('cal_info'),questionEnglishMore('health_food'),questionEnglishMore('playGame')]



#  Heath Worker
####################

def ElseMoreHindiHealthWorker():
    return [questionHindiMore('stock_est'),questionHindiMore('demand_est'),questionHindiMore('anemia_info'),questionHindiMore('cal_info'),questionHindiMore('health_food'),questionHindiMore('playGame')]



def ElseMoreEnglishHealthWorker():
    return [questionEnglishMore('stock_est'),questionEnglishMore('demand_est'),questionEnglishMore('anemia_info'),questionEnglishMore('cal_info'),questionEnglishMore('health_food'),questionEnglishMore('playGame')]






# Answer Related Question
#  (i)  Animia
#########################################
def questionHindiAnimiaMore(qLabel):
    if qLabel == 'what_animia':
        return "एनीमिया क्या है"
    if qLabel == 'anemia_info':
        return 'एनीमिया जानकारी'
    if qLabel == 'animia_def':
        return "एनीमिया पहचान करें"
    if qLabel == 'animia_effect':
        return "एनीमिया का प्रभाव"
    if qLabel == 'animia_do_not':
        return "करने, न करने योग्य कार्य"
    if qLabel == 'iron_food':
        return "आयरन युक्त आहार"

    if qLabel == 'iron_tablet_info':
        return "आयरन गोली के बारे में"
    if qLabel == 'iron_tablet_sol':
        return "एनीमिया रोकथाम और उपचार"
    if qLabel == 'other':
        return "अन्य"


def what_do_you_want_animia_hindi():
    return [questionHindiAnimiaMore("what_animia"),questionHindiAnimiaMore('animia_def'),questionHindiAnimiaMore('animia_effect'),
            questionHindiAnimiaMore('animia_do_not'),questionHindiAnimiaMore('iron_food'),questionHindiAnimiaMore('iron_tablet_info'),questionHindiAnimiaMore('iron_tablet_sol')]


def questionEnglishAnimiaMore(qLabel):
    if qLabel == 'what_animia':
        return "What is anemia"
    if qLabel == 'anemia_info':
        return 'Anemia information'
    if qLabel == 'animia_def':
        return "Identify anemia"
    if qLabel == 'animia_effect':
        return "Effects of anemia"
    if qLabel == 'animia_do_not':
        return "Do's and don'ts"
    if qLabel == 'iron_food':
        return "Iron rich diet"

    if qLabel == 'iron_tablet_info':
        return "About Iron Folic Acid"
    if qLabel == 'iron_tablet_sol':
        return "Anemia Treatment"
    if qLabel == 'other':
        return "Others"


def what_do_you_want_animia_English():
    return [questionEnglishAnimiaMore("what_animia"),questionEnglishAnimiaMore('animia_def'),questionEnglishAnimiaMore('animia_effect'),
            questionEnglishAnimiaMore('animia_do_not'),questionEnglishAnimiaMore('iron_food'),questionEnglishAnimiaMore('iron_tablet_info'),questionEnglishAnimiaMore('iron_tablet_sol')]



# Answer Related Question
#  (i)  Calcium
#########################################
def questionHindiCalMore(qLabel):
    if qLabel == 'cal_need':
        return "कैल्शियम क्यों जरूरी है"
    if qLabel == 'cal_good_resource':
        return "कैल्शियम के अच्छे आहार"
    if qLabel == 'cal_medicine_take':
        return "कैल्शियम गोली कैसे लें"
    if qLabel == 'other':
        return "अन्य"

def what_do_you_want_cal_hindi():
    return [questionHindiCalMore("cal_need"),questionHindiCalMore('cal_good_resource'),questionHindiCalMore('cal_medicine_take')]


def questionEnglishCalMore(qLabel):
    if qLabel == 'cal_need':
        return "why calcium important"
    if qLabel == 'cal_good_resource':
        return "good calcium foods"
    if qLabel == 'cal_medicine_take':
        return "how take calcium tablet"
    if qLabel == 'other':
        return "Others"

def what_do_you_want_cal_English():
    return [questionEnglishCalMore("cal_need"),questionEnglishCalMore('cal_good_resource'),questionEnglishCalMore('cal_medicine_take')]





# Answer Related Question
# Infant care related information
#  (i)  Calcium
#########################################
def questionEnglishInfant_care_More(qLabel):
    if qLabel == 'vaccine_child':
        return "टीके शिशु को दिए जानें"
    if qLabel == 'complementry_feeding':
        return "पूरक आहार"
    if qLabel == 'vaccine_side_effect':
        return "टीकेे संबंधित दुष्प्रभाव"
    if qLabel == 'other':
        return "अन्य"

def what_do_you_wantInfant_care__hindi():
    return [questionHindiInfant_care_More("vaccine_child"),questionHindiInfant_care_More('complementry_feeding'),questionHindiInfant_care_More('vaccine_side_effect')]

def what_do_you_wantInfant_care__English():
    return ['Qusestion/Answer','Anemia information','Calcium information','Healthy food','Lets play']



# Lactating

def questionHindiLactatingMore(qLabel):
    if qLabel == 'qa':
        return "प्रश्न और उत्तर"
    if qLabel == 'animia_info':
        return "एनीमिया  सम्बंधित"
    if qLabel == 'cal_food':
        return "कैल्शियम सम्बंधित"
    if qLabel == 'child_info':
        return "शिशु  संबंधी"
    if qLabel == 'food_cooking':
        return "पौष्टिक आहार सम्बंधित"
    if qLabel == 'other':
        return "अन्य"

def what_do_you_want_Lactating_hindi():
    # questionHindiLactatingMore("qa"),
    return [questionHindiLactatingMore('animia_info'),questionHindiLactatingMore('iron_food'),questionHindiLactatingMore('child_info'),
            questionHindiLactatingMore('food_cooking')]

def what_do_you_want_Lactating_English():
    return ['Qusestion/Answer','Anemia information','Calcium information','Healthy food','Lets play']








def checkBirthCalculation(datePicker):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 22")

    from datetime import datetime
    from dateutil import relativedelta
    from datetime import date
    today = date.today()
    currentDate = today.strftime("%d/%m/%Y")
    enterDate = datePicker.strftime("%d/%m/%Y")

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 22",currentDate)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 22",enterDate)

    # convert string to date object
    start_date = datetime.strptime(str(currentDate), "%d/%m/%Y")
    end_date = datetime.strptime(str(enterDate), "%d/%m/%Y")


    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 11")

    # Get the relativedelta between two dates
    delta = relativedelta.relativedelta(end_date, start_date)
    print('Years, Months, Days between two dates is')
    print(delta.years, 'Years,', delta.months, 'months,', delta.days, 'days')
    if delta.years != 0:
        return "A_6"
    elif delta.years == 0 and delta.months < 6:
        return "B_6"
    elif delta.days == 0 and delta.months == 6:
        return "E_6"
    elif delta.days != 0 and delta.months == 6:
        return "A_6"
    elif delta.months > 6:
        return "A_6"



def inputNumber(inputD,validationFor):
    try:
        userInput = int(inputD)
        if validationFor == 'AGE':
            if len(inputD) == 2 and userInput > 18 and userInput < 50:
                return "TRUE"
            else:
                return "AGE_LIMIT"
        if validationFor == 'MOBILE_NUMBER':
            if len(inputD) == 10 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"
        if validationFor == 'HB':
            if len(inputD) < 3 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"
        if validationFor == 'POPULATION':
            if len(inputD) < 5 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"
        if validationFor == 'RCH':
            if len(inputD) == 12 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"

        if validationFor == 'NO_PRAGNANT':
            if len(inputD) < 5 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"
        if validationFor == 'NO_LACTATING':
            if len(inputD) < 12 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"

        if validationFor == 'NO_WRA':
            if len(inputD) < 12 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"

        if validationFor == 'NO_EXISTING_STCOK':
            if len(inputD) < 12 :
                return "TRUE"
            else:
                return "DIGIT_ISSUE"

     



    except ValueError:
        return "INT_ISSUE"






def validationMsg(typeData,data,validationFor):
    if typeData == "INT":
        statusResponse = inputNumber(inputD,validationFor)
        return statusResponse
    elif typeData == "DATE":
        return True
    elif typeData == "BUTTON":
        return True
    else:
        return True


def countingHBLevel(hbCount,lang):
    if lang == 'English':
        if  int(hbCount) < 7:
            return "Mild Anemia"
        elif 7 <= int(hbCount) <= 9.9:
            return "Moderate Anemia"
        elif 10.0 <= int(hbCount) <= 10.9:
            return "Severe Anemia"
        else:
            return "no anemia"
    elif lang == 'Hindi':
        if  int(hbCount) < 7:
            return "आपके शरीर में खून की कमी है। इस स्थिति को एनीमिया कहा जाता है"
        elif 7 <= int(hbCount) <= 9.9:
            return "आपके शरीर में खून की कमी है। इस स्थिति को एनीमिया कहा जाता है"
        elif 10.0 <= int(hbCount) <= 10.9:
            return "आपके शरीर में खून की कमी है। इस स्थिति को गंभीर एनीमिया कहा जाता है"
        else:
            return "आपके खून में हीमोग्लोबिन का स्तर सामान्य है। आप एनीमिक नहीं हैं"





# Function Handle Hindi Text Conversation
def handleHindiTextQuery(fromID,msg,tem=False):
    client = WhatsAppWrapper()
    response = client.send_text_msg(
            msg=msg,
            phone_number=fromID
            )
    if tem:
        client.sendMsgForConfirmation("क्या आप स्वास्थ्य कार्यकर्ता हैं या लाभार्थी हैं?",fromID,"लाभार्थी","स्वास्थ्य कार्यकर्ता")
        # response = client.send_media_msg_without_params("user_identification","610976480838229", fromID,'hi')



# Function Handle English Text Conversation
def handleEnglishTextQuery(fromID,msg,tem=False):
    client = WhatsAppWrapper()
    
    response = client.send_text_msg(
            msg=msg,
            phone_number=fromID
            )
    if tem:
        # response = client.send_media_msg_without_params("user_identification","610976480838229", fromID,'en')
        client.sendMsgForConfirmation("Are you a health worker or beneficiary ?",fromID,"Beneficiary","Health Worker")


# Function Handle Gujrati Text Conversation
def handleGujratiTextQuery(fromID,msg,tem=False):
    client = WhatsAppWrapper()
    response = client.send_text_msg(
            msg=msg,
            phone_number=fromID
            )
    if tem:
        # response = client.send_media_msg_without_params("user_identification","610976480838229", fromID,'gu')
        client.sendMsgForConfirmation("क्या आप स्वास्थ्य कार्यकर्ता हैं या लाभार्थी हैं?",fromID,"लाभार्थी","स्वास्थ्य कर्मी")


def calculateTrimester(msg,lang):
    from datetime import datetime, timedelta
    lmp_str = msg
    lmp = datetime.strptime(lmp_str, "%d/%m/%Y")
    edd = lmp + timedelta(days=280)
    today = datetime.today()
    gestational_age = today - lmp
    
    trimester = (gestational_age.days // 7) // 12 + 1
    if lang == 'Hindi':
        if trimester == 1:
            return "पहली"
        elif trimester == 2:
            return "दूसरी"
        elif trimester == 3:
            return "तीसरी"
        else:
            return "बाद की तारिक"
    elif lang == 'English':
        if trimester == 1:
            return "First trimester"
        elif trimester == 2:
            return "Second trimester"
        elif trimester == 3:
            return "Third trimester"
        else:
            return "Post Dated"
    else:
        pass

    # # Display results




    




    # from datetime import date
    # today = date.today()
    # from datetime import datetime
    # from dateutil import relativedelta
    # cuurentDate = today.strftime("%d/%m/%Y")
    # eddDate = msg
    # start_date = datetime.strptime(cuurentDate, "%d/%m/%Y")
    # end_date = datetime.strptime(eddDate, "%d/%m/%Y")
    # delta = relativedelta.relativedelta(end_date, start_date)
    # trimester = ''
    # print(delta.months,"jghujguigbik",delta.days)
    # strM = str(delta.months)
    # strD = str(delta.days)
    # if lang == 'English':
    #     if '-' in strM:
    #         strM = int(strM.replace('-',''))
    #     else:
    #         strM = int(strM)
    #     if '-' in strD:
    #         strD = int(strD.replace('-',''))
    #     else:
    #         strD = int(strD)


    #     if strM <= 3 and strD == 0:
    #         trimester = "First trimester"
    #     else:
    #         trimester = "Second trimester"
    #     if strM <= 6 and strD == 0:
    #         trimester = "Second trimester"
    #     else:
    #         trimester = "Third trimester"

    #     if strM <=9 and strD == 0:
    #         trimester = "Third trimester"
    #     else:
    #         trimester = "Third trimester"
    #     if strM >9:
    #         trimester = "Post Dated"
    #     return trimester
    # elif lang == 'Hindi':
    #     if '-' in strM:
    #         strM = int(strM.replace('-',''))
    #     else:
    #         strM = int(strM)
    #     if '-' in strD:
    #         strD = int(strD.replace('-',''))
    #     else:
    #         strD = int(strD)


    #     if strM <= 3 and strD == 0:
    #         trimester = "पहली तिमाही"
    #     else:
    #         trimester = "दूसरी तिमाही"
    #     if strM <= 6 and strD == 0:
    #         trimester = "दूसरी तिमाही"
    #     else:
    #         trimester = "Third trimester"

    #     if strM <=9 and strD == 0:
    #         trimester = "तीसरी तिमाही"
    #     else:
    #         trimester = "तीसरी तिमाही"
    #     if strM >9:
    #         trimester = "बाद की तारिक"
    #     return trimester
    # else:
    #     print("Waitng For Other Langugae")



def checkFile(PATH,checkNo,json_object):
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        return False
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(PATH, checkNo+'.json'), 'w+') as db_file:
            db_file.write(json_object)
        return True