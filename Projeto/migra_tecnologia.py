import os
from django.core.files import File
from portfolio.models import Tecnologia

for obj in Tecnologia.objects.all():
    if obj.logo and obj.logo.name:
        local_path = os.path.join('media', obj.logo.name)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.logo.save(os.path.basename(local_path), File(f), save=True)
            print(f"Migrado: {obj}")
        else:
            print(f"Ficheiro não encontrado: {local_path}")
