from decouple import config

broker_url = config("BROKER_URL", default="amqp://redis:redis@localhost:5672/redis")
result_backend = config(
    "CELERY_RESULT_BACKEND",
    default="celery_amqp_backend.AMQPBackend://redis:redis@localhost:5672/redis",
)

broker_transport_options = {"visibility_timeout": 3600}
task_ignore_result = True

task_serializer = "json"
result_serializer = "json"
accept_content = ["application/json", "application/x-python-serialize"]
result_accept_content = ["application/json", "application/x-python-serialize"]
timezone = "Asia/Kathmandu"
