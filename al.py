from pya3 import *
username=open('username.txt','r').read()
api_key=open('api_key.txt','r').read()
alice=Aliceblue(username,api_key)
alice.get_session_id()['sessionID']
get_profile_response=alice.get_profile()
print(alice.get_profile()) # get profile