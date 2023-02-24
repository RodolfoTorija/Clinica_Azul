class Config:
    SECRET_KEY = 'fcea920f7412b5da7be0cf42b8c93759'


class DevelopmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Zeromainj0.'
    MYSQL_DB = 'clinica_azul'

config={
    'development': DevelopmentConfig
}
