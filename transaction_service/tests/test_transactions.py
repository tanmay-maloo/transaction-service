from django.test import TestCase, Client
from transactions import models
from django.urls import reverse
from rest_framework import status

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        self.transaction_post_url = reverse('transaction_view', kwargs={"filter":"transaction", "filterVariable":123})
        self.transaction_get_url = reverse('transaction_view', kwargs={"filter":"transaction", "filterVariable":321})
        self.transaction_sum_url = reverse('transaction_view', kwargs={"filter":"sum", "filterVariable":321})
        self.transaction_types_filter_url = reverse('transaction_view', kwargs={"filter":"types", "filterVariable":'credit2'})

    def test_create_transaction(self):

        data = {
            "amount": 1000,
            "type": "credit"
        }
        response = self.client.post(self.transaction_post_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})
        
        transaction = models.Transaction.objects.get(id=123)
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.type, "credit")
        self.assertIsNone(transaction.parent)

    def test_get_transaction(self):
        models.Transaction.objects.create(id='321', amount=1001, type='credit2')
        response = self.client.get(self.transaction_get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], 1001)
        self.assertEqual(response.data["type"], "credit2")
        self.assertIsNone(response.data["parent"])
    
    def test_sum_transaction(self):
        first_transaction = models.Transaction.objects.create(id='321', amount=1001, type='credit2')
        second_transaction = models.Transaction.objects.create(id='322', amount=101, type='credit2',parent=first_transaction)
        models.Transaction.objects.create(id='323', amount=10, type='credit2',parent=second_transaction)
        response = self.client.get(self.transaction_sum_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["transaction_sum"], 1112)
    
    def test_types_transaction(self):
        first_transaction = models.Transaction.objects.create(id='321', amount=1001, type='credit2')
        models.Transaction.objects.create(id='322', amount=101, type='credit2',parent=first_transaction)
        response = self.client.get(self.transaction_types_filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = [{'id': '321', 'amount': 1001.0, 'type': 'credit2', 'parent': None}, {'id': '322', 'amount': 101.0, 'type': 'credit2', 'parent': '321'}]
        self.assertEqual(response.data['data'], expected_response)
