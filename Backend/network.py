from fastapi import Request

class Network:
    async def get_ip(self, request: Request) -> str:
        client_ip = request.client.host

        return {"ip": client_ip}