import requests
import json

class Instance:
    
    LAUNCH_MACHINE_URL = "https://h5y8burhuk.execute-api.ap-south-1.amazonaws.com/prod/launch_instance"
    def __init__(self):
        pass
    
    def launch_machine(self, access_token, lease_time):
        x = requests.post(
            Instance.LAUNCH_MACHINE_URL, 
            data = json.dumps(
                {
                    "access_token": str(access_token),
                    "lease_time": str(lease_time)
                }))
        response = json.loads(x.text)
        
        if response['error'] == True:
            print(response['message'])
            quit()
        
        return response