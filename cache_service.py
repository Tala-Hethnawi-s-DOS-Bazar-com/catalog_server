import requests


class CacheService:
    __CACHE_SERVER_URL = "http://172.18.0.40:5000/"
    __CACHE_ENDPOINT = "cache/{book_id}"

    def remove_book_cache(self, book_id):
        url = self.__CACHE_SERVER_URL + self.__CACHE_ENDPOINT.format(book_id=book_id)
        response = requests.delete(url=url)
        if response.status_code >= 400:
            raise Exception("Failed to delete cache.")
