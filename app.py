from flask import Flask
from os import environ
from config import DevConfig, PrdConfig


app = Flask(__name__)

if environ.get("FLASK_ENV") == "dev":
    app.config.from_object(DevConfig())
else:
    app.config.from_object(PrdConfig())

@app.route('/')
def hello():
    msg = ""
    for key, val in app.config["DB"].items():
        msg += f"{key}={val}\n"
    msg += f"{app.config['DB_URI']}"
    return msg
    
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
    print(app.config["DB_IP"])
    