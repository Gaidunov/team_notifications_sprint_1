from typing import Optional


def generate_html_message(
    text: str,
    user_name: Optional[str] = None
) -> str:
    if not user_name:
        user_name = 'пользователь'

    letter = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Уважаемый {user_name}! </title>
        </head>
        <body>
            <p>{text}</p>
            <p>Ваш кинотеатр.</p>
        </body>
    </html>
    """
    return letter
