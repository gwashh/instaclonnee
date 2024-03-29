# Generated by Django 3.2.7 on 2021-12-07 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insta', '0003_auto_20211207_1554'),
    ]


    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='likes',
            new_name='like',
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.CharField(choices=[('like', 'like'), ('unlike', 'unlike')], default='like', max_length=50)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='insta.image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
