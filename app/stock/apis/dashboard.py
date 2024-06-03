from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response

from stock.models import Order


class DashboardApi(APIView):
    def get(self, request):
        seven_days_ago = datetime.now() - timedelta(days=7)
        last_seven_days_order = (
            Order.objects.filter(is_deleted=False, created_date__gte=seven_days_ago.date()).prefetch_related(
                "product", "customer").values(
                    "created_date",
                    "product__product_name",
                    "customer__first_name",
                    "customer__last_name",
                    "status"
                )
        )
        data = {}

        for entry in last_seven_days_order:
            if entry["status"] not in data:
                data.update({
                    entry["status"]: {}
                })
            if str(entry["created_date"]) in data[entry["status"]]:
                data[entry["status"]][str(entry["created_date"])].append([{
                    "product": entry["product__product_name"],
                    "customer": entry["customer__first_name"] + " " + entry["customer__last_name"],
                }])
            else:
                data[entry["status"]][str(entry["created_date"])] = [{
                    "product": entry["product__product_name"],
                    "customer": entry["customer__first_name"] + " " + entry["customer__last_name"],
                }]
        return Response({'dashboard_data': data})
