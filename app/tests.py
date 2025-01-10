from django.test import TestCase
from app import models as m

# Create your tests here.

class TestApp(TestCase):

    def test_create_profile(self):
        profile1 = m.create_profile('Spencer Hillhouse', '6625423316', 'spencer@gmail.com')
        profile2 = m.create_profile('Daniel', '111-222-3333', 'daniel@gmail.com')
        profile3 = m.create_profile('Jet', '987-654-3210', 'jet@gmail.com')

        self.assertEqual(profile1.id, 1)
        self.assertEqual(profile3.id, 3)
        self.assertEqual(3, len(m.Profile.objects.all()))
        self.assertIn(profile2, m.Profile.objects.all())

    def test_create_savings_account(self):
        profile1 = m.create_profile('Spencer Hillhouse', '6625423316', 'spencer@gmail.com')
        profile2 = m.create_profile('Daniel', '111-222-3333', 'daniel@gmail.com')
        profile3 = m.create_profile('Jet', '987-654-3210', 'jet@gmail.com')

        account1 = m.creaet_savings_account(profile1, 4000)
        account2 = m.creaet_savings_account(profile2, 3.50)
        account3 = m.creaet_savings_account(profile3, 200)



        self.assertEqual(account1.id, 1)
        self.assertEqual(account1.balance, 4000)
        self.assertEqual(3, len(m.SavingsAccount.objects.all()))
        self.assertEqual(account2.balance, 3.50)

    def test_create_transaction(self):
        profile1 = m.create_profile('Spencer Hillhouse', '6625423316', 'spencer@gmail.com')
        profile2 = m.create_profile('Daniel', '111-222-3333', 'daniel@gmail.com')
        profile3 = m.create_profile('Jet', '987-654-3210', 'jet@gmail.com')

        account1 = m.creaet_savings_account(profile1, 4000)
        account2 = m.creaet_savings_account(profile2, '3.50')
        account3 = m.creaet_savings_account(profile3, 200)

        transaction1 = m.create_transaction(profile1, 1500, 'withdraw', 'Hookers and blow')
        transaction2 = m.create_transaction(profile3, 100, 'deposit', "Cause good boy")

        self.assertEqual(transaction1.id, 1)
        self.assertEqual(account1.balance, 2500)
        self.assertEqual(transaction2.id, 2)
        self.assertEqual(account3.balance, 300)