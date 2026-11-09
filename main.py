import json
import os
from datetime import datetime
from growattServer import GrowattApi

USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574


def main():
  print("Спроба підключення до сервера Growatt...")
  plant_data = None
  status = "error"
  error_message = None

  if not USERNAME or not PASSWORD:
    print("Помилка: Не знайдено змінні середовища.")
    error_message = "Missing environment variables"
  else:
    try:
      # Ініціалізуємо API та вмикаємо збереження сесії
      api = GrowattApi()
      
      # Пробуємо авторизуватися
      login_response = api.login(USERNAME, PASSWORD)

      if login_response and "userId" in login_response:
        print("Успішний вхід в акаунт Growatt!")
        try:
          # Отримуємо деталі станції
          plant_data = api.plant_detail(PLANT_ID)
          status = "success"
        except Exception as e:
          print(f"Помилка отримання даних станції: {e}")
          error_message = f"Plant detail error: {str(e)}"
      else:
        print("Помилка: Не вдалося увійти в акаунт Growatt.")
        error_message = "Login failed - invalid credentials"
        
    except Exception as e:
      print(f"Загальна помилка підключення: {e}")
      error_message = str(e)

  # Записуємо результат у data.json у будь-якому випадку, щоб міні-апп не падав
  data_to_save = {
      "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "plant_id": PLANT_ID,
      "status": status,
      "error": error_message,
      "plant_data": plant_data,
  }

  with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_to_save, f, ensure_ascii=False, indent=4)

  print("Файл data.json успішно оновлено.")


if __name__ == "__main__":
  main()
