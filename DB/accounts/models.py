from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from dateutil.relativedelta import relativedelta
import decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_card(object):
    if object.score.type_score != "текущий":
        raise ValidationError(
            _("%(value)s is not an even number"),
            params={"value": object},
        )

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
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Страна")
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
    symbol = models.CharField("Сивол валюты", max_length=5)

    def __str__(self):
        return self.symbol

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

class TypeScore(models.Model):
    name = models.CharField("Тип счета",max_length=30)

    def __str__(self):
        return self.name


class Score(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_score")
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        verbose_name="Валюта счета",
        related_name="currency_score",
        null=True)
    score_number = models.CharField(
        "Номер счета",
        unique=True,
        max_length=20,
        validators=[RegexValidator(r'^\d{20}$')])
    bank_name = models.ForeignKey(
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
    type_score = models.ForeignKey(
        TypeScore,
        on_delete=models.SET_NULL,
        verbose_name="Тип счета",
        related_name="sc",
        null=True)

    def __str__(self):
        return f"Счет {self.user_id} Валюта: {self.currency}"

class Balance(models.Model):
    score_id = models.OneToOneField(
        Score,
        verbose_name="Счет",
        related_name="score_balance",
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

class CreditTarget(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Credit(models.Model):
    score = models.OneToOneField(
        Score,
        verbose_name="Счет",
        related_name="score_credit",
        on_delete=models.CASCADE,
        null=True
    )
    target = models.ForeignKey(
        CreditTarget,
        verbose_name="Назначение кредита",
        related_name="cr",
        on_delete=models.PROTECT
    )
    sum_credit = models.DecimalField(
        "Сумма кредита",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    beginning_date = models.DateField("Дата начала кредита", auto_now=True)
    deadline = models.PositiveSmallIntegerField("Срок кредита", max_length=3)
    interest_rate = models.ForeignKey(
        InterestRate,
        verbose_name="процентная ставка",
        related_name="credit_interest_rate",
        on_delete=models.PROTECT,
        )

    def __str__(self):
        return f"Кредит пользователя {self.score}"


class CreditInfo(models.Model):
    credit = models.OneToOneField(
        Credit,
        verbose_name="Кредит",
        related_name="info",
        on_delete=models.CASCADE,
    )
    completion_date = models.DateField(
        "Дата завершения кредита",
        null=True,
        blank=True
    )
    interest_rate_mounth = models.DecimalField(
        "Процентная ставка за месяц",
        max_digits=20,
        decimal_places=18,
        null=True,
        blank=True)
    total_rate = models.DecimalField(
        "Общая ставка",
        max_digits=20,
        decimal_places=18,
        null=True,
        blank=True)
    deadline_mounth = models.PositiveSmallIntegerField("Срок кредита, мес")
    mounthly_payments = models.DecimalField(
        "Ежемесячный платеж",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    total_debt = models.DecimalField(
        "Долг + проценты",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    interest_charges = models.DecimalField(
        "Начисленные проценты",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    paid = models.DecimalField(
        "Оплачено",
        max_digits=15,
        decimal_places=2,
        default=decimal.Decimal('0')
    )
    debt = models.DecimalField(
        "Осталось заплатить",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)

    def __str__(self):
        return str(self.credit)

    def create_irm(self):
        self.interest_rate_mounth = \
            int(self.credit.interest_rate.rate)/12/100
        return self.interest_rate_mounth

    def create_deadline_mounth(self):
        self.deadline_mounth = self.credit.deadline * 12
        return self.deadline_mounth

    def create_total_rate(self):
        self.total_rate = (1 + self.interest_rate_mounth)**self.deadline_mounth
        return self.total_rate

    def create_mounthly_payments(self):
        self.mounthly_payments = \
            round(decimal.Decimal(self.credit.sum_credit)*
                  decimal.Decimal(self.interest_rate_mounth)*
                  decimal.Decimal(self.total_rate)/
                  (decimal.Decimal(self.total_rate)-1),2)
        return self.mounthly_payments

    def create_total_debt(self):
        self.total_debt = self.mounthly_payments*self.deadline_mounth
        return self.total_debt

    def create_interest_charges(self):
        self.interest_charges = self.total_debt-self.credit.sum_credit
        return self.interest_charges

    def create_completion_date(self):
        self.completion_date = self.credit.beginning_date + relativedelta(years=self.credit.deadline)
        return self.completion_date

    def create_debt(self):
        self.debt = decimal.Decimal(self.total_debt)-self.paid
        return self.debt

@receiver(pre_save, sender=CreditInfo)
def irm(sender, instance, **kwargs):
    instance.interest_rate_mounth = instance.create_irm()
    instance.deadline_mounth = instance.create_deadline_mounth()
    instance.total_rate = instance.create_total_rate()
    instance.mounthly_payments = instance.create_mounthly_payments()
    instance.total_debt = instance.create_total_debt()
    instance.interest_charges = instance.create_interest_charges()
    instance.completion_date = instance.create_completion_date()
    instance.debt = instance.create_debt()


@receiver(post_save, sender=Credit)
def createcreditinfo(sender, instance, **kwargs):
    if not hasattr(instance, "info"):
        crinfo = CreditInfo.objects.create(credit=instance)
    if hasattr(instance, "info"):
        crinfo = CreditInfo.objects.get(credit=instance)
        crinfo.credit = instance
        crinfo.save()


@receiver(post_save, sender=CreditInfo)
def createpaymentinfo(sender, instance, **kwargs):
    if not hasattr(instance.credit, "credit_payments_info") or \
            instance.credit.credit_payments_info.all().count() == 0:
        for i in range(1,instance.deadline_mounth+1):
            crpaymentinfo = PaymentsInfo.objects.create(
                credit=instance.credit,
                date=instance.credit.beginning_date+relativedelta(months=i),
                number=i,
                mounthly_payments=instance.mounthly_payments,
                debt=instance.total_debt-instance.mounthly_payments*i
            )
    else:
        PaymentsInfo.objects.filter(credit=instance.credit).delete()
        return createpaymentinfo(sender, instance, **kwargs)


class PaymentsInfo(models.Model):
    credit = models.ForeignKey(
        Credit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Кредит",
        related_name="credit_payments_info")
    number = models.PositiveSmallIntegerField("Номер платежа")
    date = models.DateField("Дата платежа")
    mounthly_payments = models.DecimalField(
        "Ежемесячный платеж",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    debt = models.DecimalField(
        "Осталок кредита",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)


    def __str__(self):
        return f"{self.number} платеж {self.credit} {self.credit.target}"


class Payments(models.Model):
    credit = models.ForeignKey(
        Credit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="кредит",
        related_name="credit_payments")
    pay = models.DecimalField(
        "Платеж",
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True)
    date = models.DateField("Дата платежа", auto_now=True)

    def __str__(self):
        return f"Платеж на сумму {self.pay} от {self.date}"


@receiver(post_save, sender=Payments)
def changepaid(sender, instance, **kwargs):
    p = Credit.objects.get(credit_payments=instance)
    p.info.paid += instance.pay
    p.save()


class PaymentSystem(models.Model):
    name = models.CharField("Тип платежной системы", max_length=15)

    def __str__(self):
        return self.name

class TypeCard(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Card(models.Model):

    score = models.OneToOneField(
        Score,
        on_delete= models.PROTECT,
        verbose_name="Счет",
        related_name="score_card")
    card_number = models.CharField(
        "Номер карты",
        max_length=18,
        validators=[RegexValidator(r'^\d{16,18}$')])
    cvv = models.CharField(
        "Код безопасности",
        max_length=3,
        validators=[RegexValidator(r'^\d{3}$')])
    date = models.DateField("Срок действия")
    paymentsystem = models.ForeignKey(
        PaymentSystem,
        on_delete=models.PROTECT,
        verbose_name="тип платежной системы",
        related_name="paymentsystem_card"
    )
    type_card = models.ForeignKey(
        TypeCard,
        on_delete=models.PROTECT,
        verbose_name="Тип карты",
        related_name="card"
    )

    def __str__(self):
        return f"{self.paymentsystem} {self.card_number}"




