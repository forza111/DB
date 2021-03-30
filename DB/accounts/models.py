from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

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
        return ",".join([str(i) for i in self.type_number.all()])


class Country(models.Model):
    name_country = models.CharField(max_length=30)

    def __str__(self):
        return self.name_country


class Area(models.Model):
    name_area = models.CharField("Область",max_length=30)
    country_id = models.ForeignKey(Country, on_delete=models.SET_NULL,null=True,verbose_name="Страна")

    def __str__(self):
        return self.name_area


class City(models.Model):
    name_city = models.CharField("Город",max_length=30)
    area_id = models.ForeignKey(Area, on_delete=models.SET_NULL,null=True,verbose_name="Область")

    def __str__(self):
        return self.name_city


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    country = models.OneToOneField(Country, on_delete=models.SET_NULL,null=True)
    area = ChainedForeignKey(
    Area,
    chained_field="country",
    chained_model_field="country_id",
    show_all=False,
    auto_choose=True)
    city = ChainedForeignKey(
        City,
        chained_field="area",
        chained_model_field="area_id",
        show_all=False,
        auto_choose=True)
    street = models.CharField("Улица", max_length=30)
    house_number = models.CharField("Номер дома", max_length=10)
    entrance = models.SmallIntegerField("Подъезд", max_length=50, null=True, blank=True)
    floor = models.SmallIntegerField("Этаж", max_length=200, null=True, blank=True)
    room = models.SmallIntegerField("Номер квартиры", max_length=500, null=True, blank=True)