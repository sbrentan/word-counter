from flask import Flask
app = Flask(__name__ , static_folder='static', static_url_path='/static')
from app import views

# if __name__ == "__main__":
# 	app.run()