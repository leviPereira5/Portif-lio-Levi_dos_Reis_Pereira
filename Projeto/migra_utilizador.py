import os
from django.core.files import File
from portfolio.models import Utilizador

for obj in Utilizador.objects.all():
    if obj.foto and obj.foto.name:
        local_path = os.path.join('media', obj.foto.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.foto.save(os.path.basename(local_path), File(f), save=True)
            print(f"Migrado: {obj}")
        else:
            print(f"Ficheiro não encontrado: {local_path}")
