"""config file

Keyword arguments:
argument -- description
Return: return_description
"""


class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:yin732501242@localhost/test'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:Natalie3399!@database-1.cvlxq8ccnbut.us-east-1.rds.amazonaws.com:3306/recommendation"


APP = Config()
