# Author: Valley-e
# Date: 2025/2/6  
# Description:
import requests


def get_location():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        return {
            "ip": data.get("ip"),
            "country": data.get("country"),  # 国家代码，如 "US"
            "region": data.get("region"),  # 省份/州
            "city": data.get("city")  # 城市
        }
    except requests.RequestException as e:
        print("Error fetching location:", e)
        return None


def get_default_language():
    if get_location() is not None:
        if get_location()['country'] == 'CN':
            return 'zh'
        else:
            return 'en'
    else:
        return 'en'


if __name__ == "__main__":
    location = get_location()
    if location:
        print(
            f"IP: {location['ip']}, Country: {location['country']}, Region: {location['region']}, City: {location['city']}")
