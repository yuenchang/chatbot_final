import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAbZBGmoeocoBAKbix1a1jan4y7mfnd5MCyhjG36Ae3VBSZAV7RyRbAWdeZAwoUdJnTdlBIuSeR9mtcZCJFB2ZCbVC6ZCRuPKQF83NeLqsnLAZCJCJ2OpZCXuw3OlZBusqpe0YplsHkPdDiWE9O8t5oZBHa0AO20WufHh0mdXgxZBpYYAZDZD"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def send_img_message(id, image_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    res = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type":"image",
                "payload":{
                    "url":image_url,
                    "is_reusable": True
                },
            }
        }
    }
    response = requests.post(url, json=res)

    if response.status_code != 200:
        print("Unable to send message: ")
    return response

def send_button_message(id, text, buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons": buttons
                },
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: "+response.text)
    return response

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
