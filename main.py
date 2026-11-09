import json
import os
from datetime import datetime
from growattServer import GrowattApi

USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574

def main():
    plant_data = None
    status = "error"
    error_message = None

    if not USERNAME or not PASSWORD:
        error_message = "Missing environment variables"
    else:
        try:
            api = GrowattApi()
            login_response = api.login(USERNAME, PASSWORD)
            
            if login_response and ("userId" in login_response or login_response.get("success") == True):
                try:
                    plant_data = api.plant_detail(PLANT_ID)
                    status = "success"
                except Exception as e:
                    error_message = f"Plant detail error: {str(e)}"
            else:
                error_message = f"Login failed: {login_response}"
        except Exception as e:
            error_message = str(e)

    data_to_save = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plant_id": PLANT_ID,
        "status": status,
        "error": error_message,
        "plant_data": plant_data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
