import os
from growattServer import GrowattApi

# Дані для підключення до вашої станції Growatt
# (Замініть 'YOUR_USERNAME' та 'YOUR_PASSWORD' на ваші реальні дані облікового запису Growatt)
USERNAME = os.getenv("GROWATT_USER", "YOUR_USERNAME")
PASSWORD = os.getenv("GROWATT_PASSWORD", "YOUR_PASSWORD")
PLANT_ID = 4137574  # Ваш числовий Plant ID
DATALOGGER_SN = "PFQ0G620VL"  # Ваш даталоггер


def main():
  print("Спроба підключення до серверну Growatt...")

  api = GrowattApi()

  # Авторизація в системі Growatt
  login_response = api.login(USERNAME, PASSWORD)
  if not login_response or "userId" not in login_response:
    print("Помилка: Не вдалося увійти в акаунт Growatt. Перевірте логін та пароль.")
    return

  print("Успішний вхід в акаунт Growatt!")

  # Отримання деталей по станції (Plant ID: 4137574)
  plant_data = api.plant_detail(PLANT_ID)
  print(f"Дані станції успішно отримані:")
  print(plant_data)


if __name__ == "__main__":
  main()
