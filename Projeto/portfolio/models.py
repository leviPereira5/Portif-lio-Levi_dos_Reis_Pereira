from django.db import models

#Utilizador "Entidade extra"
#basicamente vai servir para por as minhas informações o famoso "Perfil"
class Utilizador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.ImageField(upload_to='utilizadores/', null=True, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    #Como aparece no admin
    def __str__(self):
        return self.nome
    
#Licenciatura  
class Licenciatura(models.Model):
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20, blank=True)
    codigo = models.IntegerField(null=True, blank=True)  # 👈 importante para API
    instituicao = models.CharField(max_length=150, blank=True)
    descricao = models.TextField(blank=True)
    duracao_anos = models.IntegerField(null=True, blank=True)
    
    #Relacões
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    
    #Como aparece no admin
    def __str__(self):
        return self.nome


#Docente
#class auxiliar 
class Docente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    pagina_pessoal = models.URLField(blank=True)
    foto = models.ImageField(upload_to='docentes/', null=True, blank=True)

    #Como aparece no admin
    def __str__(self):
        return self.nome


#Unidades Curiculares
class UC(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.CharField(max_length=20)
    ano = models.IntegerField(null=True, blank=True)
    semestre = models.IntegerField(null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)
    ects = models.FloatField(null=True, blank=True)
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)

    #Relacões
    licenciatura = models.ForeignKey('Licenciatura', on_delete=models.CASCADE, related_name="ucs")
    docentes = models.ManyToManyField('Docente', blank=True) 

    #Como aparece no admin
    def __str__(self):
        return self.nome    

#Tecnologia    
class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tecnologias/',blank=True, null=True)
    website_url = models.URLField()
    nivel_preferencia = models.IntegerField()

    #Como aparece no admin
    def __str__(self):
        return self.nome
    

#Projeto
class Projeto(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    data = models.DateField()
    imagem = models.ImageField(upload_to='projetos/',blank=True, null=True)
    video_demo = models.URLField(blank=True)
    conceitos_aplicados = models.TextField()
    
    #Relacões
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    uc = models.ForeignKey(UC, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia)
    competencias = models.ManyToManyField('Competencia', blank=True)
    
    #Como aparece no admin
    def __str__(self):
        return self.titulo
    

#Formação
class Formacao(models.Model):
    titulo = models.CharField(max_length=150)
    instituicao = models.CharField(max_length=150)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    certificado_url = models.URLField(blank=True)
    descricao = models.TextField()
    
    #Relacões
    competencias = models.ManyToManyField('Competencia', blank=True)

    #Como aparece no admin
    def __str__(self):
        return self.titulo
    
#Competência
class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)
    descricao = models.TextField()
    
    #Como aparece no admin
    def __str__(self):
        return self.nome
    
    
#Repositorio "Entidade Extra"
class Repositorio(models.Model):
    nome = models.CharField(max_length=150)
    url = models.URLField()
    descricao = models.TextField()
    data_criacao = models.DateField()
    visibilidade = models.CharField(max_length=20)
    
    #Relacões
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True)
    
    #Como aparece no admin
    def __str__(self):
        return self.nome


#TFC
class TFC(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    sumario = models.TextField(blank=True, null=True)
    
    ano = models.IntegerField(null=True, blank=True)
    classificacao = models.IntegerField(null=True, blank=True)

    pdf = models.URLField(blank=True)
    imagem = models.ImageField(upload_to='tfc/', blank=True, null=True)

    #Relacões
    licenciatura = models.ForeignKey(Licenciatura,on_delete=models.SET_NULL,null=True, blank=True)
    autores = models.ManyToManyField(Utilizador, related_name='tfc_autores', blank=True)
    orientadores = models.ManyToManyField(Docente, blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, blank=True)
    areas = models.ManyToManyField('Area', blank=True)
    palavras_chave = models.ManyToManyField('PalavraChave', blank=True)

    #Como aparece no admin
    def __str__(self):
        return self.titulo
    
    
#Area
class Area(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


#Palavra chave
class PalavraChave(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


#Making off
class MakingOf(models.Model):
    descricao = models.TextField()
    data = models.DateField()
    imagem = models.ImageField(upload_to='makingof/',blank=True, null=True)
    decisoes = models.TextField()
    erros = models.TextField()
    correcoes = models.TextField()
    justificacao = models.TextField()
    uso_ia = models.TextField()

    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)

    def __str__(self):
        return f"MakingOf {self.id}"


