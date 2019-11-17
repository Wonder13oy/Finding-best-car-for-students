from flask import Flask, render_template, request
from pusher import Pusher

app = Flask(__name__)

# CONFIGURE PUSHER OBJECT
pusher = Pusher(
    app_id = "897146",
    key = "666138d1b968d88eb26a",
    secret = "b2c0cebe684e29d8d8d2",
    cluster = "mt1",
    ssl=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    pusher.trigger(u'message', u'send', {
        u'name': data['name'],
        u'message': data['message']
    })
    return 'message sent'

@app.route('/customer', methods=['POST'])
def customer():
    data = request.form
    pusher.trigger(u'customer', u'add', {
        u'name': data['name'],
        u'position': data['position'],
        u'office': data['office'],
        u'age': data['age'],
        u'salary': data['salary']
    })
    return 'customer added'

if __name__ == '__main__':
    app.run(debug=True)