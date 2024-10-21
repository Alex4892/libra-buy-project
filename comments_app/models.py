from django.db import models

from books_app.models import Book

class Comment(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    email = models.EmailField(
        verbose_name='Email'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарий'
    
    def __str__(self):
        return f'Комментарий от {self.email}'

# Create your models here.
