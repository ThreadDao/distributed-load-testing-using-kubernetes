import random
import os
import h5py
from locust import HttpUser, task

data_dir = '/data'

url = os.environ["TARGET_HOST"]
api_key = os.environ["api_key"]
top_k = os.environ["top_k"]
file_name = os.environ["fname"]


class ChunkData(object):
    def __init__(self, fname):
        f = h5py.File(fname, 'r')
        self.data = f['test']
        self.total = self.data.shape[0]

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            _id = random.randint(0, self.total - 1)
            print(f"random vector pos {_id}")
            d = self.data[_id].tolist()
            return d
        raise StopIteration()


class PineconeUser(HttpUser):

    @task
    def query_task(self):
        chunk_data = ChunkData(f'{data_dir}/{file_name}')
        query_vec = chunk_data.__next__()
        data = {
            "namespace": "",
            "topK": int(top_k),
            "includeValues": False,
            "includeMetadata": False,
            "vector": query_vec
        }
        headers = {
            "Content-Type": "application/json",
            "Api-Key": api_key
        }
        self.client.post(url=url, headers=headers, json=data)
