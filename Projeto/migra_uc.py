import os
from django.core.files import File
from portfolio.models import UC

for obj in UC.objects.all():
    if obj.imagem and obj.imagem.name:
        local_path = os.path.join('media', obj.imagem.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.imagem.save(os.path.basename(local_path), File(f), save=True)
            print(f"Migrado: {obj}")
        else:
            print(f"Ficheiro não encontrado: {local_path}")
