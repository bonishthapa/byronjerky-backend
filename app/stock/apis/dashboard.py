from rest_framework.views import APIView
from rest_framework.response import Response

from stock.models import Order
from helpers.misc import get_start_and_end_of_week


class DashboardApi(APIView):
    def get(self, request):
        start_date, end_date = get_start_and_end_of_week()
        last_seven_days_order = (
            Order.objects.filter(is_deleted=False, created_date__range=[start_date, end_date]).prefetch_related(
                "product", "customer").values(
                    "created_date",
                    "product__product_name",
                    "customer__first_name",
                    "customer__last_name",
                    "status",
                    "number_of_units",
                    "wet_weight",
                    "order_date",
                    "production_date",
                    "idx"
                )
        )
        data = {}

        for entry in last_seven_days_order:
            if entry["status"] not in data:
                data.update({
                    entry["status"]: {}
                })
            if str(entry["created_date"]) in data[entry["status"]]:
                data[entry["status"]][str(entry["created_date"])].append({
                    "idx": entry["idx"],
                    "product": entry["product__product_name"],
                    "customer": entry["customer__first_name"] + " " + entry["customer__last_name"],
                    "created_date": entry["created_date"],
                    "quantity": entry["number_of_units"],
                    "wet_weight": entry["wet_weight"],
                    "order_date": entry["order_date"],
                    "production_date": entry["production_date"],

                })
            else:
                data[entry["status"]][str(entry["created_date"])] = [{
                    "idx": entry["idx"],
                    "product": entry["product__product_name"],
                    "customer": entry["customer__first_name"] + " " + entry["customer__last_name"],
                    "created_date": entry["created_date"],
                    "quantity": entry["number_of_units"],
                    "wet_weight": entry["wet_weight"],
                    "order_date": entry["order_date"],
                    "production_date": entry["production_date"],
                }]

        return Response({'dashboard_data': data})
