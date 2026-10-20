"""Consulta de dúvidas.

  1. FUNÇÕES COMPARTILHADAS
  2. PARTE DO MONITOR   -> recebe as dúvidas e marca atendimento em grupo
  3. PARTE DO PROFESSOR -> só vê quais dúvidas mais se repetem
"""

from collections import Counter

from acesso import exigir_tipo
from monitoria import Monitor, Professor



# FUNÇÕES COMPARTILHADAS

def normalizar_duvida(texto):
    """Ignora maiúsculas e espaços a mais ("Regra  da Cadeia" == "regra da cadeia")."""
    return " ".join(texto.lower().split())


def duvidas_do_monitor(monitor):
    """Horários do monitor que têm aluno e dúvida."""
    return [h for h in monitor.disponibilidades if h.aluno and h.duvida]



# PARTE DO MONITOR

def consultar_duvidas_monitor(usuario):
    """Dúvidas dos alunos do monitor. Só o próprio monitor acessa."""
    exigir_tipo(usuario, Monitor)
    return duvidas_do_monitor(usuario)


def duvidas_repetidas(usuario):
    """Dúvidas que mais de um aluno tem: {dúvida normalizada: [horários]}."""
    grupos = {}
    for horario in consultar_duvidas_monitor(usuario):
        grupos.setdefault(normalizar_duvida(horario.duvida), []).append(horario)
    return {d: hs for d, hs in grupos.items() if len(hs) > 1}


def marcar_em_grupo(usuario, duvida):
    """O monitor decide marcar como atendimento em grupo uma dúvida repetida.

    Só funciona se mais de um aluno tiver essa dúvida; senão, lança ValueError.
    Devolve os horários marcados como em grupo.
    """
    horarios = duvidas_repetidas(usuario).get(normalizar_duvida(duvida))
    if not horarios:
        raise ValueError("Não há mais de um aluno com essa dúvida.")
    for horario in horarios:
        horario.em_grupo = True
    return horarios


# PARTE DO PROFESSOR

def ranking_duvidas(usuario, monitores):
    """Dúvidas da disciplina do professor, da mais para a menos frequente.

    Devolve lista de (dúvida, quantidade). Sem monitorias, lista vazia.
    """
    exigir_tipo(usuario, Professor)
    contagem = Counter()
    for monitor in monitores:
        if monitor.disciplina == usuario.disciplina:
            for horario in duvidas_do_monitor(monitor):
                contagem[normalizar_duvida(horario.duvida)] += 1
    return contagem.most_common()