from time import sleep
from bs4 import BeautifulSoup
import requests
import json


BASE_URL = "https://www.whatdotheyknow.com"
SHEFFIELD_CITY_URL = BASE_URL + "/body/sheffield_city_council"


def get_requests_on_page(url):
    """
    This function takes a URL and returns a list of all the FOI requests on this page
    """
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select(".request_listing .request_left .head a")
        links = [link["href"] for link in links if "href" in link.attrs]
        foi_links = []
        for foi_link in links:
            foi_link = BASE_URL + foi_link.split("#")[0]
            foi_links.append(foi_link)
        return foi_links
    return []


def get_foi_request_json(url):
    json_url = url + ".json"
    json_response = requests.get(json_url, timeout=5)
    if json_response.status_code == 200:
        return json_response.json()
    else:
        json_response.raise_for_status()


def get_foi_request_events(feed_data):
    result = []
    request_events = feed_data.get("info_request_events", [])
    for event in request_events:
        e = {
            "created_at": event.get("created_at"),
        }
        incoming_message_id = event.get("incoming_message_id")
        outgoing_message_id = event.get("outgoing_message_id")

        if not incoming_message_id and not outgoing_message_id:
            continue
        if incoming_message_id:
            e["message_id"] = incoming_message_id
            e["type"] = "incoming"
        elif outgoing_message_id:
            e["message_id"] = outgoing_message_id
            e["type"] = "outgoing"
        result.append(e)
    return result


def get_event_messages(url, events):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for event in events:
        event_element = soup.select(
            f"#{event['type']}-{event['message_id']} .correspondence_text"
        )
        event["content"] = "\n".join(element.get_text(separator="\n", strip=True) for element in event_element)


def save_foi_request(url):
    foi_request_data = get_foi_request_json(url)
    feed_events = get_foi_request_events(foi_request_data)
    get_event_messages(url, feed_events)
    foi_request_data_with_events = {
        "id": foi_request_data["id"],
        "title": foi_request_data["title"],
        "display_status": foi_request_data["display_status"],
        "law_used": foi_request_data["law_used"],
        "url_title": foi_request_data["url_title"],
        "created_at": foi_request_data["created_at"],
        "events": feed_events,
    }
    with open(f"sample_foi_requests/{foi_request_data['url_title']}.json", "w") as f:
        json.dump(foi_request_data_with_events, f, indent=4)


def main():
    try:
        page = 1
        while True:
            page_url = get_requests_on_page(SHEFFIELD_CITY_URL + f"?page={page}")
            for request_url in page_url:
                save_foi_request(request_url)
            print(f"Saved page {page} of FOI requests")
            page += 1
            sleep(5)
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")


if __name__ == "__main__":
    main()
