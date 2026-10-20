from monitoria import Monitor, Professor

#tira os espaços e palavras em maisculo e junta elas pra falitar a leitura
def normalizar_duvida(texto):
    palavras = texto.lower().split()
    return " ".join(palavras)

#lista as horas q o monitor pode e tem alunos pra fazer monitoria 
def duvidas_do_monitor(monitor):
    lista = []
    for h in monitor.disponibilidades:
        if h.aluno is not None and h.duvida is not None:
            lista.append(h)
    return lista

#ajunta todas as duvidas dos alunos
def duvidas_repetidas(usuario):
    grupos = {}
    for horario in duvidas_do_monitor(usuario):
        chave = normalizar_duvida(horario.duvida)
        if chave not in grupos:
            grupos[chave] = []
        grupos[chave].append(horario)

    repetidas = {}
    for d, hs in grupos.items():
        if len(hs) > 1:
            repetidas[d] = hs
    return repetidas

#procura duvidas iguais se nao tiver manda erro 
def marcar_em_grupo(usuario, duvida):
    repetidas = duvidas_repetidas(usuario)
    chave = normalizar_duvida(duvida)

    if chave not in repetidas:
        raise ValueError("Não ha mais de um aluno com essa duvida")

    horarios = repetidas[chave]
    for horario in horarios:
        horario.em_grupo = True
    return horarios

