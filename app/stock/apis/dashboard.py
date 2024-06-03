from datetime import datetime, timedelta
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response

from stock.models import Order


class DashboardApi(APIView):
    def get(self, request):
        seven_days_ago = datetime.now() - timedelta(days=7)
        last_seven_days_order = (
            Order.objects.filter(is_deleted=False, created_date__gte=seven_days_ago.date()).prefetch_related(
                "product", "customer").values(
                    "created_date", "product__product_name", "customer__first_name", "customer__last_name").annotate(
                        count=Count("id"))
        )
        data = {}
        for entry in last_seven_days_order:
            data[str(entry["created_date"])] = {
                "count": entry["count"],
                "product": entry["product__product_name"],
                "customer": entry["customer__first_name"] + " " + entry["customer__last_name"],
            }
        return Response({'dashboard_data': data})
