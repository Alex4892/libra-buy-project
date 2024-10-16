# Generated by Django 5.1.1 on 2024-10-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Жанр')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='book',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Описание'),
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication',
            field=models.CharField(max_length=100, verbose_name='Издательство'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.CharField(max_length=4, verbose_name='Год'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='books_app.genre', verbose_name='Жанры'),
        ),
    ]