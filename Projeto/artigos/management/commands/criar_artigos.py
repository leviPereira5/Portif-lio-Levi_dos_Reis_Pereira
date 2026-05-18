from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from artigos.models import Artigo

ARTIGOS = [
    {
        'titulo': 'Python: A Linguagem que Mudou o Meu Percurso',
        'texto': (
            "Quando comecei a estudar programação, a primeira linguagem que verdadeiramente me apaixonou foi Python. "
            "A sua sintaxe limpa e legível permite focar no problema em si, sem ficar preso em detalhes de declarações "
            "de tipos ou gestão de memória.\n\n"
            "O que mais me surpreendeu foi a vastidão do ecossistema: desde análise de dados com Pandas e NumPy, "
            "a desenvolvimento web com Django e Flask, passando por machine learning com scikit-learn e TensorFlow. "
            "É praticamente impossível encontrar uma área da computação onde Python não tenha uma biblioteca sólida.\n\n"
            "Na universidade, Python tem sido o meu companheiro constante — em algoritmos, bases de dados, projetos web "
            "e até automação de tarefas repetitivas. A comunidade é enorme e os recursos de aprendizagem são excelentes. "
            "Se estás a começar, começa por Python. Não te vais arrepender."
        ),
        'link_externo': 'https://www.python.org',
    },
    {
        'titulo': 'Git e GitHub: Controlo de Versões que Todo o Programador Deve Dominar',
        'texto': (
            "Antes de aprender Git, eu guardava versões do meu código com nomes como 'projeto_final_v2_MESMO_FINAL.zip'. "
            "Quem nunca? Git resolveu esse problema de vez.\n\n"
            "Git é um sistema de controlo de versões distribuído que permite guardar o histórico completo de alterações "
            "de um projeto, colaborar com outros programadores sem conflitos, e voltar atrás no tempo sempre que "
            "algo corre mal. É como ter um 'Ctrl+Z' ilimitado, mas para projetos inteiros.\n\n"
            "GitHub é a plataforma online que complementa o Git, permitindo hospedar repositórios, colaborar em "
            "projetos open source, e mostrar o teu trabalho ao mundo. O teu perfil GitHub é hoje o teu portfólio "
            "mais importante como programador.\n\n"
            "Conceitos essenciais: commits, branches, merges, pull requests. Domina estes e estarás pronto para "
            "trabalhar em qualquer equipa profissional."
        ),
        'link_externo': 'https://github.com',
    },
    {
        'titulo': 'Bases de Dados Relacionais: Por Que SQL Ainda Domina em 2026',
        'texto': (
            "Com toda a hype em torno de bases de dados NoSQL, grafos e documentos, podia pensar-se que SQL "
            "estava ultrapassado. A realidade é bem diferente: SQL continua a ser a competência mais pedida em "
            "ofertas de emprego para programadores, e por boas razões.\n\n"
            "Bases de dados relacionais como PostgreSQL, MySQL e SQLite assentam em décadas de investigação em "
            "teoria de conjuntos e álgebra relacional. Garantem propriedades ACID (Atomicidade, Consistência, "
            "Isolamento, Durabilidade) que são críticas em aplicações onde os dados não podem ser perdidos "
            "nem corrompidos — bancos, hospitais, e-commerce.\n\n"
            "Neste portfólio, uso PostgreSQL (via Neon) para guardar todos os dados. A ORM do Django abstrai "
            "muito do SQL, mas entender o que acontece por baixo faz toda a diferença quando precisas de "
            "otimizar queries lentas ou modelar relações complexas.\n\n"
            "O meu conselho: aprende SQL puro antes de usar qualquer ORM. Vai tornar-te um programador "
            "muito mais capaz."
        ),
        'link_externo': 'https://neon.tech',
    },
]


class Command(BaseCommand):
    help = 'Cria 3 artigos de exemplo e configura o grupo bloggers'

    def handle(self, *args, **options):
        grupo, _ = Group.objects.get_or_create(name='bloggers')

        autor = User.objects.filter(is_superuser=True).first()
        if not autor:
            autor = User.objects.first()
        if not autor:
            autor = User.objects.create_superuser('admin', 'admin@portfolio.pt', 'admin1234')
            self.stdout.write('Superutilizador admin criado.')

        autor.groups.add(grupo)

        criados = 0
        for dados in ARTIGOS:
            if not Artigo.objects.filter(titulo=dados['titulo']).exists():
                Artigo.objects.create(autor=autor, **dados)
                criados += 1
                self.stdout.write(f'  + Artigo criado: {dados["titulo"]}')

        if criados == 0:
            self.stdout.write('Os artigos já existem, nada foi criado.')
        else:
            self.stdout.write(self.style.SUCCESS(f'{criados} artigo(s) criado(s) com sucesso.'))
