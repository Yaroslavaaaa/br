# Generated by Django 4.1.6 on 2023-04-21 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_roles_options_books_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsAns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans_com_text', models.TextField(db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('book_com_ans', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments_ans', to='books.books')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_ans', to='books.comments')),
                ('user_com_ans', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответы на комментарии',
                'verbose_name_plural': 'Ответв на комментарии',
                'ordering': ['create_time', 'ans_com_text'],
            },
        ),
    ]
