import requests
from portfolio.models import Licenciatura, UC


def loader_uc(course_code=260, year="202526", language="PT", debug=True):
    print(f"A carregar curso {course_code} ({language})")

    url = "https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail"

    payload = {
        "language": language,
        "courseCode": course_code,
        "schoolYear": year
    }

    headers = {"content-type": "application/json"}

    print("📡 A enviar request...")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print("📡 Status code:", response.status_code)

        if response.status_code != 200:
            print(" Erro na API:", response.text)
            return

        data = response.json()

    except requests.exceptions.Timeout:
        print(" TIMEOUT: API não respondeu a tempo")
        return
    except Exception as e:
        print(" ERRO:", e)
        return

    if debug:
        print("\n CURSO:")
        print(data.get("courseName"))

        print("\n UCs encontradas:")
        for uc in data.get("courseFlatPlan", []):
            print("-", uc.get("curricularIUnitReadableCode"), uc.get("curricularUnitName"))

        print("\n DEBUG ON: nada foi guardado na base de dados")
        return