from django.contrib import admin
from .models import Account, BalanceRecord, Budget, BudgetRecord, Cost, Currency, CurrencyExchange, Document, Inventory, Profit, Transfer, User

admin.site.register(User)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    list_display_links = ('id', 'name') 
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Profit)
admin.site.register(Cost)
admin.site.register(Transfer)
admin.site.register(Inventory)
admin.site.register(CurrencyExchange)
admin.site.register(Document)
admin.site.register(BudgetRecord)
admin.site.register(BalanceRecord)
