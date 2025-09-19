from django.db import models
from django.utils.translation import gettext_lazy as _

from contacts.models import ContactInfo


class BankAccount(models.Model):
    partner = models.ForeignKey(
        "partners.Partner", related_name="bank_accounts", on_delete=models.CASCADE, verbose_name=_("Партнёр")
    )
    bank_name = models.CharField(max_length=200, verbose_name=_("Банк"), help_text=_("Полное наименование банка."))
    bic = models.CharField(max_length=20, blank=True, verbose_name=_("БИК"), help_text=_("BIC/SWIFT код, если есть."))
    account_number = models.CharField(max_length=64, verbose_name=_("Номер счёта"),
                                      help_text=_("Номер счета в локальном формате."))
    iban = models.CharField(max_length=64, blank=True, verbose_name=_("Международный номер банковского счёта"),
                            help_text=_("IBAN для международных переводов (если есть)."))
    is_primary = models.BooleanField(default=False, verbose_name=_("Основной счёт"),
                                     help_text=_("Отмечается, если этот счёт должен использоваться по умолчанию."))

    class Meta:
        verbose_name = "Банковский счёт"
        verbose_name_plural = "Банковские счета"

    def __str__(self):
        return f"{self.bank_name} / {self.account_number}"


class Partner(models.Model):
    PARTNER_TYPES = [
        ("manufacturer", _("Производитель")),
        ("distributor", _("Дистрибьютор")),
        ("retailer", _("Розничная сеть")),
        ("individual", _("Индивидуальный предприниматель")),
        ("other", _("Другое")),
    ]

    name = models.CharField(max_length=255, verbose_name=_("Название"))
    legal_name = models.CharField(max_length=255, blank=True, verbose_name=_("Юридическое название"))
    partner_type = models.CharField(
        max_length=30, choices=PARTNER_TYPES, default="retailer", verbose_name=_("Тип партнёра")
    )
    tax_id = models.CharField(max_length=64, blank=True, verbose_name="ИНН/VAT")
    legal_address = models.ForeignKey(
        ContactInfo, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    contact_person_name = models.CharField(max_length=200, blank=True)
    contact_person_phone = models.CharField(max_length=50, blank=True)
    contact_person_email = models.EmailField(blank=True)
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    contract_file = models.FileField(upload_to="contracts/", null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="active",
        choices=[
            ("active", _("Активен")),
            ("suspended", _("Приостановлен")),
            ("terminated", _("Расторгнут")),
        ],
        verbose_name=_("Статус"),
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["partner_type"]),
        ]

    def __str__(self):
        return self.name
