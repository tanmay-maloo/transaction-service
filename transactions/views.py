from rest_framework.views import APIView
from transactions.models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer


def index(request):
    return Response("Hello, world. use GET /transactionservice/transaction/<Id> to get the transaction")

class TransactionView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            response = None
            filter = kwargs.get('filter','')
            filterVariable = kwargs.get('filterVariable', '')
            if(filter == 'transaction'):
                response = self.getTransaction(filterVariable)
            elif(filter == 'types'):
                response = self.getTransactionByType(filterVariable)
            elif(filter == 'sum'):
                response = self.getAggregatedSumById(filterVariable)
            else:
                Response({"error": f"Invalid request: {filter}"}, status=status.HTTP_400_BAD_REQUEST)
            if(response==None):
                return Response({"error": f"filter required for {filter} is not valid"}, status=status.HTTP_404_NOT_FOUND)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, *args, **kwargs):
        try:
            filter = kwargs.get('filter','')
            transaction_id = kwargs.get('filterVariable', '')
            if(filter == 'transaction'):
                
                parent = None
                amount = request.data.get("amount")
                type = request.data.get("type")
                if(request.data.get("parent_id")):
                    parent_id = request.data.get("parent_id")
                    parent  = Transaction.objects.get(id = parent_id)
                Transaction.objects.create(id=transaction_id, amount=amount, type=type, parent=parent)
                return Response({"status":"ok"}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def getTransaction(self, transaction_id):
        try:
            transaction  = Transaction.objects.get(id = transaction_id)
            serializer = TransactionSerializer(transaction, many=False)
            return serializer.data
        except Transaction.DoesNotExist:
            return None
        except Exception:
            raise Exception
    
    def getTransactionByType(self, transaction_type):
        try:
            transactions  = Transaction.objects.filter(type=transaction_type)
            serializer = TransactionSerializer(transactions, many=True)
            return {"data": serializer.data}
        except Transaction.DoesNotExist:
                return None
        except Exception:
            raise Exception
        
    def getAggregatedSumById(self, transaction_id):
        try:
            transaction  = Transaction.objects.get(id = transaction_id)
            return {"transaction_sum": transaction.transaction_sum}
        except Transaction.DoesNotExist:
                return None
        except Exception:
            raise Exception
