from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework import status, viewsets
from django.conf import settings
from .client import InstagramClient
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer


class SyncPostsView(APIView):
    def post(self, request):
        token = settings.INSTAGRAM_ACCESS_TOKEN
        user_id = settings.INSTAGRAM_USER_ID
        client = InstagramClient(token, user_id)

        try:
            media_list = client.get_user_media()
        except Exception as e:
            return Response({'error': f'Failed to fetch media from Instagram: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        created_count = 0
        updated_count = 0

        for media in media_list:
            instagram_id = media['id']
            defaults = {
                'caption': media.get('caption', ''),
                'media_type': media['media_type'],
                'media_url': media.get('media_url', ''),
                'permalink': media['permalink'],
                'timestamp': media['timestamp'],
            }
            obj, created = Post.objects.update_or_create(
                instagram_id=instagram_id,
                defaults=defaults
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        return Response({
            'message': 'Sync completed',
            'created': created_count,
            'updated': updated_count,
        }, status=status.HTTP_200_OK)

class PostCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-timestamp'

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для чтения постов (list и retrieve).
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostCursorPagination

    @action(detail=True, methods=['post'], url_path='comment')
    def add_comment(self, request, pk=None):
        post = self.get_object()  # получаем пост по pk (внутренний id)

        # Валидируем входные данные
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data['text']

        # Отправляем комментарий в Instagram
        client = InstagramClient(settings.INSTAGRAM_ACCESS_TOKEN, settings.INSTAGRAM_USER_ID)
        try:
            instagram_response = client.post_comment(post.instagram_id, text)
        except Exception as e:
            # Обрабатываем ошибку (пост мог быть удалён в Instagram)
            return Response(
                {'error': f'Instagram API error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Из ответа Instagram получаем id созданного комментария
        instagram_comment_id = instagram_response.get('id')
        if not instagram_comment_id:
            return Response(
                {'error': 'Instagram did not return comment ID'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Сохраняем комментарий в БД
        # Для упрощения timestamp и username не сохраняем (можно потом получить дополнительным запросом)
        # Или можно сразу сохранить то, что есть. В реальном проекте, вероятно, нужно получить данные комментария.
        # Но по заданию достаточно сохранить комментарий. Для timestamp используем текущее время.
        from django.utils import timezone
        comment = Comment.objects.create(
            instagram_id=instagram_comment_id,
            post=post,
            text=text,
            timestamp=timezone.now(),
            username='',  # можно оставить пустым или запросить отдельно
        )

        # Возвращаем сериализованный комментарий
        output_serializer = CommentSerializer(comment)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)