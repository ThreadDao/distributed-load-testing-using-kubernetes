import random
import os
import h5py
import numpy as np
import pandas as pd
from locust import HttpUser, task

url = os.environ["TARGET_HOST"]
api_key = os.environ["api_key"]
top_k = os.environ["top_k"]
file_name = os.environ["fname"]


class ChunkData(object):
    def __init__(self, fname):
        if fname.endswith('hdf5'):
            self.data = h5py.File(fname, 'r')['test']
        elif fname.endswith('npy'):
            self.data = np.load(fname)
        elif fname.endswith('parquet'):
            self.data = pd.read_parquet(fname)['emb']
        else:
            raise Exception(f"Currently only support hdf5 and npy file type")
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
        chunk_data = ChunkData(file_name)
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
