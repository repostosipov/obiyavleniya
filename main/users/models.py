from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxLengthValidator, RegexValidator
from django.urls import reverse

class Profile(models.Model):
    CHOICES = [
    ('Приморский край', (
            ('Владивосток', 'Владивосток'),
            ('Находка', 'Находка'),
        )
    ),
    ('Сахалин', (
            ('Южно Сахалинск', 'Южно Сахалинск'),
            ('Холмск', 'Холмск'),
        )
    ),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(verbose_name="Описание продавца", blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Телефон должнен быть похож на: '+999999999'. ")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Телефон") 
    shop = models.BooleanField(default=False, verbose_name="Вы магазин?")
    city = models.CharField(max_length=300, choices = CHOICES, blank=True)
  

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"



# user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)

