import requests
from django.conf import settings
from typing import List, Dict, Any, Optional

class InstagramClient:
    BASE_URL = "https://graph.instagram.com"

    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id

    def _get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Базовый GET-запрос к API Instagram."""
        if params is None:
            params = {}

        params['access_token'] = self.access_token

        url = f"{self.BASE_URL}/{endpoint}"


        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Базовый POST-запрос к API Instagram."""
        if data is None:
            data = {}

        data['access_token'] = self.access_token

        url = f"{self.BASE_URL}/{endpoint}"

        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    def get_user_media(self) -> List[Dict[str, Any]]:
        """
        Получить все медиа-объекты пользователя с обработкой пагинации.
        Возвращает список словарей с данными медиа.
        """
        all_media = []
        endpoint = f"{self.user_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp'
        }

        while True:
            data = self._get(endpoint, params)
            all_media.extend(data.get('data', []))

            paging = data.get('paging', {})
            next_url = paging.get('next')
            if not next_url:
                break

            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()

        return all_media

    def post_comment(self, instagram_media_id: str, text: str) -> Dict[str, Any]:
        """
        Отправить комментарий к медиа в Instagram.
        Возвращает ответ API (обычно {'id': 'comment_id'}).
        """
        endpoint = f"{instagram_media_id}/comments"
        data = {'message': text}
        return self._post(endpoint, data)