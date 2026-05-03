from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
import ssl
import time
import requests
from urllib.parse import urlparse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_url(url: str):
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    return parsed.scheme, parsed.hostname, url



@app.get("/")
def home():
    return {
        "message": "🚀 Internet Visualizer Backend Running"
    }



@app.get("/analyze")
def analyze(url: str):
    try:
        scheme, host, full_url = parse_url(url)

        result = {
            "host": host,
            "url": full_url,
            "ip": None,
            "dns_time_ms": 0,
            "tcp_time_ms": 0,
            "tls_time_ms": 0,
            "http_time_ms": 0,
            "total_time_ms": 0
        }

        total_start = time.time()

     
        start = time.time()
        ip = socket.gethostbyname(host)
        result["ip"] = ip
        result["dns_time_ms"] = (time.time() - start) * 1000

     
        port = 443 if scheme == "https" else 80
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        start = time.time()
        sock.connect((host, port))
        result["tcp_time_ms"] = (time.time() - start) * 1000

       
        if scheme == "https":
            context = ssl.create_default_context()

            start = time.time()
            secure_sock = context.wrap_socket(sock, server_hostname=host)
            result["tls_time_ms"] = (time.time() - start) * 1000
            secure_sock.close()
        else:
            sock.close()

       
        start = time.time()
        requests.get(full_url)
        result["http_time_ms"] = (time.time() - start) * 1000

       
        result["total_time_ms"] = (time.time() - total_start) * 1000

        return result

    except Exception as e:
        return {
            "error": str(e),
            "message": "Something went wrong while analyzing the URL"
        }
