import os
import requests
import ast
import json

class WhatsAppWrapper:

    API_URL = "https://graph.facebook.com/v13.0/"
    # API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
    API_TOKEN = 'EAAMZArIrPKxMBAC1MbHDipcCbMfyeF93iPgTG4fnPvnQfXghEelFZCUkow2t5jjQSqO7gPMThLYbU5DWIEZBBXetyZCP0bQJ0srIsPhRVzl6pzo7A5T3VomZCFlW3RCYRjLsA5UfUCWTrQks9IIxpxVLVDVhzlOxyjmul2ZAsgRmAEADM9DdjM80Hw0heVX3PhI0d3K8E12wZDZD'
    
    # NUMBER_ID = os.environ.get("WHATSAPP_NUMBER_ID")
    #NUMBER_ID = '102098082798609'
    NUMBER_ID  = '103423489386148'
    print(API_TOKEN)
    print(NUMBER_ID)

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = str(self.API_URL) + str(self.NUMBER_ID)

    def send_template_message(self, template_name, language_code, phone_number):
        print("Comming")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"

        return response.status_code


    def send_image_message(self,phone_number,imageID):
    
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": phone_number,
          "type": "image",
          "image": {
            "id": imageID
          }
        })
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"

        return response.status_code

    def send_document_message(self,phone_number,imageID,docCaption,filName):
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": phone_number,
          "type": "document",
          "document": {
            "id": imageID,
            "caption": docCaption,
            "filename": filName
          }
        })
        print("payload",payload)

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"

        return response.status_code












    def send_text_msg(self, msg, phone_number):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",msg,phone_number)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": msg
            }
            })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"

        return response.status_code


    def send_media_msg(self,templateName,mediaID, phone_number,langCode='en'):
        print("AAAAASWEE",templateName,mediaID, phone_number)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
            "name": templateName,
            "language": {
                "code": langCode,
                "policy": "deterministic"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                        "type": "image",
                        "image": {"id": mediaID}
                        }]
                }
            ]
            }})
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code




    def sendMsgForConfirmation(self, msg, phone_number,type1,type2):
        print("YUYUYUYUYUUYUYU^^%&^&",type1,type2)

        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": phone_number,
          "type": "interactive",
          "interactive": {
            "type": "button",
            "body": {
              "text": msg
            },
            "action": {
              "buttons": [
                {
                  "type": "reply",
                  "reply": {
                    "id": type1,
                    "title": type1
                  }
                },
                {
                  "type": "reply",
                  "reply": {
                    "id": type2,
                    "title": type2
                  }
                }
              ]
            }
          }
        })
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code



    def send_media_msg_without_params(self,templateName,mediaID, phone_number,langCode):
        print("AAAAASWEE",templateName,mediaID, phone_number)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
            "name": templateName,
            "language": {
                "code": langCode,
                "policy": "deterministic"
            }
            }})
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code


    def send__msg_button_without_media(self,templateName, phone_number,langCode):
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "to": phone_number,
          "type": "template",
          "template": {
            "name": templateName,
            "language": {
              "code": langCode,
              "policy": "deterministic"
            }
          }
        })

        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code



    def interactivte_reply(self,templateData, phone_number,lableText1,lableText2):
        print("#######################")
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": phone_number,
          "type": "interactive",
          "interactive": {
            "type": "button",
            "body": {
              "text": templateData
            },
            "action": {
              "buttons": [
                {
                  "type": "reply",
                  "reply": {
                    "id": lableText1,
                    "title": lableText1
                  }
                },
                {
                  "type": "reply",
                  "reply": {
                    "id": lableText2,
                    "title": lableText2
                  }
                }
              ]
            }
          }
        })
        print("payload",payload)
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code



    def interactivte_reply_one_button(self,templateData, phone_number,lableText1,lableText2,lableText3):
        print("#######################")
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "recipient_type": "individual",
          "to": phone_number,
          "type": "interactive",
          "interactive": {
            "type": "button",
            "body": {
              "text": templateData
            },
            "action": {
              "buttons": [
                {
                  "type": "reply",
                  "reply": {
                    "id": lableText1,
                    "title": lableText1
                  }
                },
                {
                  "type": "reply",
                  "reply": {
                    "id": lableText2,
                    "title": lableText2
                  }
                },
                {
                  "type": "reply",
                  "reply": {
                    "id": lableText3,
                    "title": lableText3
                  }
                }
              ]
            }
          }
        })
        print("payload",payload)
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code


    def interactivte_reply_list(self,templateData,bodyText, phone_number,buttonClickName):
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        payload = json.dumps({
                  "messaging_product": "whatsapp",
                  "recipient_type": "individual",
                  "to": phone_number,
                  "type": "interactive",
                  "interactive": {
                    "type": "list",
                    "body": {
                      "text": bodyText
                    },
                    "action": {
                      "button": buttonClickName,
                      "sections": templateData
                    }
                  }
                })
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"
        return response.status_code





    def send_media_url(self, msg,msgUrl, phone_number):
        payload = json.dumps({
          "messaging_product": "whatsapp",
          "to": phone_number,
          "text": {
            "preview_url": True,
            "body": msg + msgUrl
          }
        })
        response = requests.request("POST", f"{self.API_URL}/messages", headers=self.headers, data=payload)
        print("response",response)
        assert response.status_code == 200, "Error sending message"

        return response.status_code












    def process_webhook_notification(self, data):
        """_summary_: Process webhook notification
        For the moment, this will return the type of notification
        """
        print("UIYJI",data)
        response = []
        try:
            for entry in data["entry"]:
                print("HI")
                # msgtext = ""
                for change in entry["changes"]:
                    print("Type::",change["field"])
                    print("Checking Value",change["value"])
                    if "messages" in change["value"]:
                        print("OOOOOOOO",change["value"]['messages'][0]['type'],type(change["value"]['messages'][0]['type']),len(change["value"]['messages'][0]['type']))
                        if change["value"]['messages'][0]['type'] == 'button':
                            print("IIIIIIIIIIIIIIII")
                            response.append(
                                {
                                    "display_phone_number": change["value"]["metadata"]["display_phone_number"],
                                    "msg_text": change["value"]["messages"][0]['button']['text'],
                                    "msg_type": change["value"]["messages"][0]["type"],
                                    "timestamp": change["value"]["messages"][0]["timestamp"],
                                    "from": change["value"]["messages"][0]["from"],
                                    "contacts": change["value"]["contacts"][0]["profile"]["name"],
                                    "wa_id": change["value"]["contacts"][0]["wa_id"]
                                }
                            )
                        elif change["value"]['messages'][0]['type'] == "text":
                            print("KKKKKKKKKKK")
                            response.append(
                                {

                                    "display_phone_number": change["value"]["metadata"]["display_phone_number"],
                                    "msg_text": change["value"]["messages"][0]["text"]["body"],
                                    "msg_type": change["value"]["messages"][0]["type"],
                                    "timestamp": change["value"]["messages"][0]["timestamp"],
                                    "from": change["value"]["messages"][0]["from"],
                                    "contacts": change["value"]["contacts"][0]["profile"]["name"],
                                    "wa_id": change["value"]["contacts"][0]["wa_id"]
                                }
                            )
                        elif change["value"]['messages'][0]['type'] == "interactive" and change["value"]['messages'][0]['interactive']['type'] == "button_reply":
                            response.append(
                                {

                                    "display_phone_number": change["value"]["metadata"]["display_phone_number"],
                                    "msg_text": change["value"]["messages"][0]["interactive"]["button_reply"]["id"],
                                    "msg_type": change["value"]["messages"][0]["type"],
                                    "timestamp": change["value"]["messages"][0]["timestamp"],
                                    "from": change["value"]["messages"][0]["from"],
                                    "contacts": change["value"]["contacts"][0]["profile"]["name"],
                                    "wa_id": change["value"]["contacts"][0]["wa_id"]
                                }
                            )
                        elif change["value"]['messages'][0]['type'] == "interactive" and change["value"]['messages'][0]['interactive']['type'] == "list_reply" :
                            response.append(
                                {

                                    "display_phone_number": change["value"]["metadata"]["display_phone_number"],
                                    "msg_text": change["value"]["messages"][0]["interactive"]["list_reply"]["title"],
                                    "msg_type": change["value"]["messages"][0]["type"],
                                    "timestamp": change["value"]["messages"][0]["timestamp"],
                                    "from": change["value"]["messages"][0]["from"],
                                    "contacts": change["value"]["contacts"][0]["profile"]["name"],
                                    "wa_id": change["value"]["contacts"][0]["wa_id"]
                                }
                            )
                        else:
                            print("Comming Here")
                        pass
                    else:
                        print("No Response Message Here ...")
            print("JHGVHJVJVFJHV",response)
            return response
        except:
            response = []
            return response




























































