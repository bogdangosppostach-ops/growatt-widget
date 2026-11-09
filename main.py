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
    print(f"Помилка логіну: {e}")
    return

  if not login_response or "userId" not in login_response:
    print("Помилка: Не вдалося увійти в акаунт Growatt.")
    return

  print("Успішний вхід в акаунт Growatt!")

  # Безпечне отримання даних станції
  try:
    plant_data = api.plant_detail(PLANT_ID)
  except Exception as e:
    print(f"Помилка отримання даних станції: {e}")
    plant_data = {"status": "error", "message": str(e)}

  data_to_save = {
      "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "plant_id": PLANT_ID,
      "plant_data": plant_data,
  }

  # Гарантований запис файлу data.json у корінь репозиторію
  with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

  print("Файл data.json успішно створено та записано.")


if __name__ == "__main__":
  main()
