from statick.letter_template import sample


def get_user_data(user_id):
    

def send_message(message, user_id):
    # Достать данные пользователя запрос в auth сервис
    user_data = get_user_data(user_id)
    # проверка тайм зоны пользователя

    # понять тип отправки
    type_send = user_data['type_send']
    if type_send == 'email':
        ...
    elif type_send == 'push':
        ...
    elif type_send == 'websockets':
        ...
    # Сформировать уведомление
    # Отправить уведомление