# Для локального
#server = '127.0.0.1:3306'
#login = 'root'
#password = 'root'
#db_name = 'workshops_dev' #'workshops_ptc'

# Для удалённого
server = 'j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306'
login = 'vlgfj1uq4cd9bh17'
password = 'm6x73pzfy7jkw1e4'
db_name = 'ng3ltq1ftea03f4d'


class Config:
    SECRET_KEY = '3f0ab93b1fea443496882eff3b6555d5'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'\
                              + login + ':'\
                              + password\
                              + '@' + server\
                              + '/' + db_name + ''

    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'artyom.dubogrej@yandex.ru'
    MAIL_DEFAULT_SENDER = 'artyom.dubogrej@yandex.ru'
    MAIL_PASSWORD = 'chwwsayfpfhxbyfi'
