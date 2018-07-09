from email.message import EmailMessage
from email.parser import BytesParser, Parser
from email.policy import default

def to_json(data):
    msg = Parser(policy=default).parsestr(data)
    print(vars(msg))
    if msg.is_multipart():
        for payload in msg.get_payload():
            print(payload.get_payload())
    else:
        print(msg.get_payload())

if __name__ == "__main__":
    path = input()
    with open(path, 'r', encoding='iso2022_jp') as f:
        data = f.read()
    to_json(data)
