from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from king_suit.king_suit_app.core.app_validators import validate_only_letters, validate_file_size


# Create your models here.


class KingSuitUser(AbstractUser):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Do not show', 'Do not show'),
    )

    first_name = models.CharField(
        verbose_name='First name',
        max_length=30,
        validators=(validators.MinLengthValidator(2), validate_only_letters,)
    )

    last_name = models.CharField(
        verbose_name='Last name',
        max_length=30,
        validators=(validators.MinLengthValidator(2), validate_only_letters,),
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    gender = models.CharField(
        verbose_name='Gender',
        choices=gender_choices,
        max_length=len('Do not show'),
    )

    photo = models.ImageField(
        verbose_name='Personal photo',
        upload_to='user_photos/',
        validators=(validate_file_size,),
        null=True,
        blank=True,
    )

    # photo = models.URLField(
    #     verbose_name='Image URL',
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class KingSuitUserFeedbackComment(models.Model):
    title = models.CharField(
        verbose_name='Title',
        max_length=50,
        validators=(validators.MinLengthValidator(3),)
    )

    content = models.TextField(
        verbose_name='Content',
    )

    photo = models.ImageField(
        verbose_name='Photo',
        upload_to='feedback_photos/',
        validators=(validate_file_size,),
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        KingSuitUser,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Custom feedback'

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        validators=(validators.MinLengthValidator(4), ),
    )

    price = models.PositiveIntegerField(
        verbose_name='Price'
    )

    size = models.CharField(
        verbose_name='Size',
        max_length=60,
    )

    description = models.TextField(
        verbose_name='Description',
    )

    photo = models.ImageField(
        verbose_name='Suit photo',
        upload_to='suit_photos/',
        validators=(validate_file_size,),
    )

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.pk} {self.name}'


class Article(models.Model):
    title = models.CharField(
        verbose_name='Title',
        max_length=50,
    )

    content = models.TextField(
        verbose_name='Content',
    )

    photo = models.ImageField(
        verbose_name='Article photo',
        upload_to='article_photos/',
        validators=(validate_file_size,),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.pk} {self.title}'


class Department(models.Model):
    name = models.CharField(
        verbose_name='Department name',
        max_length=30,
    )

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.name}'


class Employee(models.Model):
    first_name = models.CharField(
        verbose_name='First name',
        max_length=30,
        validators=(validators.MinLengthValidator(2), validate_only_letters,)
    )

    last_name = models.CharField(
        verbose_name='Last name',
        max_length=30,
        validators=(validators.MinLengthValidator(2), validate_only_letters,),
    )

    age = models.PositiveIntegerField(
        verbose_name='Age',
        null=True,
        blank=True,
    )

    hobby = models.CharField(
        verbose_name='Hobby',
        max_length=30,
        null=True,
        blank=True,
    )

    position = models.CharField(
        verbose_name='Position',
        max_length=50,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
    )

    photo = models.ImageField(
        verbose_name='Employee photo',
        upload_to='employee_photos/',
        validators=(validate_file_size,),
    )

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


