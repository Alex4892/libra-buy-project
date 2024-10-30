from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name = "Жанр"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        
    

class Book(models.Model):
    seller = models.ForeignKey(
        User,
        related_name ="books",
        on_delete = models.CASCADE,
        verbose_name="Продавец"
    )
    name = models.CharField(
        max_length=200,
        verbose_name = "Название"
    )
    author = models.CharField(
        max_length=100,
        verbose_name = "Автор"
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name = "Жанры"
    )
    description = models.TextField(
        max_length=500,
        verbose_name = "Описание"
    )
    publication = models.CharField(
        max_length=100,
        verbose_name = "Издательство"
    )
    publication_year = models.CharField(
        max_length=4,
        verbose_name = "Год"
    )
    quantity = models.PositiveIntegerField(
        default = 0,
        verbose_name = "Количество"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name = "Цена"
    )
    image = models.ImageField(
        upload_to='books/', 
        blank=True,
        null=True,
        verbose_name="Изображения"
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name = "Дата"
    )

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"




# Create your models here.
