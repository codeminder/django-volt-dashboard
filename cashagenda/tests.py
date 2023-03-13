from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import *
from datetime import date, timedelta
import math

class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12',
                                                         email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

class CreateDeleteDocumentTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12',
                                                         email='test@example.com')
        self.user.save()
        self.start_timestamp = date.today()
        self.acc1 = Account(name="Acc1", owner = self.user)
        self.acc1.save()
        self.acc2 = Account(name="Acc2", owner = self.user)
        self.acc2.save()
        self.cur1 = Currency(name="Currency1", short_name = "cu1", course = 1)
        self.cur1.save()
        self.budget = Budget(name="budget number 1", short_name = "budg")
        self.budget.save()
        

    def tearDown(self):
        self.user.delete()

    def test_cost_creation_correct(self):
        test_cost = Cost(account=self.acc1, sum=24.12, currency=self.cur1, comment="comment", budget=self.budget)
        test_cost.save()
        self.assertEqual(Cost.objects.all().count(), 1)
        self.assertTrue(math.isclose(-24.12, BalanceRecord.get_balance_undo(account_pk=self.acc1.pk, 
                                                                currency_pk=self.cur1.pk, 
                                                                date=None, document_pk=None)))
        # self.assertEqual(-24.12, BalanceRecord.get_balance_undo(account_pk=self.acc1.pk, 
        #                                                         currency_pk=self.cur1.pk, 
        #                                                         date=None, document_pk=None))
