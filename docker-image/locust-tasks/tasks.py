import random
import os
from locust import HttpUser, task

url = os.environ["url"]
dim = os.environ["dim"]
api_key = os.environ["api_key"]


class PineconeUser(HttpUser):

    @task
    def query_task(self):
        query_vec = [random.random() for _ in range(dim)]
        data = {
            "namespace": "",
            "topK": 1,
            "includeValues": False,
            "includeMetadata": False,
            "vector": query_vec
        }
        headers = {
            "Content-Type": "application/json",
            "Api-Key": api_key
        }
        self.client.post(url=url, headers=headers, json=data)
