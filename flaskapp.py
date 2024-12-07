from flask import Flask
from views import views
from flask_session import Session
#import itemsearching
import os
import redissetup
from dotenv import load_dotenv, dotenv_values 
load_dotenv('info.env') 


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(views,url_prefix="/")
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'your_prefix:'
app.config['SESSION_REDIS'] = redissetup.r

Session(app)

if __name__ == '__main__':
    app.run(debug=True)