import os
from growattServer import GrowattApi

# Отримання даних для підключення з безпечних секретів GitHub Actions
USERNAME = os.getenv("GROWATT_USER")
PASSWORD = os.getenv("GROWATT_PASSWORD")
PLANT_ID = 4137574  # Ваш числовий Plant ID
DATALOGGER_SN = "PFQ0G620VL"  # Ваш даталоггер


def main():
  print("Спроба підключення до сервера Growatt...")

  # Перевірка наявності змінних середовища
  if not USERNAME or not PASSWORD:
    print(
        "Помилка: Не знайдено змінні середовища GROWATT_USER або"
        " GROWATT_PASSWORD."
    )
    return

  api = GrowattApi()

  # Авторизація в системі Growatt
  login_response = api.login(USERNAME, PASSWORD)
  if not login_response or "userId" not in login_response:
    print(
        "Помилка: Не вдалося увійти в акаунт Growatt. Перевірте секрети на GitHub."
    )
    return

  print("Успішний вхід в акаунт Growatt!")

  # Отримання деталей по станції (Plant ID: 4137574)
  plant_data = api.plant_detail(PLANT_ID)
  print("Дані станції успішно отримані:")
  print(plant_data)


if __name__ == "__main__":
  main()
