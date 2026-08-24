"""
Suíte de testes / validação de acertividade do Agente de Triagem
===================================================================
Cada caso de teste define os valores das 6 proposições (p, q, r, s, t, u)
e o nível de urgência ESPERADO (gabarito). O script roda o agente para
cada caso, compara com o esperado e calcula a acertividade (accuracy) geral.

Proposições:
    p - dor no peito
    q - dificuldade respiratória
    r - hemorragia
    s - consciência alterada
    t - febre alta
    u - muita dor
    w - dor leve a moderada (EVA 3-6)
    x - tosse ou congestão nasal
    y - mal-estar geral / tontura leve

Rode com: python test_triage.py
"""

from triage_agent import Proposicoes, classificar


# ---------------------------------------------------------------------------
# CASOS DE TESTE: (descrição, proposições [p,q,r,s,t,u], nível esperado)
# ---------------------------------------------------------------------------
CASOS = [
    ("Nenhum sintoma",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False),
     "NÃO URGENTE (e)"),

    ("Somente dor no peito (p isolado)",
     Proposicoes(p=True, q=False, r=False, s=False, t=False, u=False),
     "POUCO URGENTE (d)"),

    ("Somente dificuldade respiratória (q isolado)",
     Proposicoes(p=False, q=True, r=False, s=False, t=False, u=False),
     "MUITO URGENTE (b)"),

    ("Somente hemorragia (r isolado)",
     Proposicoes(p=False, q=False, r=True, s=False, t=False, u=False),
     "EMERGÊNCIA (a)"),

    ("Somente consciência alterada (s isolado)",
     Proposicoes(p=False, q=False, r=False, s=True, t=False, u=False),
     "EMERGÊNCIA (a)"),

    ("Somente febre alta (t isolado)",
     Proposicoes(p=False, q=False, r=False, s=False, t=True, u=False),
     "URGENTE (c)"),

    ("Somente muita dor (u isolado)",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=True),
     "URGENTE (c)"),

    ("p ^ q -- dor no peito + dificuldade respiratória",
     Proposicoes(p=True, q=True, r=False, s=False, t=False, u=False),
     "EMERGÊNCIA (a)"),

    ("p ^ u -- dor no peito + muita dor (sem dificuldade respiratória)",
     Proposicoes(p=True, q=False, r=False, s=False, t=False, u=True),
     "MUITO URGENTE (b)"),

    ("p ^ t -- dor no peito + febre alta (sem muita dor)",
     Proposicoes(p=True, q=False, r=False, s=False, t=True, u=False),
     "URGENTE (c)"),

    ("q ^ s -- dificuldade respiratória + consciência alterada",
     Proposicoes(p=False, q=True, r=False, s=True, t=False, u=False),
     "EMERGÊNCIA (a)"),

    ("t ^ u -- febre alta + muita dor",
     Proposicoes(p=False, q=False, r=False, s=False, t=True, u=True),
     "URGENTE (c)"),

    ("p ^ r -- dor no peito + hemorragia",
     Proposicoes(p=True, q=False, r=True, s=False, t=False, u=False),
     "EMERGÊNCIA (a)"),

    ("Todas as proposições verdadeiras",
     Proposicoes(p=True, q=True, r=True, s=True, t=True, u=True),
     "EMERGÊNCIA (a)"),

    ("r ^ u -- hemorragia + muita dor (checa prioridade de a sobre c)",
     Proposicoes(p=False, q=False, r=True, s=False, t=False, u=True),
     "EMERGÊNCIA (a)"),

    ("s ^ t -- consciência alterada + febre alta (checa prioridade de a sobre c)",
     Proposicoes(p=False, q=False, r=False, s=True, t=True, u=False),
     "EMERGÊNCIA (a)"),

    ("q ^ t -- dificuldade respiratória + febre alta (checa prioridade de b sobre c)",
     Proposicoes(p=False, q=True, r=False, s=False, t=True, u=False),
     "MUITO URGENTE (b)"),

    ("p isolado, sem t e sem u (checa não regressão)",
     Proposicoes(p=True, q=False, r=False, s=False, t=False, u=False),
     "POUCO URGENTE (d)"),

    ("Somente dor leve a moderada (w isolado)",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False, w=True),
     "POUCO URGENTE (d)"),

    ("Somente tosse ou congestão nasal (x isolado)",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False, x=True),
     "POUCO URGENTE (d)"),

    ("Somente mal-estar geral / tontura leve (y isolado)",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False, y=True),
     "POUCO URGENTE (d)"),

    ("w ^ x -- dor leve + tosse (combinação de sintomas leves)",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False, w=True, x=True),
     "POUCO URGENTE (d)"),

    ("w ^ x ^ y -- todos os sintomas leves juntos",
     Proposicoes(p=False, q=False, r=False, s=False, t=False, u=False, w=True, x=True, y=True),
     "POUCO URGENTE (d)"),

    ("w ^ t -- dor leve + febre alta (checa prioridade de c sobre d)",
     Proposicoes(p=False, q=False, r=False, s=False, t=True, u=False, w=True),
     "URGENTE (c)"),

    ("x ^ s -- tosse + consciência alterada (checa prioridade de a sobre d)",
     Proposicoes(p=False, q=False, r=False, s=True, t=False, u=False, x=True),
     "EMERGÊNCIA (a)"),
]


def rodar_testes(verbose: bool = True):
    total = len(CASOS)
    acertos = 0
    falhas = []

    for descricao, props, esperado in CASOS:
        nivel, cor, tempo, explicacao = classificar(props)
        correto = (nivel == esperado)
        acertos += int(correto)

        if verbose:
            status = "OK " if correto else "FALHOU"
            print(f"[{status}] {descricao}")
            print(f"        esperado: {esperado} | obtido: {nivel}")
            if not correto:
                print(f"        (explicação do agente: {explicacao})")

        if not correto:
            falhas.append((descricao, esperado, nivel))

    acertividade = (acertos / total) * 100

    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {acertos}/{total} corretos")
    print(f"ACERTIVIDADE: {acertividade:.1f}%")
    print("=" * 60)

    if falhas:
        print("\nCasos com divergência:")
        for descricao, esperado, obtido in falhas:
            print(f" - {descricao}: esperado='{esperado}', obtido='{obtido}'")

    return acertividade


if __name__ == "__main__":
    rodar_testes()
