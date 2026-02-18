
from django.db.models import Model, TextField, CharField, URLField, DateTimeField, ForeignKey, CASCADE


class Post(Model):
    instagram_id = CharField(max_length=100, unique=True, verbose_name="ID в Instagram")
    caption = TextField(blank=True)
    media_type = CharField(max_length=20)
    media_url = URLField(max_length=2000, blank=True)
    permalink = URLField(max_length=2000)
    timestamp = DateTimeField()
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.instagram_id} - {self.caption[:30]}"


class Comment(Model):
    instagram_id = CharField(max_length=100, unique=True, verbose_name="ID комментария в Instagram")
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    text = TextField()
    timestamp = DateTimeField()
    username = CharField(max_length=100, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Comment {self.instagram_id} on {self.post.instagram_id}"