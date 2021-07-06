from baguette_bi.server import settings, startup

wsgi_app = "baguette_bi.server.app:app"
preload_app = True
daemon = settings.web_daemon
bind = f"{settings.web_host}:{settings.web_port}"
workers = settings.web_workers

worker_class = "uvicorn.workers.UvicornWorker"
max_requests = settings.web_max_requests
max_requests_jitter = max_requests // 10

accesslog = "-"
errorlog = "-"
loglevel = "info"

user = None
group = None


def on_starting(server):
    startup.run()
