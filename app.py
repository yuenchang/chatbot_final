#from bottle import route, run, request, abort, static_file

from fsm import TocMachine

import os, sys
from flask import Flask, request, send_file
from pymessenger import Bot
from io import BytesIO

app = Flask(__name__)
PAGE_ACCESS_TOKEN = "EAAbZBGmoeocoBAKbix1a1jan4y7mfnd5MCyhjG36Ae3VBSZAV7RyRbAWdeZAwoUdJnTdlBIuSeR9mtcZCJFB2ZCbVC6ZCRuPKQF83NeLqsnLAZCJCJ2OpZCXuw3OlZBusqpe0YplsHkPdDiWE9O8t5oZBHa0AO20WufHh0mdXgxZBpYYAZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'state4',
        'state5',
        'state6',
        'state1_1',
        'state7'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1' 
        },
        {
            'trigger': 'advance',
            'source': 'state1_1',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'state1_1',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state4',
            'conditions': 'is_going_to_state4'
        },
        {
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'state5',
            'conditions': 'is_going_to_state5'
        },
        {
            'trigger': 'advance',
            'source': 'state5',
            'dest': 'state6',
            'conditions': 'is_going_to_state6'
        },
        {
            'trigger': 'go_back',
            'source': ['state2','state3', 'state6', 'state7'],
            'dest': 'user'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state1_1',
            'conditions': 'is_going_to_state1_1'
        },
        {
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state7',
            'conditions': 'is_going_to_state7'
        }
        
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'

def log(message):
	print(message)
	sys.stdout.flush()


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    #machine.get_graph().draw('fsm1.png', prog='dot', format='png')
    #return static_file('fsm.png', root='./', mimetype='image/png')
    byte_io = BytesIO()
    machine.get_graph().draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    app.run(debug = True, port = 9990)
