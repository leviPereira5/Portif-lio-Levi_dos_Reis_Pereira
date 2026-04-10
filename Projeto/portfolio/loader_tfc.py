import json
import os
from django.db import transaction
from portfolio.models import (
    TFC, Utilizador, Docente, Tecnologia,
    Area, PalavraChave, Licenciatura
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "tfcs_2025.json")


def split_values(value):
    """
    Converte strings tipo:
    "A, B, C" -> ["A", "B", "C"]
    """
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [v.strip() for v in value.split(",") if v.strip()]


@transaction.atomic
def load_tfc(debug=True):
    print(f"A abrir: {JSON_PATH}")

    if not os.path.exists(JSON_PATH):
        print("❌ Ficheiro não encontrado!")
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    tfcs = data.get("TFCs_2025", [])

    print(f"Total de TFCs: {len(tfcs)}\n")

    for item in tfcs:
        titulo = item.get("titulo")

        if debug:
            print(f"📌 A processar: {titulo}")

        # -------------------------
        # 1. Criar TFC
        # -------------------------
        tfc = TFC.objects.create(
            titulo=titulo,
            descricao=item.get("sumario", ""),
            ano=int(item.get("ano", 0)) if item.get("ano") else 0,
            classificacao=item.get("rating", 0) or 0
        )

        # -------------------------
        # 2. AUTORES (M2M)
        # -------------------------
        for nome in split_values(item.get("autores")):
            autor, _ = Utilizador.objects.get_or_create(nome=nome)
            tfc.autores.add(autor)

        # -------------------------
        # 3. ORIENTADORES (M2M)
        # -------------------------
        for nome in split_values(item.get("orientadores")):
            docente, _ = Docente.objects.get_or_create(nome=nome)
            tfc.orientadores.add(docente)

        # -------------------------
        # 4. TECNOLOGIAS (M2M)
        # -------------------------
        for tech in split_values(item.get("tecnologias")):
            t, _ = Tecnologia.objects.get_or_create(
                nome=tech,
                defaults={
                    "tipo": "geral",
                    "descricao": "",
                    "website_url": "",
                    "nivel_preferencia": 1
                }
            )
            tfc.tecnologias.add(t)

        # -------------------------
        # 5. ÁREAS (M2M)
        # -------------------------
        for area in split_values(item.get("areas")):
            a, _ = Area.objects.get_or_create(nome=area)
            tfc.areas.add(a)

        # -------------------------
        # 6. PALAVRAS-CHAVE (M2M)
        # -------------------------
        for palavra in split_values(item.get("palavras_chave")):
            p, _ = PalavraChave.objects.get_or_create(nome=palavra)
            tfc.palavras_chave.add(p)

        print(f"✔ Criado: {titulo}\n")

    print("🎉 Importação concluída!")