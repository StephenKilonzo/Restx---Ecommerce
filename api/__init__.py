from flask import Flask
from .auth.views import auth_namespace
from .orders.views import order_namespace
from .config.config import config_dict
from .models.orders import Order
from .models.users import User
from .utils import db
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    authorizations={
        "Bearer Auth":{
            'type':"apikey",
            'in':"header",
            'name':"Authorization",
            'description':"Add a JWT with **Bearer &lt;JWT&gt; to authorize"
        }
    }

    api=Api(app,
    title="Ecommerce",
    description="A rest API for for ecommerce customer service",
    authorizations=authorizations,
    security="Bearer Auth"
    )

    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace,path='/auth')

    db.init_app(app)

    jwt=JWTManager(app)

    migrate=Migrate(app,db)

    @app.errorhandler(NotFound)
    def not_found(error):
        return {"error":"Not Found"},404


    @app.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "MethodNotAllowed"},405

    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
            'Order':Order
        }

    return app