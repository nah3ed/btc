import sys
import requests

print("Addresses Extract from cryptoid.info\n\n")


def extract(coin: str, hash: str):
    url = f"https://chainz.cryptoid.info/explorer/block.txs.dws?coin={coin}&h={hash}.js"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        wallet_amounts = []

        for item in data:
            if "inputs" in item:
                for inputs in item["inputs"]:
                    if isinstance(inputs, dict) and "a" in inputs and "v" in inputs:
                        wallet_amounts.append(f"{inputs['a']} {inputs['v']}")
            if "outputs" in item:
                for output in item["outputs"]:
                    if isinstance(output, dict) and "a" in output and "v" in output:
                        wallet_amounts.append(f"{output['a']} {output['v']}")

        with open("extracted.txt", "w") as file:
            for line in wallet_amounts:
                file.write(line + "\n")

        print(f"{wallet_amounts.__len__()} addresses extracted successfully")
    else:
        print("Failed to make the GET call to the URL.")


def exibir_menu():
    print("Options:")
    print("1. Extract BTC")
    print("2. Extract LTC")
    print("3. Exit")


def main():
    while True:
        exibir_menu()

        opcao = input("Choose an option: ")

        if opcao == "1":
            hash: str = input("hash: ")
            extract("btc", hash)
        elif opcao == "2":
            hash: str = input("hash: ")
            extract("ltc", hash)
        elif opcao == "3":
            sys.exit()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
