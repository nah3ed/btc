import requests;n=input('Number:');r=requests.post('https://webapi.robi.com.bd/v1/account/register/otp',headers={"Authorization":"Bearer a.a.a"},data={"phone_number":n});print('Send\n'if r.status_code==200 else'Error\n')
