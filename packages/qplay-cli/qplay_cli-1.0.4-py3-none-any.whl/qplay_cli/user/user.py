import requests
import json
from qplay_cli.qplay_config import QplayConfig

class User:
    SIGNIN_URL = 'https://s5y92z0788.execute-api.ap-south-1.amazonaws.com/prod/signin'
    SIGNUP_URL = 'https://s5y92z0788.execute-api.ap-south-1.amazonaws.com/prod/signup'
    CONFIRM_SIGNUP = 'https://s5y92z0788.execute-api.ap-south-1.amazonaws.com/prod/confirm_signup'
    
    def __init__(self):
        pass
    
    def signup(self, username, name, email, password):
        x = requests.post(
            User.SIGNUP_URL, 
            data = json.dumps(
                {
                    'username' : username,
                    'password' : password,
                    "email" : email,
                    "name" : name
                    
                }))
        response = json.loads(x.text)
        
        if response['error'] == True:
            print(response['message'])
            quit()
        
        return response
    
    def confirm_signup(self, username, password, code):
        x = requests.post(
            User.CONFIRM_SIGNUP, 
            data = json.dumps(
                {
                    'username' : username,
                    'password' : password,
                    "code" : code
                    
                }))
        response = json.loads(x.text)
        
        if response['error'] == True:
            print(response['message'])
            quit()
        
        return response
    
    def signin(self, username, password):
        x = requests.post(User.SIGNIN_URL, data =json.dumps({'username' : username, 'password' : password}))
        
        credentials = QplayConfig.get_credentials()
        credentials['DEFAULT']['access_token'] = json.loads(x.text)['data']['access_token']
        with open('{}/config'.format(QplayConfig.config_path), 'w') as configfile:
            credentials.write(configfile)
