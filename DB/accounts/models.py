from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator

class TypeNumber(models.Model):
    type_number = models.CharField("Тип телефона",max_length=20)

    def __str__(self):
        return self.type_number


class Telephone(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь")
    telephone_number = models.CharField("Номер телефона",max_length=12)
    type_number = models.ManyToManyField(
        TypeNumber,
        verbose_name="Тип телефона",
        related_name="type_num")

    def get_type_number(self):
        return ",".join([str(i) for i in self.type_number.all()])


class Country(models.Model):
    name_country = models.CharField(max_length=30)

    def __str__(self):
        return self.name_country


class Area(models.Model):
    name_area = models.CharField("Область",max_length=30)
    country_id = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Страна")

    def __str__(self):
        return self.name_area


class City(models.Model):
    name_city = models.CharField("Город", max_length=30)
    area_id = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Область")

    def __str__(self):
        return self.name_city


class UserLocation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="location")
    country = models.OneToOneField(
        Country,
        on_delete=models.SET_NULL,
        null=True)
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
    house_number = models.CharField(
        "Номер дома",
        max_length=11,
        validators=[RegexValidator(r'^\d{1,5}(([/]\d{1,5})|[a-z,а-я])?$')])
    building = models.PositiveSmallIntegerField(
        "Корпус",
        max_length=5,
        null=True,
        blank=True)
    edifice = models.PositiveSmallIntegerField(
        "Строение",
        max_length=5,
        null=True,
        blank=True)
    entrance = models.PositiveSmallIntegerField(
        "Подъезд",
        max_length=5,
        null=True,
        blank=True)
    floor = models.PositiveSmallIntegerField(
        "Этаж",
        max_length=200,
        null=True,
        blank=True)
    room = models.PositiveSmallIntegerField(
        "Номер квартиры", max_length=5, null=True, blank=True)


class Currency(models.Model):
    name_currency = models.CharField("Валюта", max_length=20)

    def __str__(self):
        return self.name_currency

class Rate(models.Model):
    currency = models.OneToOneField(
        Currency,
        verbose_name="Валюта",
        related_name="currency_rate",
        on_delete=models.CASCADE)
    date = models.DateTimeField("Дата",auto_now=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Курс {self.currency} по ЦБ на {self.date}"


class BankName(models.Model):
    name = models.CharField("Название",max_length=30)

    def __str__(self):
        return self.name

class Swift(models.Model):
    name = models.CharField("SWIFT-код",max_length=30)

    def __str__(self):
        return self.name


class Score(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_score")
    currency = models.ManyToManyField(
        Currency,
        verbose_name="Валюта счета",
        related_name="currency_score")
    score_number = models.CharField(
        "Номер счета",
        unique=True,
        max_length=20,
        validators=[RegexValidator(r'^\d{20}$')])
    bank_name = models.OneToOneField(
        BankName,
        verbose_name="Банк",
        on_delete=models.SET_NULL,
        null=True)
    bik = models.CharField(
        "БИК",
        unique=True,
        max_length=9,
        validators=[RegexValidator(r'^\d{9}$')])
    correspondent_account = models.CharField(
        "Корр.счет",
         max_length=20,
         validators=[RegexValidator(r'^\d{20}$')])
    inn = models.CharField(
        "ИНН", max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    kpp = models.CharField(
        "КПП", max_length=9, validators=[RegexValidator(r'^\d{9}$')])
    swift = models.ForeignKey(
        Swift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="SWIFT-код")

    def __str__(self):
        return f"Счет {self.user_id} Валюта: {self.currency.get()}"

class Balance(models.Model):
    score_id = models.OneToOneField(
        Score,
        verbose_name="Счет",
        related_name="score",
        on_delete=models.CASCADE)
    balance = models.PositiveIntegerField("Баланс", null=True, blank=True)

    def __str__(self):
        return f"Баланс пользователя {self.score_id.user_id}"


class InterestRate(models.Model):
    rate = models.CharField(
        "Процентная ставка",
        max_length=2,
        validators=[RegexValidator(r'^\d{1,2}$')])

    def __str__(self):
        return f"Процентная ставка {self.rate} %"


class Credit(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="клиент",related_name="cr")
    name = models.CharField("Назначение кредита", max_length=100)
    sum_credit = models.PositiveIntegerField("Сумма кредита")
    loan_credit = models.PositiveIntegerField(
        "Остаток по кредиту", null=True, blank=True)
    beginning_date = models.DateField("Дата начала кредита", auto_now=True)
    deadline = models.PositiveSmallIntegerField("Срок кредита", max_length=3)
    end_date = models.DateField(
        "Дата закрытия кредита", null=True, blank=True)
    interest_rate = models.ManyToManyField(
        InterestRate,
        verbose_name="процентная ставка",
        related_name="credit_interest_rate",
        )

    def __str__(self):
        return f"Кредит пользователя {self.user_id}"

class Payments(models.Model):
    credit = models.ForeignKey(
        Credit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="кредит",
        related_name="credit_payments")
    pay = models.PositiveIntegerField("Платеж")
    date = models.DateField("Дата платежа", auto_now=True)

    def __str__(self):
        return f"Платеж на сумму {self.pay} от {self.date}"