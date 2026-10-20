from datetime import datetime


class AlunoBloqueadoError(Exception):
    pass


class HorarioOcupadoError(Exception):
    pass


class CancelamentoForaDoPrazoError(Exception):
    pass


class Usuario:
    def __init__(self, nome):
        self.nome = nome


class Professor(Usuario):
    def __init__(self, nome, disciplina):
        super().__init__(nome)
        self.disciplina = disciplina


class Coordenacao(Usuario):
    pass


class Horario:
    def __init__(self, disciplina, monitor, data_hora):
        self.disciplina = disciplina
        self.monitor = monitor
        self.data_hora = data_hora
        self.duracao_minutos = 30
        self.aluno = None
        self.duvida = None
        self.em_grupo = False
        self.cancelado_pelo_monitor = False

    def esta_disponivel(self):
        return self.aluno is None and not self.cancelado_pelo_monitor


class Monitor(Usuario):
    def __init__(self, nome, disciplina):
        super().__init__(nome)
        self.disciplina = disciplina
        self.disponibilidades = []

    def adicionar_disponibilidade(self, data_hora):
        horario = Horario(self.disciplina, self, data_hora)
        self.disponibilidades.append(horario)
        return horario

    def horarios_disponiveis(self):
        livres = []
        for horario in self.disponibilidades:
            if horario.esta_disponivel():
                livres.append(horario)
        return livres

    def cancelar_horario(self, horario):
        if horario in self.disponibilidades:
            horario.cancelado_pelo_monitor = True
            horario.aluno = None
            horario.duvida = None


class Aluno(Usuario):
    def __init__(self, nome, bloqueado=False):
        super().__init__(nome)
        self.bloqueado = bloqueado
        self.faltas = 0

    def marcar_monitoria(self, horario, duvida):
        if self.bloqueado:
            raise AlunoBloqueadoError(f"O aluno {self.nome} esta bloqueado e não pode marcar monitoria")
        if not horario.esta_disponivel():
            raise HorarioOcupadoError(f"O horario {horario.data_hora} ja esta ocupado")

        horario.aluno = self
        horario.duvida = duvida
        return horario

    def cancelar_monitoria(self, horario, hora_atual):
        if horario.aluno != self:
            raise ValueError("Este horario não foi marcado por este aluno")

        dt_horario = datetime.strptime(f"{horario.data_hora}/2026", "%d/%m %H:%M/%Y")
        dt_atual = datetime.strptime(f"{hora_atual}/2026", "%d/%m %H:%M/%Y")

        diferenca_horas = (dt_horario - dt_atual).total_seconds() / 3600

        if diferenca_horas < 2:
            raise CancelamentoForaDoPrazoError("Cancelamento so e permitido com ate 2h de antecedencia")

        horario.aluno = None
        horario.duvida = None
        horario.em_grupo = False

    def registrar_falta(self):
        self.faltas += 1
        if self.faltas >= 2:
            self.bloqueado = True


def listar_horarios_disponiveis(monitores, disciplina):
    horarios_livres = []
    for monitor in monitores:
        if monitor.disciplina == disciplina:
            for h in monitor.horarios_disponiveis():
                horarios_livres.append(h)
    return horarios_livres


if __name__ == "__main__":
    monitor_calculo = Monitor("Marcio", "Calculo")
    monitor_poo = Monitor("Gabriel", "POO")

    h1 = monitor_calculo.adicionar_disponibilidade("19/10 14:00")
    h2 = monitor_calculo.adicionar_disponibilidade("19/10 14:30")
    h3 = monitor_poo.adicionar_disponibilidade("20/10 10:00")

    monitores = [monitor_calculo, monitor_poo]

    aluno = Aluno("Ana")
    disponiveis = listar_horarios_disponiveis(monitores, "Calculo")
    print(f"Horarios livres de Calculo antes da marcação: {len(disponiveis)}")

    aluno.marcar_monitoria(h1, "Duvida sobre regra da cadeia")
    print(f"Monitoria marcada por {h1.aluno.nome} as {h1.data_hora}")
    print(f"Duvida: {h1.duvida}")

    aluno.cancelar_monitoria(h1, "19/10 11:30")
    print("Monitoria cancelada com sucesso")
    
    disponiveis = listar_horarios_disponiveis(monitores, "Calculo")
    print(f"Horarios livres de Calculo depois do cancelamento: {len(disponiveis)}")