import requests
import datetime
from collections import defaultdict
import json
from getpass import getpass

CONFIG = {
  "apiKey": "AIzaSyA3EK79yqGOp6nz0x2uiLHxEiN48bjtuHA",
  "authDomain": "visualizer-830ec.firebaseapp.com",
  "databaseURL": "https://visualizer-830ec.firebaseio.com",
  "storageBucket": "visualizer-830ec.appspot.com",
  "project": "visualizer-830ec"
}


class Auth:
    def __init__(self, email: str=None, password: str=None):
        if email is None:
            print('Type email:')
            email=input()
        if password is None:
            print('Type password')
            password=getpass()
        self.email = email
        self.password = password
        self.post_data = defaultdict()
        self.post_data['email'] = self.email
        self.post_data['password'] = self.password
        self.post_data['returnSecureToken'] = True
        self.headers = {"Content-Type": "application/json"}
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + CONFIG['apiKey']
        payload = {"email": email, "password": password, "returnSecureToken": True}
        rsp = requests.post(url, data=payload)
        self.id_token = rsp.json().get("idToken")

        # User idToken from your auth for later requests
        self.headers = {
          'Content-type': 'application/json',
          'Authorization': "Bearer %s" % self.id_token
        }
        self.model_reference = None
        self.name = None
        self.description = None

    def add_model(self, name: str, description: str):
        url = "https://firestore.googleapis.com/v1beta1/projects/"\
              + CONFIG['project']\
              + "/databases/(default)/documents/models"
        payload = {
          "fields": {
            "name": {"stringValue": name},
            "description": {"stringValue": description}
          }
        }
        # Create Doc
        rsp = requests.post(url, headers=self.headers, data=json.dumps(payload))
        assert (rsp.status_code == 200)
        model_reference = rsp.json().get("name")
        self.model_reference = model_reference
        self.name = name
        self.description = description

    def add_accuracy(self, x, y):
        url = "https://firestore.googleapis.com/v1beta1/" + self.model_reference
        current_date = datetime.datetime.now()
        current_date = current_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = {
          "fields": {
            "name": {"stringValue": self.name},
            "description": {"stringValue": self.description},
            "x": {
              "arrayValue": {
                "values": [

                ]
              }
            },
            "y": {
              "arrayValue": {
                "values": [

                ]
              }
            },
            "createdAt": {
              "timestampValue": str(current_date)
            }


          }
        }
        for x_ in x:
            payload['fields']['x']['arrayValue']['values'].append({'doubleValue': str(x_)})
        for y_ in y:
            payload['fields']['y']['arrayValue']['values'].append({'doubleValue': str(y_)})
        rsp = requests.patch(url, headers=self.headers, data=json.dumps(payload))
        assert (rsp.status_code == 200)