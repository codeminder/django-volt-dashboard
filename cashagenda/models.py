from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
import django.utils.timezone
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Q, F
from datetime import datetime
from django.utils.timezone import is_aware, make_aware

class User(AbstractUser):
    
    avatar = models.ImageField(upload_to="user_avatars/")
    
    def __str__(self):
        return self.username
    
class Account(models.Model):
    
    name = models.CharField(max_length=50, default="")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta():
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
    
    def __str__(self, *args, **kwargs):
        return self.name

class Currency(models.Model):
    
    name = models.CharField(max_length=50, default="")
    short_name = models.CharField(max_length=3, default="")
    course = models.DecimalField(decimal_places=4, max_digits=10, verbose_name="Course", default=0)
    
    class Meta():
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
    
    def __str__(self, *args, **kwargs):
        return self.name
    
class Budget(models.Model):
    
    name = models.CharField(max_length=50, default="")
    short_name = models.CharField(max_length=3, default="")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    
    class Meta():
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
    
    def __str__(self, *args, **kwargs):
        return self.name
        

class Document(models.Model):

    date     = models.DateTimeField(verbose_name="Date", default=django.utils.timezone.now)
    # currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    # number = models.AutoField(primary_key=False)
    account  = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Account")
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Sum", default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Currency")
    comment  = models.TextField(verbose_name="Comment", default="", blank=True)
    photo    = models.ImageField(upload_to='photos/%Y/%m/', blank=True)
    # posted   = models.BooleanField(default=False)
    def __str__(self):
        
        doc = self
        
        if (hasattr(self, "cost")):
            doc = self.cost
        elif (hasattr(self, "profit")):
            doc = self.profit
        elif (hasattr(self, "transfer")):
            doc = self.transfer
        elif (hasattr(self, "inventory")):
            doc = self.inventory
        elif (hasattr(self, "currencyexchange")):
            doc = self.currencyexchange
        
        return "{0} №{1} от {2}".format(doc._meta.verbose_name, self.id, self.date.astimezone().strftime("%d.%m.%Y %H:%M"))
    
    def __cmp__(self, other):
        if self.date < other.date or (self.date == other.date and self.pk < other.pk):
            return -1
        elif self.date > other.date  or (self.date == other.date and self.pk > other.pk):
            return 1       
        return 0
    
    class Meta():
        ordering = ["-date", "-id"]
        
    # def post(self):
    #     self.posted = True
    #     self.save()

    
    # def unpost(self):
    #     self.posted = False
    #     self.save()
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:
            BalanceRecord.objects.filter(document = self.pk).delete()
            BudgetRecord.objects.filter(document = self.pk).delete()
    #     if self == None:
    #         raise Exception
    
    def clean(self):
        #  this Document without inheritance dont matter
        if not (type(self) is Cost
            or type(self) is Profit
            or type(self) is Transfer
            or type(self) is Inventory
            or type(self) is CurrencyExchange):
            raise ValidationError('That document saving is restricted')
        
        # Don't allow dates older than Linux .
        if self.date.timestamp() < 0:
            raise ValidationError({'date': "Тhe date must be afrer than beginning of the UNIX epoch"})
        
    
    def get_my_model_name(self):
        return self._meta.model_name
    
    def get_absolute_url(self):
        # return reverse("view_doc", kwargs={"doc_id": self.pk, "type_doc": self._meta.model_name})
        return reverse_lazy(f"cashagenda_{self.__class__.__name__.lower()}_update", kwargs={"pk": self.pk})
    


class Profit(Document):
    
    budget = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Budget")
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum, 
                           account=self.account, currency=self.currency)
        br.save()
        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Profit"
        verbose_name_plural = "Profits"
        # fields = ('date', 'sum_in', 'currency', 'account_in', 'comment')
        
    def clean(self):
        return super().clean()
        # pass
    


class Cost(Document):
    
    budget = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Budget")
        
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, 
                           account=self.account, currency=self.currency)
        br.save()
        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Cost"
        verbose_name_plural = "Costs"
        # fields = ('date', 'sum_out', 'currency', 'account_out', 'comment')
    
    def clean(self):
        return super().clean()
        # pass
    



class Transfer(Document):
    
    account_in = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="IncomeAccount", verbose_name="Income Account")
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br1 = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, 
                            account=self.account, currency=self.currency)
        br1.save()
        br2 = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum, 
                            account=self.account_in, currency=self.currency)
        br2.save()
        self.balance_records.set([br1, br2])
    
    class Meta():
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"
    
    def clean(self):
        return super().clean()
        # pass
    


class Inventory(Document):
    
    budget   = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Budget")
    sum_diff = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Diff sum", default=0)
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
    
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum_diff, 
                           account=self.account, currency=self.currency)
        br.save()

        self.balance_records.set([br])
    
    class Meta():
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"
    
    def clean(self):
        return super().clean()
        # pass
    


class CurrencyExchange(Document):
    
    currency_in = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="IncomeCurrency", verbose_name="Income currency")
    sum_in      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Income sum", default=0)
    
    # def __init__(self, *args, **kwargs): # Django в документации не советует переопределять метод __init__()
    #     super().__init__()               # https://djbook.ru/rel1.8/ref/models/instances.html
        
    def __str__(self, *args, **kwargs):
        return super().__str__()
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        br1 = BalanceRecord(document=self.document_ptr, date=self.date, sum=-self.sum, 
                            account=self.account, currency=self.currency)
        br1.save()
        br2 = BalanceRecord(document=self.document_ptr, date=self.date, sum=self.sum_in, 
                            account=self.account, currency=self.currency_in)
        br2.save()
        self.balance_records.set([br1, br2])

    
    class Meta():
        verbose_name = "Currency exchange"
        verbose_name_plural = "Currency exchanges"
    
    def clean(self):
        return super().clean()
        # pass
        
        
class BalanceRecord(models.Model):
    
    @classmethod
    def get_balance_undo(cls, account_pk, currency_pk, date, document_pk):
        
        # most be filled, else its dont have matter
        if not account_pk or not currency_pk:
            return None
        
        sum = None
        # it worked if doc not saved and document.date <> date_doc
        if date:
            # return cls.objects.filter(account = acc, currency = curr, date__lte = doc.date).aggregate(sum = models.Sum("sum"))["sum"]
            if document_pk:
                sum = cls.objects.filter(Q(account__pk = account_pk), Q(currency__pk = currency_pk), 
                                        Q(date__lt = date) | Q(date = date) & Q(document__pk__lt = document_pk)
                                        ).aggregate(sum = Sum("sum"))["sum"] 
                
            # it worked if doc not filled and position or doc dont have matter
            else:
                sum = cls.objects.filter(Q(account__pk = account_pk), Q(currency__pk = currency_pk), 
                                        Q(date__lt = date)
                                        ).aggregate(sum = Sum("sum"))["sum"] 
        # if intend acc and curr only - calculate last value
        else:
            sum = cls.objects.filter(account__pk = account_pk, currency__pk = currency_pk).aggregate(sum = Sum("sum"))["sum"]
        
        return sum if sum else 0
    
    @classmethod    
    def getAccountCurrencyCrossTable(cls):
    
        accounts = {}
        currencies = {}
        аverage_balance = 0
        basis_for_persent = 0
        
        dataQS = cls.objects.values("account", "account__name", "currency", "currency__name", "currency__course").annotate(
            cur_sum=Sum("sum"), bal_sum=Sum(F("currency__course")*F("sum")))
        
        
        for record in dataQS:
            
            if not accounts.get(record["account"]):
                accounts[record["account"]] = {}
                
            accounts[record["account"]]["account"] = record["account"]
            accounts[record["account"]]["name"] = record["account__name"]
            accounts[record["account"]][record["currency"]] = {"cur_sum": record["cur_sum"], "bal_sum": record["bal_sum"]}
            accounts[record["account"]]["acc_sum"] =  accounts[record["account"]].get("acc_sum", 0) + record["bal_sum"] 
            
            if not currencies.get(record["currency"]):
                currencies[record["currency"]] = {}
                
            currencies[record["currency"]]["currency"] = record["currency"]
            currencies[record["currency"]]["name"] = record["currency__name"]
            currencies[record["currency"]]["course"] = record["currency__course"]
            currencies[record["currency"]]["cur_sum"] =  currencies[record["currency"]].get("cur_sum", 0) + record["cur_sum"]
            currencies[record["currency"]]["bal_sum"] =  currencies[record["currency"]].get("bal_sum", 0) + record["bal_sum"]
            
            аverage_balance += record["bal_sum"]
            basis_for_persent = basis_for_persent + record["bal_sum"] if record["bal_sum"] > 0 else 0
        
        cur_arr = sorted(currencies.values(), key=lambda cur: cur["course"])
        acc_arr = sorted(accounts.values(), key=lambda acc: -acc["acc_sum"])
        
        for cur in cur_arr:
            cur["percent"] = 0        
            if cur["bal_sum"] > 0 and basis_for_persent > 0:
                cur["percent"] = round(100 * cur["bal_sum"] / basis_for_persent, 2)
        
        for acc in acc_arr:
            acc["currency_sums"] = []
            for cur in cur_arr:
                if acc.get(cur["currency"]):
                    sum = acc[cur["currency"]]["cur_sum"]
                    bal_sum = acc[cur["currency"]]["bal_sum"]
                    if cur["course"] > 1:
                        acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f} ({bal_sum:.2f})"})
                    else:
                        acc["currency_sums"].append({"bal_sum": bal_sum, "sum_view":f"{sum:.2f}"})
                else:
                    acc["currency_sums"].append({"bal_sum": 0, "sum_view":"-"})
            
            acc["percent"] = 0        
            if acc["acc_sum"] > 0 and basis_for_persent > 0:
                acc["percent"] = round(100 * acc["acc_sum"] / basis_for_persent, 2) 
        
        
        return {"accounts": acc_arr, "currencies": cur_arr, "balance": аverage_balance}
    
    date     = models.DateTimeField(verbose_name="Date", default=django.utils.timezone.now)
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Sum", default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Currency", default=1)
    balance  = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Balance", default=0)
    account  = models.ForeignKey(Account, on_delete=models.PROTECT, verbose_name="Account", related_name="balance_records")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Document", related_name="balance_records")
    
    def __str__(self, *args, **kwargs):
        return "{0} to {1} from {2}".format(self.sum, self.account, self.document)
    
class BudgetRecord(models.Model):
    
    date     = models.DateTimeField(verbose_name="Дата", default=django.utils.timezone.now)
    sum      = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Sum", default=0)
    budget  = models.ForeignKey(Budget, on_delete=models.PROTECT, verbose_name="Budget", related_name="budget_records")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name="Document", related_name="budget_records")