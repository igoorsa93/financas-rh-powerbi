"""
Gera dados ficticios consistentes para o projeto demo (RH + Financas).
Nao usa nomes de pessoas reais/famosas - apenas combinacoes comuns de nomes
brasileiros genericos.
"""
import random
import json
from datetime import date, timedelta

random.seed(42)

PRIMEIROS_M = [
    "Joao", "Carlos", "Marcos", "Paulo", "Antonio", "Jose", "Francisco",
    "Ricardo", "Eduardo", "Rafael", "Rodrigo", "Fernando", "Gustavo",
    "Bruno", "Diego", "Felipe", "Leandro", "Marcelo", "Anderson", "Vinicius",
    "Alexandre", "Renato", "Sergio", "Wagner", "Cleber", "Adriano",
]
PRIMEIROS_F = [
    "Maria", "Ana", "Francisca", "Antonia", "Adriana", "Juliana", "Marcia",
    "Fernanda", "Patricia", "Aline", "Sandra", "Camila", "Amanda", "Bruna",
    "Jessica", "Leticia", "Vanessa", "Simone", "Renata", "Tatiane",
    "Cristina", "Rosangela", "Luciana", "Priscila", "Debora",
]
MEIOS = [
    "da Silva", "dos Santos", "de Oliveira", "Souza", "Rodrigues", "Ferreira",
    "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins",
    "Carvalho", "Almeida", "Barbosa", "Araujo", "Nascimento", "Cardoso",
    "Correia", "Teixeira", "Fernandes", "Moreira", "Cavalcante", "Nunes",
]
SOBRENOMES = [
    "Xavier", "Reis", "Junior", "Neto", "Filho", "Pinto", "Rocha", "Dias",
    "Castro", "Freitas", "Mendes", "Vieira", "Monteiro", "Batista", "Sales",
    "Guimaraes", "Andrade", "Peixoto", "Bezerra", "Farias",
]

CARGOS = [
    "Analista Financeiro", "Assistente Financeiro", "Assistente Administrativo",
    "Auxiliar Administrativo", "Recepcionista", "Analista de RH",
    "Auxiliar de Producao", "Operador de Maquinas", "Pedreiro",
    "Servente de Obras", "Motorista", "Encarregado de Producao",
    "Supervisor de Producao", "Almoxarife", "Auxiliar de Almoxarifado",
    "Soldador", "Eletricista de Manutencao", "Mecanico de Manutencao",
    "Gerente Administrativo", "Coordenador Financeiro",
]

CARGO_FAIXA_SALARIAL = {
    "Analista Financeiro": (3200, 4800),
    "Assistente Financeiro": (2100, 2900),
    "Assistente Administrativo": (2000, 2800),
    "Auxiliar Administrativo": (1500, 2100),
    "Recepcionista": (1500, 1900),
    "Analista de RH": (3000, 4500),
    "Auxiliar de Producao": (1450, 1900),
    "Operador de Maquinas": (1800, 2600),
    "Pedreiro": (1700, 2400),
    "Servente de Obras": (1420, 1750),
    "Motorista": (1900, 2700),
    "Encarregado de Producao": (2800, 3800),
    "Supervisor de Producao": (3500, 5200),
    "Almoxarife": (1900, 2600),
    "Auxiliar de Almoxarifado": (1500, 1950),
    "Soldador": (2000, 3000),
    "Eletricista de Manutencao": (2400, 3400),
    "Mecanico de Manutencao": (2300, 3300),
    "Gerente Administrativo": (6500, 9500),
    "Coordenador Financeiro": (5500, 7800),
}

DEPARTAMENTOS = [
    "Administracao - Escritorio",
    "Administracao - Fabrica",
    "Apoio a Producao",
    "Operacional",
    "ACME_ADM DA FABRICA",
    "ACME_DP/RH",
    "ACME_OPERACIONAL_DIARIA",
    "ACME_PRODUCAO",
    "Pre-Moldados",
]

CARGO_POR_DEPARTAMENTO = {
    "Administracao - Escritorio": ["Analista Financeiro", "Assistente Financeiro", "Assistente Administrativo", "Recepcionista", "Analista de RH", "Coordenador Financeiro"],
    "Administracao - Fabrica": ["Assistente Administrativo", "Auxiliar Administrativo", "Almoxarife", "Auxiliar de Almoxarifado"],
    "Apoio a Producao": ["Auxiliar de Producao", "Servente de Obras", "Almoxarife"],
    "Operacional": ["Pedreiro", "Servente de Obras", "Operador de Maquinas", "Motorista"],
    "ACME_ADM DA FABRICA": ["Gerente Administrativo", "Assistente Administrativo", "Supervisor de Producao"],
    "ACME_DP/RH": ["Analista de RH", "Assistente Administrativo"],
    "ACME_OPERACIONAL_DIARIA": ["Servente de Obras", "Pedreiro", "Auxiliar de Producao"],
    "ACME_PRODUCAO": ["Operador de Maquinas", "Soldador", "Eletricista de Manutencao", "Mecanico de Manutencao", "Encarregado de Producao"],
    "Pre-Moldados": ["Operador de Maquinas", "Soldador", "Supervisor de Producao", "Auxiliar de Producao"],
}

CENTRO_CUSTO_POR_DEPARTAMENTO = {
    "Administracao - Escritorio": "Escritorio ACME",
    "Administracao - Fabrica": "Fabrica ACME",
    "Apoio a Producao": "Producao ACME",
    "Operacional": "Operacional ACME",
    "ACME_ADM DA FABRICA": "Fabrica ACME",
    "ACME_DP/RH": "DP/RH ACME",
    "ACME_OPERACIONAL_DIARIA": "Operacional ACME",
    "ACME_PRODUCAO": "Producao ACME",
    "Pre-Moldados": "Producao ACME",
}


def gerar_nome(sexo):
    primeiro = random.choice(PRIMEIROS_M if sexo == "Masculino" else PRIMEIROS_F)
    partes = [primeiro, random.choice(MEIOS), random.choice(SOBRENOMES)]
    if random.random() < 0.25:
        partes.append(random.choice(SOBRENOMES))
    return " ".join(partes).upper()


def data_aleatoria(inicio, fim):
    delta = (fim - inicio).days
    return inicio + timedelta(days=random.randint(0, delta))


def gerar_funcionarios(qtd=36):
    funcionarios = []
    codigos_usados = set()
    for i in range(qtd):
        codigo = random.randint(100, 299)
        while codigo in codigos_usados:
            codigo = random.randint(100, 299)
        codigos_usados.add(codigo)

        sexo = random.choice(["Masculino", "Feminino"])
        nome = gerar_nome(sexo)
        departamento = random.choice(DEPARTAMENTOS)
        cargo = random.choice(CARGO_POR_DEPARTAMENTO[departamento])
        faixa = CARGO_FAIXA_SALARIAL[cargo]
        salario = round(random.uniform(*faixa) / 5) * 5  # arredonda pra multiplo de 5
        admissao = data_aleatoria(date(2015, 1, 1), date(2026, 3, 1))
        nascimento = data_aleatoria(date(1965, 1, 1), date(2005, 12, 31))
        c_de_custo = CENTRO_CUSTO_POR_DEPARTAMENTO[departamento]

        funcionarios.append({
            "codigo": codigo,
            "nome": nome,
            "cargo": cargo,
            "admissao": admissao.isoformat(),
            "salario": salario,
            "servico": random.choice([1, 2]),
            "departamento": departamento,
            "c_de_custo": c_de_custo,
            "nascimento": nascimento.isoformat(),
            "sexo": sexo,
        })
    return funcionarios


if __name__ == "__main__":
    funcs = gerar_funcionarios(36)
    out_path = "C:/Users/igoor/Desktop/Controle Pessoal/github-demo/scripts/funcionarios_fake.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(funcs, f, ensure_ascii=False, indent=2)
    print(f"Gerados {len(funcs)} funcionarios ficticios em {out_path}")
