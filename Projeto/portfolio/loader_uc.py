import os
import requests

from portfolio.models import Licenciatura, UC, Utilizador, Docente


CURSOS = [260, 1504, 12]
ANO_LECTIVO = "202526"

BASE_URL = "https://secure.ensinolusofona.pt/dados-publicos-academicos/resources"


def obter_nome_curso(dados):
    detail = dados.get("courseDetail", {})
    return (
        detail.get("courseName")
        or dados.get("courseName")
        or dados.get("name")
        or "Curso sem nome"
    )


def obter_descricao_curso(dados):
    detail = dados.get("courseDetail", {})
    return detail.get("presentation", "")


def obter_duracao(dados):
    detail = dados.get("courseDetail", {})
    semesters = detail.get("semesters")
    try:
        return int(semesters) // 2
    except:
        return None


def normalizar_semestre(valor):
    if valor in ["1º Semestre", "S1"]:
        return 1
    if valor in ["2º Semestre", "S2"]:
        return 2
    return None


def normalizar_ano(valor):
    try:
        return int(valor)
    except:
        return None


def post_api(endpoint, payload):
    try:
        resposta = requests.post(
            f"{BASE_URL}/{endpoint}",
            json=payload,
            timeout=15
        )
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        print(f"Erro na API ({endpoint}): {e}")
        return None


def importar_docentes(dados, licenciatura):
    docentes_importados = {}

    for t in dados.get("teachers", []):
        nome  = t.get("academicName") or t.get("fullName", "")
        email = t.get("email", "")

        if not nome:
            continue

        email_final = email if email else f"docente-{t.get('employeeCode', 0)}@ulusofona.pt"

        docente, criado = Docente.objects.get_or_create(
            email=email_final,
            defaults={
                "nome": nome,
                "pagina_pessoal": (
                    f"https://www.cienciavitae.pt/{t['cienciaVitae']}"
                    if t.get("cienciaVitae") else ""
                ),
            }
        )

        if criado:
            print(f"Docente: {docente.nome}")

        docentes_importados[t.get("employeeCode")] = docente

    return docentes_importados


def importar_detalhes_uc(codigo_uc):

    dados = post_api(
        "GetSIGESCurricularUnitDetails",
        {"language": "PT", "curricularIUnitReadableCode": codigo_uc}
    )

    if not dados:
        return {}, {}

    objetivos = dados.get("objectives", "") or dados.get("syllabus", "") or ""
    conteudos = dados.get("contents", "")   or dados.get("programContents", "") or ""
    descricao = dados.get("description", "") or ""

    campos = {
        "objetivos": objetivos,
        "conteudos": conteudos,
        "descricao": descricao,
    }


    docentes_uc = [
        t.get("employeeCode")
        for t in dados.get("teachers", [])
        if t.get("employeeCode")
    ]

    return campos, docentes_uc


def importar_ucs(dados, licenciatura, docentes_por_codigo):
    for uc in dados.get("courseFlatPlan", []):

        nome_uc   = uc.get("curricularUnitName")
        codigo_uc = uc.get("curricularIUnitReadableCode")
        ano       = normalizar_ano(uc.get("curricularYear"))
        semestre  = normalizar_semestre(uc.get("semester"))
        ects      = uc.get("ects")

        print(f"{nome_uc}")

        campos_extra, docentes_uc_codes = importar_detalhes_uc(codigo_uc)

        uc_obj, criada = UC.objects.get_or_create(
            codigo=codigo_uc,
            defaults={
                "nome":         nome_uc,
                "ano":          ano,
                "semestre":     semestre,
                "ects":         ects,
                "licenciatura": licenciatura,
                **campos_extra,
            }
        )

        if not criada:
            atualizado = False
            for campo, valor in campos_extra.items():
                if valor and not getattr(uc_obj, campo):
                    setattr(uc_obj, campo, valor)
                    atualizado = True
            if atualizado:
                uc_obj.save()

        
        for code in docentes_uc_codes:
            docente = docentes_por_codigo.get(code)
            if docente:
                uc_obj.docentes.add(docente)


def importar_dados():
    utilizador = Utilizador.objects.first()

    print("\nDados da API...\n")

    for codigo in CURSOS:

        print(f"\nCurso {codigo}")

        dados = post_api(
            "GetCourseDetail",
            {
                "language": "PT",
                "courseCode": codigo,
                "schoolYear": ANO_LECTIVO,
            }
        )

        if not dados:
            continue

        nome_curso = obter_nome_curso(dados)
        print(f"{nome_curso}")

        if nome_curso == "Curso sem nome":
            continue

        licenciatura, _ = Licenciatura.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nome":          nome_curso,
                "instituicao":   "Universidade Lusófona",
                "descricao":     obter_descricao_curso(dados),
                "duracao_anos":  obter_duracao(dados),
                "utilizador":    utilizador,
            }
        )

        print(f"\nDocentes...")
        docentes_por_codigo = importar_docentes(dados, licenciatura)

        print(f"\nUCs...")
        importar_ucs(dados, licenciatura, docentes_por_codigo)

    
    print(f" \nLicenciaturas : {Licenciatura.objects.count()}")
    print(f"   Docentes      : {Docente.objects.count()}")
    print(f"   UCs           : {UC.objects.count()}")

importar_dados()