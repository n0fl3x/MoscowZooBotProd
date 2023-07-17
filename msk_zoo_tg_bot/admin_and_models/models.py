from django.db import models


class Question(models.Model):

    number = models.IntegerField(
        blank=False,
        unique=True,
        verbose_name='Порядковый номер вопроса',
        help_text='Порядковый номер НЕ должен совпадать с каким-либо другим номером вопроса',
    )

    text = models.TextField(
        blank=False,
        verbose_name='Текст вопроса',
        help_text='Введите здесь текст вопроса (обязательное поле)',
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):

    to_question = models.ForeignKey(
        null=False,
        to='Question',
        on_delete=models.CASCADE,
        related_name='answer_to_question',
        help_text='К какому вопросу относится ответ (обязательное поле)',
    )

    number = models.CharField(
        blank=False,
        max_length=8,
        unique=True,
        verbose_name='Идентификатор ответа',
        help_text='Введите здесь уникальный идентификатор ответа в формате:'
                  '<номер вопроса>.<номер ответа>.'
                  'Например для третьего ответа на второй вопрос идентификатором будет 2.3',
    )

    text = models.TextField(
        blank=False,
        verbose_name='Ответ',
        help_text='Введите здесь текст ответа (обязательное поле)',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.text}'


class Animal(models.Model):

    name = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
        verbose_name='Название животного',
        help_text='Максимум 64 символа',
    )

    image = models.TextField(
        blank=False,
        verbose_name='Изображение',
        help_text='Вставьте сюда ID изображения животного в Telegram или ссылку на изображение',
    )

    text = models.TextField(
        blank=False,
        verbose_name='Описание',
        help_text='Вставьте сюда текстовое описание животного (обязательное поле)',
    )

    anim_url = models.TextField(
        blank=False,
        verbose_name='Веб-страница',
        help_text='Вставьте сюда ссылку на страницу с описанием животного (обязательное поле)',
    )

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'

    def __str__(self):
        return f'{self.name}'


class Result(models.Model):

    user_id = models.CharField(
        max_length=64,
        blank=False,
        unique=True,
        verbose_name='ID пользователя',
        help_text='Уникальный идентификатор пользователя в Telegram',
    )

    totem_animal = models.ForeignKey(
        null=True,
        to='Animal',
        verbose_name='Итоговое животное',
        on_delete=models.CASCADE,
    )

    ans_list = models.TextField(
        verbose_name='Ответы пользователя',
        help_text='Список ответов пользователя на все вопросы'
                  '(статистические данные) для отладки бота',
    )

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return f'{self.user_id} = {self.totem_animal.name}'


class Feedback(models.Model):

    result = models.OneToOneField(
        to='Result',
        on_delete=models.CASCADE,
        verbose_name='Результат',
    )

    user_id = models.CharField(
        max_length=64,
        blank=False,
        verbose_name='Идентификатор пользователя',
        help_text='Уникальный идентификатор пользователя в Telegram',
    )

    username = models.CharField(
        max_length=64,
        null=True,
        verbose_name='Имя пользователя',
        help_text='Имя пользователя в Telegram, если оно задано',
    )

    text = models.TextField(
        blank=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.user_id} = {self.text}'
