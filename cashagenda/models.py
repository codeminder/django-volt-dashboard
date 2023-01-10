from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
import django.utils.timezone
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy


class User(AbstractUser):
    
    avatar = models.ImageField(upload_to="user_avatars/")
    
    def __str__(self):
        return self.username
    
class Account(models.Model):
    
    name = models.CharField(max_length=50, default="")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta():
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
    
    def __str__(self, *args, **kwargs):
        return self.name

class Currency(models.Model):
    
    name = models.CharField(max_length=50, default="")
    short_name = models.CharField(max_length=3, default="")
    course = models.DecimalField(decimal_places=4, max_digits=10, verbose_name="Курс", default=0)
    
    class Meta():
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
    
    def __str__(self, *args, **kwargs):
        return self.name
    
class Budget(models.Model):
    
    name = models.CharField(max_length=50, default="")
    short_name = models.CharField(max_length=3, default="")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    class Meta():
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
    
    def __str__(self, *args, **kwargs):
        return self.name
        

class Document(models.Model):

    date     = models.DateTimeField(verbose_name="Дата", default=django.utils.timezone.now)
    # currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    # number = models.AutoField(primary_key=False)
    account  = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Счет")
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма", default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Валюта")
    comment  = models.TextField(verbose_name="Комментарий", default="", blank=True)
    photo    = models.ImageField(upload_to='photos/%Y/%m/', blank=True)
    # posted   = models.BooleanField(default=False)
    def __str__(self):
        return "{0} №{1} от {2}".format(self._meta.verbose_name, self.id, self.date.strftime("%Y-%b-%d %H:%M:%S"))
    
    # class Meta():
    #     ordering = ["date"]
        
    # def post(self):
    #     self.posted = True
    #     self.save()

    
    # def unpost(self):
    #     self.posted = False
    #     self.save()
    # def save(self, *args, **kwargs):
    #     if self == None:
    #         raise Exception
    
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        # if self == 'draft' and self is not None:
        raise ValidationError('That document saving is restricted')
        # Set the pub_date for published items if it hasn't been set already.
    
    def get_my_model_name(self):
        return self._meta.model_name
    
    def get_absolute_url(self):
        # return reverse("view_doc", kwargs={"doc_id": self.pk, "type_doc": self._meta.model_name})
        return reverse_lazy(f"cashagenda_{self.__class__.__name__.lower()}_update", kwargs={"pk": self.pk})
    


class Profit(Document):
    
    budget = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Статья")
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum, account=self.account)
        br.save()
        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Прибыль"
        verbose_name_plural = "Прибыли"
        # fields = ('date', 'sum_in', 'currency', 'account_in', 'comment')
        
    def clean(self):
        # return super().clean()
        pass
    


class Cost(Document):
    
    budget = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Статья")
        
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, account=self.account)
        br.save()
        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Затрата"
        verbose_name_plural = "Затраты"
        # fields = ('date', 'sum_out', 'currency', 'account_out', 'comment')
    
    def clean(self):
            # return super().clean()
        pass
    



class Transfer(Document):
    
    account_in = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="IncomeAccount", verbose_name="Счет поступления")
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br1 = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, account=self.account)
        br1.save()
        br2 = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum, account=self.account_in)
        br2.save()
        self.balance_records.set([br1, br2])
    
    class Meta():
        verbose_name = "Перемещение"
        verbose_name_plural = "Перемещения"
    
    def clean(self):
            # return super().clean()
        pass
    


class Inventory(Document):
    
    budget   = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Статья")
    sum_diff = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма разница", default=0)
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
    
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum_diff, account=self.account)
        br.save()

        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Инвентаризация"
        verbose_name_plural = "Инвентаризации"
    
    def clean(self):
            # return super().clean()
        pass
    


class CurrencyExchange(Document):
    
    currency_in = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="OutcomeCurrency", verbose_name="Валюта покупки")
    sum_in      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма разница", default=0)
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br1 = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, account=self.account)
        br1.save()
        br2 = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum_in, account=self.account)
        br2.save()
        self.balance_records.set([br1, br2])

    
    class Meta():
        verbose_name = "Обмен валюты"
        verbose_name_plural = "Обмены валют"
    
    def clean(self):
            # return super().clean()
        pass
        
        
class BalanceRecord(models.Model):
    
    date     = models.DateTimeField(verbose_name="Дата", default=django.utils.timezone.now)
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма", default=0)
    balance  = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Баланс", default=0)
    account  = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Счет", related_name="balance_records")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Документ", related_name="balance_records")
    
    def __str__(self, *args, **kwargs):
        return "{0} to {1}".format(self.sum, self.account)
    
class BudgetRecord(models.Model):
    
    date     = models.DateTimeField(verbose_name="Дата", default=django.utils.timezone.now)
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Сумма", default=0)
    account  = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Статья", related_name="budget_records")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Документ", related_name="budget_records")