from email.message import EmailMessage
from email.parser import BytesParser, Parser
from email.policy import default
import json

def to_json(data):
    msg = Parser(policy=default).parsestr(data)
    ans = {k:msg[k] for k in msg.keys()}
    ans['body'] = {}
    if msg.is_multipart():
        for i, payload in enumerate(msg.get_payload()):
            ans['body'][i] = payload.get_payload()
    else:
        ans['body'][0] = msg.get_payload()
    return json.dumps(ans, indent=4)

if __name__ == "__main__":
    path = input()
    with open(path, 'r', encoding='iso2022_jp') as f:
        data = f.read()
    ans = to_json(data)
    print(ans)
