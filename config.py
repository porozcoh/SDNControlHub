class Config:
    SECRET_KEY = '3d6f45a5fc12445dbac2f59c3b6c7cb1'


class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST= 'localhost'
    MYSQL_USER= 'root'
    MYSQL_PASSWORD = 'progra2010'
    MYSQL_DB = 'Redes'


config = {
    'development':DevelopmentConfig
}