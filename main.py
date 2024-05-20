import requests
import json


def fetch_data(api_url):
    all_data = []
    current_page = 1

    while True:
        response = requests.get(f"{api_url}?page={current_page}")

        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break

        data = response.json()

        if data['status'] != "success":
            print(f"Error in response: {data['message']}")
            break

        page_data = data['data']['data']
        all_data.extend(page_data)

        # Check if there are more pages
        if current_page >= data['data']['current_page']:
            break

        current_page += 1

    return all_data


def save_data_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def identify_response_sources(data):
    for item in data:
        response_text = item['response']
        citations = []
        for source in item['source']:
            if response_text in source['context']:
                citations.append({
                    "id": source['id'],
                    "link": source.get('link', '')
                })
        item['citations'] = citations if citations else []


def main():
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    data = fetch_data(api_url)

    if data:
        identify_response_sources(data)
        save_data_to_json(data, 'fetched_data.json')
        print("Data saved to fetched_data.json")

        # Optionally, print the data for verification
        for item in data:
            print(f"ID: {item['id']}")
            print(f"Response: {item['response']}")
            print(f"Citations: {item['citations']}")
            for source in item['source']:
                print(f"  Source ID: {source['id']}")
                print(f"  Context: {source['context']}")
                if source['link']:
                    print(f"  Link: {source['link']}")
            print("")


if __name__ == "__main__":
    main()
