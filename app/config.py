import os
basedir = os.path.abspath(os.path.dirname(__file__))
#print(basedir)
class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #print(os.path.join(basedir, 'prints.db'))
    #db_dir = (BASE_DIR + '\\PupilPremiumTable.db')
    
#/home/remoteprinter/Documentos/printAuto/prints.db