import csv
import random


def process_data(input_file, output_file, n):
    # Читаємо дані з CSV файлу
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаємо заголовок
        coordinates = [(float(lat), float(lon)) for lat, lon in reader]

    # Отримуємо лише унікальні координати
    unique_coordinates = list(set(coordinates))
    print(f"{len(unique_coordinates) = }")

    # Взяти 0.7*n унікальних координат з повтореннями і до кожної з них
    # приписати ще рандомне число від 0 до 100 (всього буде n записів)
    result = [(random.randint(0, 100), lat, lon) for lat, lon in random.choices(unique_coordinates[:int(0.7*n)], k=n)]

    # Записуємо результат в csv файл
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["empty_count", "longitude", "latitude"])
        writer.writerows(result)


# Викликаємо функцію з вашими файлами і n=10
process_data('gps.csv', 'parking.csv', 40)
