from config import BASE_URL
from urllib.parse import quote

def qr_code_maker(type: str, name: str):
    route_url = f"{BASE_URL}/route-to-app?type={type}&name={name}"
    encoded_url = quote(route_url, safe="")    
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=120x120&data={encoded_url}"
    return qr_code_url