from transitions.extensions import GraphMachine
from utils import send_text_message
from utils import send_img_message
from utils import send_button_message
import requests
from bs4 import BeautifulSoup
import socket
import sys
import os
import time
import os.path
from math import radians, cos, sin, asin, sqrt

#web
URL = 'http://course-query.acad.ncku.edu.tw/qry/' 

def get_web_page(url):
    #resp
    resp = requests.get(url)
    resp.encoding = 'big-5'

    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    #articles  
    titlelist = [] 
    hreflist = [] 
    divs = soup.find_all('div', 'dept')
    for d in divs:
        if d.find('a'):
            title = d.find('a').string
            href = d.find('a')['href']
            titlelist.append(title)
            hreflist.append(URL + href)
    articles = dict(zip(titlelist, hreflist))
    return articles

#distance
def placeLAtLong(address):
    print('Google API Start ->', end = ' ')
    api_key = "AIzaSyBmShn3UEM3v7I6yStl1MHgMgwRLjWZ2x4"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        latitude = api_response_dict['results'][0]['geometry']['location']['lat']
        longitude = api_response_dict['results'][0]['geometry']['location']['lng']
        print ('Latitude:'+str(latitude), end=' ')
        print ('Longitude:'+ str(longitude))
        tmp = []
        tmp.append(latitude)
        tmp.append(longitude)
        print('Google API finish')
        return tmp
def haversine(lon1, lat1, lon2, lat2): 
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 
    return c * r * 1000

#state
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_state1(self, event):
        if event.get("message"):
            return True
        return False
    
    def is_going_to_state1_1(self, event):
        if event.get("postback"):
            text_ = event['postback']['payload']
            if text_ == 'I want to check course catalog!!!':
                return True
            else:
                return False
        return False

    def is_going_to_state2(self, event):
        if event.get("message"):
            text_ = event['message']['text']
            if text_ == 'all':
                return True
            else:
                return False
        return False
    
    def is_going_to_state3(self, event):
        if event.get("message"):
            global mayjor 
            mayjor = event['message']['text']
            if mayjor!='all':
                return True
            else:
                return False
        return False
    def is_going_to_state4(self, event):
        if event.get("postback"):
            text_ = event['postback']['payload']
            if text_ == 'How far is it to NCKU?':
                return True
            else:
                return False
        return False
    def is_going_to_state5(self, event):
        if event.get("message"):
            global from_
            from_ = event['message']['text']
            return True
        return False
    def is_going_to_state6(self, event):
        if event.get("message"):
            global to_
            if event['message']['text'] == '1':
                to_ = '成大 力行校區'
            elif event['message']['text'] == '2':
                to_ = '成大 成杏校區'
            elif event['message']['text'] == '3':
                to_ = '成大 敬業校區'
            elif event['message']['text'] == '4':
                to_ = '成大 光復校區'
            elif event['message']['text'] == '5':
                to_ = '成大 成功校區'
            elif event['message']['text'] == '6':
                to_ = '成大 自強校區'
            elif event['message']['text'] == '7':
                to_ = '成大 勝利校區'
            elif event['message']['text'] == '8':
                to_ = '成大 東寧校區'
            return True
        return False
    
    def is_going_to_state7(self, event):
        if event.get("postback"):
            text_ = event['postback']['payload']
            if text_ == 'Hand me the map~':
                return True
            else:
                return False
        return False
##############################################################################
    def on_enter_state1(self, event):
        print("I'm entering state1")
        sender_id = event['sender']['id']
        buttons = [
            {
                "type":"postback",
                "title":"check course catalog",
                "payload":"I want to check course catalog!!!"
            },
            {
                "type":"postback",
                "title":"caculate the distanece to NCKU",
                "payload":"How far is it to NCKU?"
            },
            {
                "type":"postback",
                "title":"view the map of NCKU",
                "payload":"Hand me the map~"
            }
            
        ]
        responese = send_button_message(sender_id, "choose one service :", buttons)
        
    def on_enter_state1_1(self, event):
        print("I'm entering state1_1")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "if you want to check all departments, enter 'all'\n\nOr type in any department to get a specific one")

    def on_enter_state2(self, event):
        print("I'm entering state2")
        page = get_web_page('http://course-query.acad.ncku.edu.tw/qry/')
        current_articles = get_articles(page)
        whole_depr = ""
        for key in current_articles.keys():
            depr = str(key)+"\n"
            whole_depr = whole_depr + depr
        sender_id = event['sender']['id']
        send_text_message(sender_id, str(whole_depr))
        self.go_back()
        
    def on_enter_state3(self, event):
        flag = 0
        print("I'm entering state3")
        page = get_web_page('http://course-query.acad.ncku.edu.tw/qry/')
        current_articles = get_articles(page)
        for key in current_articles.keys():
            if str(key.split()[2]) == "）" + mayjor:
                flag = 1
                sender_id = event['sender']['id']
                send_text_message(sender_id, str(current_articles[key]))
                break
        if flag == 0:
            sender_id = event['sender']['id']
            send_text_message(sender_id, "cannot find this department")
        self.go_back()

    def on_enter_state4(self, event):
        print("I'm entering state4")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Where do you want to go FROM ?")
        
    def on_enter_state5(self, event):
        print("I'm entering state5")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "Where do you want to go TO ?\n'1' :力行校區\n'2' :成杏校區\n'3' :敬業校區\n'4' :光復校區\n'5' :成功校區\n'6' :自強校區\n'7' :勝利校區\n'8' :東寧校區")
        
    def on_enter_state6(self, event):
        print("I'm entering state6")
        forpm25LatLong = placeLAtLong(from_)
        print(forpm25LatLong)
        forpm25LatLong2 = placeLAtLong(to_)
        print(forpm25LatLong2)
        ans = haversine(forpm25LatLong[1],forpm25LatLong[0],forpm25LatLong2[1], forpm25LatLong2[0])
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, 'distance between two locations is '+str(ans)+'m\n\n'+'you might have to walk '+ str(ans/90.5) + ' to ' + str(ans/62.5) + ' min')
        #62.5m/min~90.5m/min
        self.go_back()

    def on_enter_state7(self, event):
        print("I'm entering state7")
        sender_id = event['sender']['id']
        responese = send_img_message(sender_id, "https://i.imgur.com/LMagZUl.jpg")
        self.go_back()
##############################################################
    def on_exit_state2(self):
        print('Leaving state2')
        
    def on_exit_state3(self):
        print('Leaving state3')
