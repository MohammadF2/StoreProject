from Server.CustomerManagement import CustomerManagement
from CartManagment import *

app = flask.Flask(__name__)
app.register_blueprint(CartManagement, url_prefix='/cart_management')
app.register_blueprint(CustomerManagement, url_prefix='/customer_management')

app.run(host='127.0.0.1', port=5000, debug=True)
