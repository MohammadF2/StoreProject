import flask

from Server.Blueprints.Checkout import Checkout
from Server.Blueprints.CustomerManagement import CustomerManagement
from Server.Blueprints.CartManagment import CartManagement
from Server.Blueprints.Orders import orders
from waitress import serve
from config.config import RUN_AS, DEBUG, PORT, ip, PRODUCTION, PROJECT_NAME


__name__ = PROJECT_NAME

app = flask.Flask(__name__)
app.register_blueprint(CartManagement, url_prefix='/cart_management')
app.register_blueprint(CustomerManagement, url_prefix='/customer_management')
app.register_blueprint(orders, url_prefix='/orders')
app.register_blueprint(Checkout, url_prefix='/')

if RUN_AS == PRODUCTION:
    serve(app, host=ip, port=PORT)
else:
    app.run(host=ip, port=PORT, debug=DEBUG)
