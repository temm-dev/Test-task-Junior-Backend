from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
from .models import Post
from django.urls import reverse
from rest_framework import status

class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаём тестовый пост в БД
        self.post = Post.objects.create(
            instagram_id='12345',
            caption='Test post',
            media_type='IMAGE',
            media_url='http://example.com/img.jpg',
            permalink='http://instagram.com/p/12345',
            timestamp='2023-01-01T00:00:00Z'
        )
        self.valid_payload = {'text': 'Test comment'}

    @patch('instagram.views.InstagramClient.post_comment')
    def test_create_comment_success(self, mock_post_comment):
        mock_post_comment.return_value = {'id': 'comment_123'}

        url = reverse('post-add-comment', args=[self.post.id])
        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Test comment')
        self.assertEqual(response.data['instagram_id'], 'comment_123')
        self.assertEqual(response.data['post'], self.post.id)
        # Проверяем, что комментарий создан в БД
        self.assertTrue(self.post.comments.filter(instagram_id='comment_123').exists())

    def test_create_comment_post_not_found(self):
        url = reverse('post-add-comment', args=[999])  # несуществующий id
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('instagram.views.InstagramClient.post_comment')
    def test_create_comment_instagram_post_deleted(self, mock_post_comment):
        # Мокаем ошибку Instagram (например, 404)
        from requests.exceptions import HTTPError
        mock_post_comment.side_effect = HTTPError('404 Client Error: Not Found')

        url = reverse('post-add-comment', args=[self.post.id])
        response = self.client.post(url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Instagram API error', response.data['error'])
        # Проверяем, что комментарий не создан в БД
        self.assertEqual(self.post.comments.count(), 0)