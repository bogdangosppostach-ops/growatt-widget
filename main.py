import json
import os
from datetime import datetime
import urllib.request

PLANT_ID = 4137574

def main():
    plant_data = None
    status = "error"
    error_message = None

    try:
        # Використовуємо публічний API-ендпоинт Growatt без логіна та пароля, які блокує 403
        url = f"https://server.growatt.com/panel/app/getPlantData?plantId={PLANT_ID}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode())
            if res_data:
                plant_data = res_data
                status = "success"
            else:
                error_message = "Empty response from server"
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
