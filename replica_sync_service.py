import requests
import os


class ReplicaSyncService:
    __REPLICAS_URLS = ["http://172.18.0.20:5000/", "http://172.18.0.21:5000/"]
    __SYNC_ENDPOINT = "sync/{book_id}"

    def sync_book(self, book_id, request_data):
        current_ip = os.environ.get("SERVER_IP")
        replicas_urls = [_url for _url in self.__REPLICAS_URLS if current_ip not in _url]
        for _url in replicas_urls:
            url = _url + self.__SYNC_ENDPOINT.format(book_id=book_id)
            response = requests.post(url=url, json=request_data)
            if response.status_code >= 400:
                raise Exception("Failed to sync order quantity.")
