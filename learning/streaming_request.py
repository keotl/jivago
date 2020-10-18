import time

import requests


def gen():
    for i in range(0, 5):
        yield f"hello {i}".encode("utf-8")
        time.sleep(10)


res = requests.post("http://localhost:4000/stream", data=gen())

print(res.status_code)
