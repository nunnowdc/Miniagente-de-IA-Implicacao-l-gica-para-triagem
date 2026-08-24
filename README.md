# Agente de triagem — lógica proposicional

Agente de IA para triagem de pacientes baseado em **lógica proposicional**: um conjunto de proposições (fatos observáveis sobre o paciente) combinadas por regras lógicas de decisão (`SE ... ENTÃO ...`), inspirado no Protocolo de Manchester. O projeto inclui o motor de decisão, uma interface web interativa e uma suíte de testes para validar a acertividade das classificações.

## Proposições

| Letra | Proposição |
|---|---|
| `p` | Dor no peito |
| `q` | Dificuldade respiratória |
| `r` | Hemorragia |
| `s` | Consciência alterada |
| `t` | Febre alta (≥ 39°C) |
| `u` | Muita dor (EVA ≥ 8/10) |
| `w` | Dor leve a moderada (EVA 3-6) |
| `x` | Tosse ou congestão nasal |
| `y` | Mal-estar geral / tontura leve |

## Regras de decisão

As regras são avaliadas em ordem de prioridade — a primeira que for verdadeira define a classificação:

| Regra | Nível | Expressão lógica |
|---|---|---|
| `a` | Emergência | `(p ∧ q) ∨ r ∨ s` |
| `b` | Muito urgente | `¬a ∧ (q ∨ (p ∧ u))` |
| `c` | Urgente | `¬a ∧ ¬b ∧ (u ∨ t)` |
| `d` | Pouco urgente | `¬a ∧ ¬b ∧ ¬c ∧` qualquer proposição verdadeira |
| `e` | Não urgente | nenhuma proposição verdadeira |

## Arquivos

- **`triage_agent.py`** — motor de inferência + interface de linha de comando (CLI) interativa
- **`test_triage.py`** — suíte de testes com 25 casos rotulados, calcula a acertividade do agente
- **`triage_web.html`** — interface web interativa: alterna as proposições e acompanha ao vivo qual regra dispara, com uma aba de testes embutida

## Como rodar

### Interface web
Basta abrir `triage_web.html` no navegador (duplo clique) — não precisa de instalação nem servidor.

### CLI (Python 3.8+)
```bash
python3 triage_agent.py
```

### Testes
```bash
python3 test_triage.py
```

## Status atual

25/25 casos de teste corretos (100% de acertividade).
