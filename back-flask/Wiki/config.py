from dotenv import load_dotenv, dotenv_values
import os


load_dotenv()

config = {
        **os.environ,
#        **dotenv_values(".env.secret"),
#        **dotenv_values(".env.shared")
        }

# General Config
class Config:
    ENVIRONMENT = "developmnet"
    FLASK_APP = "DeepCluster"
    MONGO_URI = config['DB_URI']
    
class ProdConfig(Config):
    FLASK_ENV = "production"
    FLASK_DEBUG = False

class DevConfig(Config):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
