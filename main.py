import json
from datetime import datetime
import urllib.request
import urllib.parse

PLANT_ID = 4137574

def main():
    plant_data = None
    status = "error"
    error_message = None

    try:
        # Використовуємо прямий публічний запит до веб-інтерфейсу сервера Growatt
        url = f"https://server.growatt.com/panel/propagand/getPlantData?plantId={PLANT_ID}"
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://server.growatt.com/'
            }
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_text = response.read().decode('utf-8')
            res_data = json.loads(res_text)
            
            if res_data:
                plant_data = res_data
                status = "success"
            else:
                error_message = "Empty data received"
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

    print("Файл data.json оновлено зі статусом:", status)

if __name__ == "__main__":
    main()
