import time

from flask import Flask, request, abort

app = Flask(__name__)


# Тестовая инфа вместо настоящей базы данных.
db = [
    {
        'name': 'Jack',
        'text': 'Привет всем',
        'time': time.time(),
    }, {
        'name': 'Mary',
        'text': 'Привет Jack',
        'time': time.time(),
    }
]


@app.route('/')
def hello():
    return "Hello, Word"


@app.route('/status')
def status():
    return {
        'status': True,
        'name': 'SkillBox Messager',
        'time': time.now()
    }


@app.route('/send', methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')

    if not (isinstance(name, str)
            and isinstance(text, str)
            and name
            and text):
        return abort(400)

    new_messege = {
        'name': name,
        'text': text,
        'time': time.time(),
    }
    db.append(new_messege)

    return {'ok': True}


@app.route('/messages')
def get_messages():
    """Возвращает те сообщения которых ранеше не получали"""
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)

    return {
        'messages': messages
    }


if __name__ == '__main__':
    app.run()
