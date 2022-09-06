import random
from locust import HttpUser, task


class PineconeUser(HttpUser):

    @task
    def query_task(self):
        url = "https://sift-128-euclidean-61a3a8a.svc.us-west1-gcp.pinecone.io/query"
        # url = "https://random-1m-768-0d908f2.svc.us-west1-gcp.pinecone.io/query"
        dim = 768
        # nq = 1
        # query_vec = []
        # for _ in range(nq):
        #     values = [random.random() for _ in range(dim)]
        #     query_vec.append({"values": values})
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
            "Api-Key": "d3ccxxx-xxx-xxx-xxx-xxx58e5"
        }
        self.client.post(url=url, headers=headers, json=data)
