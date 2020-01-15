from requests import put, get, post
import json

"""
data = {
    'card' : {
        type : <Card type>,
        name : <text>
        hp : <text if applicable>,
        mana : <text if applicable>,
        pwr : <text if applicable>,
        card_text : <text with formatting>,
        lvl_up_text : <text with formatting>,
        tribe : <text>,
        region : <text>,
        keywords : [],
        image : <blob of image data>
    }
}
"""
data = {
    'hp':'7',
    'mana':'17',
    'pwr':'1000',
    'type':'unit_common',
    'card_text':'When I die, give me <k>barrier</k> and summon a <b>cool spider</b> in attack mode',
    'lvl_up_text':'I have seen 3 units survive damage',
    'tribe':'elite',
    'region':'ionia'
}

headers = {'Content-type': 'application/json'}

response = get('http://127.0.0.1:5000/api/session')
cookies = response.cookies
print(response.text)
response = get('http://127.0.0.1:5000/api/session',
                cookies=cookies,
                headers=headers
                )
print(response.cookies)
print(response.text)
response = post('http://127.0.0.1:5000/api/session/card',
                cookies=cookies,
                headers=headers,
                data=json.dumps(data)
                )
print(response.cookies)
print(response.text)
