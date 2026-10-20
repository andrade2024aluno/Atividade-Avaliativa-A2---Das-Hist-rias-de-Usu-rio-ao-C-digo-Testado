from monitoria import Coordenacao


def mes_do_horario(horario):
    data = horario.data_hora.split()[0]
    mes = data.split("/")[1]
    return int(mes)


def horas_atendidas(monitor, mes):
    minutos = 0
    for horario in monitor.disponibilidades:
        if horario.aluno is not None and mes_do_horario(horario) == mes:
            minutos += horario.duracao_minutos
    return minutos / 60


def gerar_relatorio_horas(usuario, monitores, mes):
    relatorio = {}
    for monitor in monitores:
        relatorio[monitor.nome] = horas_atendidas(monitor, mes)
    return relatorio