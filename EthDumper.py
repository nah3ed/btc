import requests
import json
import time


def get_transaction_data():
    url = "https://api2.ethplorer.io/getTokenHistory"
    params = {
        "apiKey": "ethplorer.widget2",
        "domain": "https://ethplorer.io/last",
        "type": "transfer",
        "limit": 1000,
        "ts": int(time.time()),
    }

    headers = {
        "cookie": "_wui=5ecb7c3b1; lang=en; _fbp=fb.1.1704768988233.1507256553; _gid=GA1.2.1532976294.1704768988; __gads=ID=561f6ee9f9a7f15f:T=1704769014:RT=1704769014:S=ALNI_MbMG3aeEuyPamZya_rV0PxM9PWnLg; __gpi=UID=00000a06efab895c:T=1704769014:RT=1704769014:S=ALNI_MaMBDCudpOi_P4hlbXBWU6dRtW6Mw; cto_bundle=Lssog18lMkIwR3doODhHU2dmNGpDNkVhUlhqQ2lNZ01IbmIxWmNXVGlNUlFobUZzaFhGdlllJTJCSmJGUW5WdjBlTFFlQ2dvNzY1Q0olMkJyYXVUbGNhNnUlMkZoVmt3ZVIlMkJyYWE4eVNxNCUyQkszQ0F5TnNEWFFPVHYlMkZab2FWQzF5RHNCaHlpZDFIa081WWU3UkhSWllMZmFvYWYzaVUxZmd4RmFlVlklMkJpcVhHMUMwNU5ETkhadCUyRnhvWkRSb2dmM3ZTakVtYlAlMkYza2VsNmN0bHlMMUtNWWhEQWk1eCUyQk9iaUJiQSUzRCUzRA; _ga=GA1.1.338223699.1704768988; _hjAbsoluteSessionInProgress=1; _ga_6GY5R575PZ=GS1.1.1704768988.1.1.1704769762.60.0.0"
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return data["operations"] if "operations" in data else []


def save_from_file(sender, filename="addresses.txt"):
    with open(filename, "a") as file:
        file.write(f"{sender}\n")


def save_to_file(receiver, filename="addresses.txt"):
    with open(filename, "a") as file:
        file.write(f"{receiver}\n")


def main():
    existing_addresses = set()

    while True:
        transactions = get_transaction_data()

        for transaction in transactions:
            sender = transaction["from"]
            receiver = transaction["to"]

            if sender not in existing_addresses:
                save_from_file(sender)
                existing_addresses.add(sender)

            if receiver not in existing_addresses:
                save_to_file(receiver)
                existing_addresses.add(receiver)
        print(f"Total Saved: {existing_addresses.__len__()}")
        time.sleep(15)


if __name__ == "__main__":
    main()
