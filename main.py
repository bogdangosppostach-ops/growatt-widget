import json
import os
from datetime import datetime
from growattServer import GrowattApi

USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574
LOGGER_SN = "QAS3G6F04S"

def main():
    plant_data = None
    status = "error"
    error_message = None

    if not USERNAME or not PASSWORD:
        error_message = "Missing environment variables"
    else:
        try:
            api = GrowattApi()
            # Авторизуємося через офіційну бібліотеку, яка підтримує гібридні інвертори
            login_response = api.login(USERNAME, PASSWORD)
            
            if login_response and ("userId" in login_response or login_response.get("success") == True):
                try:
                    # Отримуємо детальні дані саме по інвертору/гібридній станції
                    detail = api.plant_detail(PLANT_ID)
                    
                    # Шукаємо пристрої (інвертори) у станції
                    inverters = detail.get('data', {}).get('inverterList', [])
                    inv_data = inverters[0] if inverters else detail
                    
                    plant_data = {
                        "invetorPower": inv_data.get('ppv', inv_data.get('pac', 0)),
                        "todayEnergy": inv_data.get('etoday', 0),
                        "status": inv_data.get('status', 1)
                    }
                    status = "success"
                except Exception as e:
                    error_message = f"Detail error: {str(e)}"
            else:
                error_message = f"Login failed: {login_response}"
        except Exception as e:
            error_message = str(e)

    data_to_save = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plant_id": PLANT_ID,
        "logger_sn": LOGGER_SN,
        "status": status,
        "error": error_message,
        "plant_data": plant_data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    print("Дані гібридного інвертора оновлено зі статусом:", status)

if __name__ == "__main__":
    main()
