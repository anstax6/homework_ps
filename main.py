import requests

token = "" #введите сюда ваш токен
version = 5.199
domain = "" #введите ID страницы, с которой хотите получить данные
fields = "bdate,activities,city,occupation"

response = requests.get(
    "https://api.vk.com/method/users.get",
    params={
        "user_ids": domain,
        "access_token": token,
        "v": version,
        "fields": fields,
    },
)

data = response.json()

with open(f"information_about_{domain}.txt", "w") as f: #открываем файл для записи
        if "error" in data:
            print(f"Ошибка от API VK: {data['error']['error_msg']}")
        else:
            try:
                name = data["response"][0]["first_name"] + " " + data["response"][0]["last_name"]
                f.write(f"Имя: {name}\n") #человекочитаемый формат

                user_data = data["response"][0] #упрощаем дальнейший код
                #Дата рождения
                if "bdate" in user_data:
                    f.write(f"Дата рождения: {user_data['bdate']}\n")
                else:
                    f.write("Дата рождения: не указана\n")
                #Город
                if "city" in user_data:
                    f.write(f"Город: {user_data['city']['title']}\n") # Вложенная структура
                else:
                    f.write("Город: не указан\n")
                #Деятельность
                if "activities" in user_data:
                    f.write(f"Деятельность: {user_data['activities']}\n")
                else:
                    f.write("Деятельность: не указана\n")
                #Занятость
                if "occupation" in user_data:
                    occupation_info = user_data['occupation']
                    occupation_type = occupation_info.get('type', 'Не указано')

                    if occupation_type == 'work':
                        occupation_name = occupation_info.get('name', 'Не указано')
                        f.write(f"Работа: {occupation_name}")

                    if occupation_type == 'school':
                        school_name = occupation_info.get('name', 'Не указано')
                        f.write(f"Учеба: {school_name}")

                    if occupation_type == 'university':
                        university_name = occupation_info.get('name', 'Не указано')
                        f.write(f"Университет: {university_name}")

                    if occupation_type not in ('work', 'school', 'university', 'Не указано'):  #Обработка других типов
                        f.write(f"Занятие: {occupation_type}")
                else:
                    f.write("Занятие: не указано")

            #Вывод ошибок при обнаружении
            except KeyError as e:
                f.write(f"Ошибка: Не найдено поле {e} в ответе API. Проверьте токен и permissions.\n")
            except IndexError:
                f.write("Ошибка: Неверный user_id или аккаунт приватный.\n")