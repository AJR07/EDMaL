# Gunicorn configuration file

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = "0.0.0.0:50505"

workers = 4
threads = workers

timeout = 200