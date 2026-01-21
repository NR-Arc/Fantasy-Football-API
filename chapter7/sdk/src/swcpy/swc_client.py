import httpx

class SWCClient:
    def __init__(self, swc_base_url: str):
        self.base_url = swc_base_url
    
    def get_health_check(self) -> bool:
        # make the API call
        with httpx.Client(base_url=self.base_url) as client:
            response = client.get("/")
            response.raise_for_status()
            return response.json().get("status") == "healthy"