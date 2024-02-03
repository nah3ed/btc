import requests
from retrying import retry

def search_bitcoin_address_on_pages(base_url, address, num_pages=2):
    for page_number in range(1, num_pages + 1):
        url = f"{base_url}/page/{page_number}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                # Replace 'your_search_term' with the term you are looking for on the page
                if address in response.text:
                    print(f"Found '{address}' on {url}")
            else:
                print(f"Failed to fetch page {url}. Status code: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {url}: {e}")
            break

if __name__ == "__main__":
    # Replace 'your_bitcoin_address' and 'your_base_url' with the actual values
    search_bitcoin_address_on_pages('https://web.archive.org/web/20230411222154/https://bitcoindat.github.io/#!/page/1', '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm')

