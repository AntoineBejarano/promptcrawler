"""
Script para ejecutar el worker RQ
"""
import os
import sys
from rq import Worker, Queue, Connection
from redis import Redis
from app.config import settings

if __name__ == '__main__':
    redis_conn = Redis.from_url(settings.REDIS_URL)
    with Connection(redis_conn):
        worker = Worker(['default'])
        worker.work()

