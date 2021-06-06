# Для локального
#server = '127.0.0.1:3306'
#login = 'root'
#password = 'root'
#db_name = 'workshops_ptc'

# Для удалённого
server = '109.95.210.183'
login = 'u108692_application'
password = '8Dr-Ytd-Diz-arJ'
db_name = 'u108692_workshops_ptc'


class Config:
    SECRET_KEY = '3f0ab93b1fea443496882eff3b6555d5'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'\
                              + login + ':'\
                              + password\
                              + '@' + server\
                              + '/' + db_name + ''
