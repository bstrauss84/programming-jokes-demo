from flask import Flask, render_template
import random
import os

app = Flask(__name__)

jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why do Java developers wear glasses? Because they don't C#.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    "Why did the developer go broke? Because he used up all his cache."
]

@app.route('/')
def home():
    app_version = os.getenv('APP_VERSION', '1.0')  # Get the APP_VERSION or default to '1.0'
    return render_template('index.html', joke=random.choice(jokes), app_version=app_version)

@app.route('/joke')
def joke():
    return random.choice(jokes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
