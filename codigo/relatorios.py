"""Relatório mensal de horas atendidas (acesso exclusivo da coordenação)."""

from acesso import exigir_tipo
from monitoria import Coordenacao


def mes_do_horario(horario):
    """Pega o mês de uma data no formato "19/10 14:00"."""
    data = horario.data_hora.split()[0]  # "19/10"
    return int(data.split("/")[1])       # 10


def horas_atendidas(monitor, mes):
    """Total de horas que o monitor atendeu no mês (0 se não teve nenhuma)."""
    minutos = 0
    for horario in monitor.disponibilidades:
        if horario.aluno is not None and mes_do_horario(horario) == mes:
            minutos += horario.duracao_minutos
    return minutos / 60


def gerar_relatorio_horas(usuario, monitores, mes):
    """Devolve {nome do monitor: horas atendidas no mês}. Só a coordenação acessa."""
    exigir_tipo(usuario, Coordenacao)
    return {monitor.nome: horas_atendidas(monitor, mes) for monitor in monitores}