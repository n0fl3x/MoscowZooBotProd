# Generated by Django 4.2.3 on 2023-08-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anim_animal', models.CharField(help_text='Максимум 128 символов.', max_length=128, unique=True, verbose_name='Название животного')),
                ('anim_name', models.CharField(help_text='Как зовут это животное в Московском зоопарке?', max_length=128, verbose_name='Кличка животного')),
                ('anim_gender', models.IntegerField(choices=[(1, 'Самка'), (0, 'Самец')], default=1)),
                ('anim_image', models.TextField(help_text='Вставьте сюда ID изображения животного в Telegram или ссылку на изображение.', verbose_name='Изображение')),
                ('anim_text', models.TextField(help_text='Вставьте сюда текстовое описание животного.', verbose_name='Описание')),
                ('anim_url', models.TextField(help_text='Вставьте сюда ссылку на страницу с описанием животного.', verbose_name='Веб-страница')),
                ('anim_day_activ', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Суточная активность')),
                ('anim_feed_type', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Тип питания')),
                ('anim_live_env', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Среда обитания')),
                ('anim_climate', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Климат')),
                ('anim_year_activ', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Годовая активность')),
                ('anim_social', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Социальность')),
                ('anim_appear', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Внешний вид')),
                ('anim_dreams', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Мечты')),
                ('anim_just_quest', models.CharField(help_text='Укажите коэффициент от -3 до 3 (включительно).', max_length=2, verbose_name='Просто вопрос')),
            ],
            options={
                'verbose_name': 'Животное',
                'verbose_name_plural': 'Животные',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')),
                ('fb_result', models.CharField(max_length=128, verbose_name='Результат')),
                ('fb_user_id', models.CharField(help_text='Уникальный идентификатор пользователя в Telegram.', max_length=64, verbose_name='Идентификатор пользователя')),
                ('fb_username', models.CharField(blank=True, help_text='Имя пользователя в Telegram, если оно задано.', max_length=128, null=True, verbose_name='Имя пользователя')),
                ('fb_text', models.TextField(blank=True, verbose_name='Текст отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата результата')),
                ('res_user_id', models.CharField(help_text='Уникальный идентификатор пользователя в Telegram.', max_length=64, unique=True, verbose_name='Идентификатор пользователя')),
                ('res_username', models.CharField(blank=True, help_text='Имя пользователя в Telegram, если оно задано.', max_length=128, null=True, verbose_name='Имя пользователя')),
                ('res_totem_animal', models.CharField(max_length=128, verbose_name='Тотемное животное')),
                ('res_ans_list', models.TextField(help_text='Список ответов пользователя на все вопросы(статистические данные) для отладки бота.', verbose_name='Ответы пользователя')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
    ]
