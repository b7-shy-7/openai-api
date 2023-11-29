# from flask import Flask, render_template

# app = Flask(__name__)

# name = 'Grey Li'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]

# @app.route('/')
# def index():
#     return render_template('index.html', name=name, movies=movies)

# if __name__  == '__main__':
#     app.run()
import openai
from openai import OpenAI
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import json
client = OpenAI()

from flask import Flask,jsonify,request, Response

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    message = request.form['message']
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # response_format={ 'type': "json_object"},
        messages=[
            {"role": "system", "content": "you are a hospitable and knowledgable helper"},
            # {"role": "user", "content": message},
            # {"role": "assistant", "content": history},
            {"role": "user", "content": message}
        ]
        # seed = 1000000
        # stream = True
    )

    def generate():
        for trunk in message:
            yield json.dumps(trunk) + '\\n'

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return completion.choices[0].message.content

    # return Response(generate(), mimetype="text/event-stream", headers=headers)


if __name__ == '__main__':
    app.run()