import json
import os
from datetime import datetime
from growattServer import GrowattApi

USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574


def main():
  print("Спроба підключення до сервера Growatt...")
  if not USERNAME or not PASSWORD:
    print("Помилка: Не знайдено змінні середовища.")
    return

  api = GrowattApi()
  try:
    login_response = api.login(USERNAME, PASSWORD)
  except Exception as e:
    print(f"Помилка підключення до API: {e}")
    return

  if not login_response or "userId" not in login_response:
    print(
        "Помилка: Не вдалося увійти. Перевірте логін та пароль у GitHub"
        " Secrets."
    )
    return

  print("Успішний вхід в акаунт Growatt!")
  plant_data = api.plant_detail(PLANT_ID)

  data_to_save = {
      "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "plant_id": PLANT_ID,
      "plant_data": plant_data,
  }

  with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

  print("Дані успішно збережено у файл data.json")


if __name__ == "__main__":
  main()
