from django.db import models


class Animal(models.Model):

    anim_name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название животного',
        help_text='Максимум 128 символов.',
    )

    anim_image = models.TextField(
        verbose_name='Изображение',
        help_text='Вставьте сюда ID изображения животного в Telegram или ссылку на изображение.',
    )

    anim_text = models.TextField(
        verbose_name='Описание',
        help_text='Вставьте сюда текстовое описание животного.',
    )

    anim_url = models.TextField(
        verbose_name='Веб-страница',
        help_text='Вставьте сюда ссылку на страницу с описанием животного.',
    )

    # балансирующие коэффициенты:
    anim_day_activ = models.CharField(
        max_length=2,
        verbose_name='Суточная активность',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_feed_type = models.CharField(
        max_length=2,
        verbose_name='Тип питания',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_live_env = models.CharField(
        max_length=2,
        verbose_name='Среда обитания',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_climate = models.CharField(
        max_length=2,
        verbose_name='Климат',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_year_activ = models.CharField(
        max_length=2,
        verbose_name='Годовая активность',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_social = models.CharField(
        max_length=2,
        verbose_name='Социальность',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_appear = models.CharField(
        max_length=2,
        verbose_name='Внешний вид',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_dreams = models.CharField(
        max_length=2,
        verbose_name='Мечты',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    anim_just_quest = models.CharField(
        max_length=2,
        verbose_name='Просто вопрос',
        help_text='Укажите коэффициент от -3 до 3 (включительно).',
    )

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return f'{self.anim_name}'


class Result(models.Model):

    res_created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата результата',
    )

    res_user_id = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор пользователя',
        help_text='Уникальный идентификатор пользователя в Telegram.',
    )

    res_totem_animal = models.CharField(
        max_length=128,
        verbose_name='Тотемное животное',
    )

    res_ans_list = models.TextField(
        verbose_name='Ответы пользователя',
        help_text='Список ответов пользователя на все вопросы'
                  '(статистические данные) для отладки бота.',
    )

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return f'{self.res_user_id} = {self.res_totem_animal}'


class Feedback(models.Model):

    fb_created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
    )

    fb_result = models.CharField(
        max_length=128,
        verbose_name='Результат',
    )

    fb_user_id = models.CharField(
        max_length=64,
        verbose_name='Идентификатор пользователя',
        help_text='Уникальный идентификатор пользователя в Telegram.',
    )

    fb_username = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя в Telegram, если оно задано.',
    )

    fb_text = models.TextField(
        blank=True,
        verbose_name='Текст отзыва',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        if self.fb_username is not None:
            return f'{self.fb_user_id} ({self.fb_username}) = {self.fb_text}'
        return f'{self.fb_user_id} = {self.fb_text}'
