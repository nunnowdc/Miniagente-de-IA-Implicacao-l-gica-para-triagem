"""
Agente de IA para Triagem de Pacientes
========================================
Sistema baseado em lógica proposicional: 6 proposições (fatos observáveis)
combinadas por regras lógicas (SE ... ENTÃO ...) que determinam o nível
de urgência do atendimento, inspirado no Protocolo de Manchester.

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

Regras:
    a (Emergência)      : (p ^ q) v r v s
    b (Muito urgente)   : ~a ^ (q v (p ^ u))
    c (Urgente)         : ~a ^ ~b ^ (u v t)
    d (Pouco urgente)   : qualquer proposição verdadeira que não caiu nos casos anteriores
    e (Não urgente)     : nenhuma proposição verdadeira

Autor: Nunno
"""

from dataclasses import dataclass, fields
from typing import Callable, List, Tuple


# ---------------------------------------------------------------------------
# 1. PROPOSIÇÕES
# ---------------------------------------------------------------------------
@dataclass
class Proposicoes:
    """Cada campo é uma proposição lógica (verdadeira ou falsa)."""
    p: bool   # dor no peito
    q: bool   # dificuldade respiratória
    r: bool   # hemorragia
    s: bool   # consciência alterada
    t: bool   # febre alta
    u: bool   # muita dor
    w: bool = False   # dor leve a moderada (EVA 3-6)
    x: bool = False   # tosse ou congestão nasal
    y: bool = False   # mal-estar geral / tontura leve


DESCRICOES = {
    "p": "Dor no peito",
    "q": "Dificuldade respiratória",
    "r": "Hemorragia",
    "s": "Consciência alterada",
    "t": "Febre alta (>= 39°C)",
    "u": "Muita dor (EVA >= 8/10)",
    "w": "Dor leve a moderada (EVA 3-6)",
    "x": "Tosse ou congestão nasal",
    "y": "Mal-estar geral / tontura leve",
}


# ---------------------------------------------------------------------------
# 2. REGRAS LÓGICAS (avaliadas em ordem de prioridade)
# ---------------------------------------------------------------------------
def regra_a_emergencia(props: Proposicoes) -> bool:
    # a: (p ^ q) v r v s
    return (props.p and props.q) or props.r or props.s


def regra_b_muito_urgente(props: Proposicoes) -> bool:
    # b: ~a ^ (q v (p ^ u))
    return props.q or (props.p and props.u)


def regra_c_urgente(props: Proposicoes) -> bool:
    # c: ~a ^ ~b ^ (u v t)
    return props.u or props.t


def regra_d_pouco_urgente(props: Proposicoes) -> bool:
    # d: qualquer proposição verdadeira que não caiu nas regras anteriores
    return any(getattr(props, f.name) for f in fields(props))


# Lista de regras em ordem de prioridade: (nível, cor, tempo alvo, função, explicação)
REGRAS: List[Tuple[str, str, str, Callable[[Proposicoes], bool], str]] = [
    ("EMERGÊNCIA (a)", "Vermelho", "imediato",
     regra_a_emergencia,
     "(p ^ q) v r v s -- dor no peito + dificuldade respiratória, ou hemorragia, ou consciência alterada"),
    ("MUITO URGENTE (b)", "Laranja", "até 10 min",
     regra_b_muito_urgente,
     "~a ^ (q v (p ^ u)) -- dificuldade respiratória isolada, ou dor no peito associada a muita dor"),
    ("URGENTE (c)", "Amarelo", "até 60 min",
     regra_c_urgente,
     "~a ^ ~b ^ (u v t) -- muita dor ou febre alta"),
    ("POUCO URGENTE (d)", "Verde", "até 120 min",
     regra_d_pouco_urgente,
     "Ao menos uma proposição verdadeira, sem critério de maior gravidade"),
]

NAO_URGENTE = ("NÃO URGENTE (e)", "Azul", "até 240 min", "Nenhuma proposição verdadeira")


# ---------------------------------------------------------------------------
# 3. MOTOR DE INFERÊNCIA
# ---------------------------------------------------------------------------
def classificar(props: Proposicoes):
    """Avalia as regras em ordem e retorna (nivel, cor, tempo_alvo, explicacao)."""
    for nivel, cor, tempo, regra, explicacao in REGRAS:
        if regra(props):
            return nivel, cor, tempo, explicacao
    nivel, cor, tempo, explicacao = NAO_URGENTE
    return nivel, cor, tempo, explicacao


def proposicoes_ativas(props: Proposicoes) -> List[str]:
    return [f"{f.name} ({DESCRICOES[f.name]})" for f in fields(props) if getattr(props, f.name)]


# ---------------------------------------------------------------------------
# 4. INTERFACE CLI
# ---------------------------------------------------------------------------
def perguntar(texto: str) -> bool:
    while True:
        resposta = input(f"{texto} (s/n): ").strip().lower()
        if resposta in ("s", "sim", "y", "yes"):
            return True
        if resposta in ("n", "nao", "não", "no"):
            return False
        print("  Resposta inválida. Digite 's' ou 'n'.")


def executar_cli():
    print("=" * 60)
    print(" AGENTE DE TRIAGEM - Sistema Baseado em Lógica Proposicional")
    print("=" * 60)

    respostas = {}
    for f in fields(Proposicoes):
        respostas[f.name] = perguntar(f"{f.name} - {DESCRICOES[f.name]}")

    props = Proposicoes(**respostas)
    nivel, cor, tempo, explicacao = classificar(props)

    print("\n" + "-" * 60)
    print("RESULTADO DA TRIAGEM")
    print("-" * 60)
    ativas = proposicoes_ativas(props)
    print(f"Proposições ativas: {', '.join(ativas) if ativas else 'nenhuma'}")
    print(f"Classificação: {nivel} ({cor})")
    print(f"Tempo alvo de atendimento: {tempo}")
    print(f"Justificativa: {explicacao}")
    print("-" * 60)


if __name__ == "__main__":
    executar_cli()
