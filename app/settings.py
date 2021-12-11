import json

class Secret():
    """ This is the class to obtain confidential data because of the performance"""
    def __init__(self):
        " As intial value return the json file in order to acces to its information"
        with open("secret.json") as f:
            self.secret = json.loads(f.read())
            def get_secret(secret_name, secrets=self.secret):
                try:
                    return secrets[secret_name]
                except:
                    msg = "la variable %s no existe" % secret_name
                    raise (msg)
            
        self.host = get_secret('host')
        self.database = get_secret('database')
        self.user = get_secret('user')
        self.password = get_secret('password')
                
secret = Secret()