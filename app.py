from flask import Flask
from modules.playlist import playlist


app = Flask(__name__)
app.register_blueprint(playlist, url_prefix='/playlist')

app.run(debug=True)