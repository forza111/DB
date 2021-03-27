from django.db import models
from django.contrib.auth.models import User

class TypeNumber(models.Model):
    type_number = models.CharField("Тип телефона",max_length=20)

    def __str__(self):
        return self.type_number


class Telephone(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    telephone_number = models.CharField("Номер телефона",max_length=12)
    type_number = models.ManyToManyField(TypeNumber, verbose_name="Тип телефона",
                                         related_name="type_num")

    def get_type_number(self):
        return ",".join([str(tn) for tn in self.type_number.all()])
