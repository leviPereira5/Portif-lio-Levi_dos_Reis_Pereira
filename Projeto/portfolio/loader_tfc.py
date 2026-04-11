import json
import os
from portfolio.models import (
    TFC, Utilizador, Docente, Tecnologia,
    Area, PalavraChave, Licenciatura
)

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FICHEIRO_JSON = os.path.join(DIRETORIO_BASE, "data", "tfcs_2025.json")


def separar_valores(valor_bruto):
    if not valor_bruto:
        return []
    if isinstance(valor_bruto, list):
        return [valor.strip().replace(".", "") for valor in valor_bruto if valor.strip()]
    return [valor.strip().replace(".", "") for valor in valor_bruto.split(",") if valor.strip()]


def carregar_tfcs():
    with open(CAMINHO_FICHEIRO_JSON, encoding="utf-8") as ficheiro_json:
        dados_json = json.load(ficheiro_json)

    lista_tfcs = dados_json.get("TFCs_2025", [])

    print(f"Total de TFCs: {len(lista_tfcs)}\n")

    for item_tfc in lista_tfcs:
        titulo_tfc = item_tfc.get("titulo")

        # LICENCIATURA
        nome_licenciatura = item_tfc.get("licenciatura")
        instancia_licenciatura = None

        if nome_licenciatura:
            instancia_licenciatura = Licenciatura.objects.create(
                nome=nome_licenciatura.strip(),
                utilizador_id=1
            )

        # TFC
        instancia_tfc = TFC.objects.create(
            titulo=titulo_tfc,
            descricao=item_tfc.get("sumario"),
            ano=int(item_tfc.get("ano", 0)),
            classificacao=item_tfc.get("rating", 0),
            pdf=item_tfc.get("pdf", ""),
            imagem=item_tfc.get("imagem", None),
            licenciatura=instancia_licenciatura
        )

        # AUTORES
        for nome_autor in separar_valores(item_tfc.get("autores")):
            instancia_autor = Utilizador.objects.create(
                nome=nome_autor,
                email="default@email.com"
            )
            instancia_tfc.autores.add(instancia_autor)

        # ORIENTADORES
        for nome_docente in separar_valores(item_tfc.get("orientadores")):
            instancia_docente = Docente.objects.create(nome=nome_docente)
            instancia_tfc.orientadores.add(instancia_docente)

        # TECNOLOGIAS
        for nome_tecnologia in separar_valores(item_tfc.get("tecnologias")):
            instancia_tecnologia = Tecnologia.objects.create(
                nome=nome_tecnologia,
                tipo="geral",
                descricao="",
                website_url="",
                nivel_preferencia=1
            )
            instancia_tfc.tecnologias.add(instancia_tecnologia)

        # ÁREAS
        for nome_area in separar_valores(item_tfc.get("areas")):
            instancia_area = Area.objects.create(nome=nome_area)
            instancia_tfc.areas.add(instancia_area)

        # PALAVRAS-CHAVE
        for nome_palavra in separar_valores(item_tfc.get("palavras_chave")):
            instancia_palavra = PalavraChave.objects.create(nome=nome_palavra)
            instancia_tfc.palavras_chave.add(instancia_palavra)

        print(f"Criado o TFC com título: {titulo_tfc}")

    print("\n A importação funcionou (EU ACHO :) !!! )")