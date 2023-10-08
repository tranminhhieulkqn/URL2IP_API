import re
from fastapi import FastAPI, status
import socket

app = FastAPI()

@app.get("/")
@app.get("/ping")
def pong(status_code = status.HTTP_200_OK):
    return {
        "message": "pong"
    }

@app.get("/ip/{domain_target}")
def check_ip(domain_target: str):
    ipv4 = set([])
    ipv6 = set([])
    try:
        addrinfo = socket.getaddrinfo(domain_target, None)
        for addr in addrinfo:
            ip_address = addr[4][0]
            if re.match(pattern=r'(\d){1,3}(\.(\d){1,3}){3}', string=ip_address):
                ipv4.add(ip_address)
            else:
                ipv6.add(ip_address)
        return {
            "domain": domain_target,
            "ipv4": list(sorted(ipv4)),
            "ipv6": list(sorted(ipv6))
        }
    except socket.gaierror as err:
        return {
            "error": "Invalid domain",
            "error_infor": str(err)
        }
    except Exception as err:
        return {
            "error": "Other err",
            "error_infor": str(err)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, workers=10, reload=True)