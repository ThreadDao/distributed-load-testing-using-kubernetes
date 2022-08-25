import random
from locust import HttpUser, task


class PineconeUser(HttpUser):

    @task
    def query_task(self):
        # index_name = "sift-128"
        # url = "https://latency-10m-2p-0d908f2.svc.us-west1-gcp.pinecone.io/query"
        url = "https://sift-128-euclidean-61a3a8a.svc.us-west1-gcp.pinecone.io/query"
        dim = 128
        nq = 1
        query_vec = []
        for _ in range(nq):
            values = [random.random() for _ in range(dim)]
            query_vec.append({"values": values})
        data = {
            "namespace": "",
            "topK": 1,
            "includeValues": False,
            "includeMetadata": False,
            "vector": query_vec
        }
        headers = {
            "Content-Type": "application/json",
            "Api-Key": "d3cce957-2401-4c94-832a-6db8eee658e5"
        }
        self.client.post(url=url, headers=headers, json=data)
