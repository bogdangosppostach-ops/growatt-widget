import json
import os
from datetime import datetime
from growattServer import GrowattApi

USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574
DATALOGGER_SN = "PFQ0G620VL"


def main():
  print("Спроба підключення до сервера Growatt...")
  if not USERNAME or not PASSWORD:
    print("Помилка: Не знайдено змінні середовища.")
    return

  api = GrowattApi()
  login_response = api.login(USERNAME, PASSWORD)
  if not login_response or "userId" not in login_response:
    print("Помилка: Не вдалося увійти в акаунт Growatt.")
    return

  print("Успішний вхід в акаунт Growatt!")
  plant_data = api.plant_detail(PLANT_ID)

  # Формуємо структуру для збереження
  data_to_save = {
      "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "plant_id": PLANT_ID,
      "plant_data": plant_data,
  }

  # Зберігаємо у файл data.json у корінній паці
  with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

  print("Дані успішно збережено у файл data.json")


if __name__ == "__main__":
  main()
