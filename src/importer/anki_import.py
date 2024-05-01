import json
import uuid
import urllib.request

base_url='http://127.0.0.1:8765'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(base_url, requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def import_card(question_svg, answer_svg):
    print("importing card")
    svg_file = f"texflash_{uuid.uuid4()}.svg"
    store_svg = {
            "action": "storeMediaFile",
            "params": {
                "filename": svg_file,
                "path" : answer_svg
                }
            }

    create_note = {
            "action": "addNote",
            "params": {
                "note": {
                    "deckName": "Default", 
                    "modelName": "Basic", 
                    "fields": { 
                               "Front": "question coming soon", 
                               "Back": f"<img src={svg_file}>" 
                               }, 
                    "tags": []
                    }
                }
            }

    my_params = { "actions": [ store_svg, create_note ] }
    print(my_params)
    print(invoke('multi', **my_params))

# result = invoke('deckNames')
# print('got list of decks: {}'.format(result))
