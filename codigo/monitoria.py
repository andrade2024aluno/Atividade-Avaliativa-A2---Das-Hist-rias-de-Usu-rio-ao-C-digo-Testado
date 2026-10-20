class AlunoBloqueadoError(Exception):
    """Exceção lançada quando um aluno bloqueado tenta marcar monitoria."""
    pass


class HorarioOcupadoError(Exception):
    """Exceção lançada quando se tenta marcar um horário já reservado."""
    pass


class Usuario:
    def __init__(self, nome):
        self.nome = nome


class Professor(Usuario):
    """Professor de uma disciplina, usado na verificação de dúvidas."""

    def __init__(self, nome, disciplina):
        super().__init__(nome)
        self.disciplina = disciplina

class Coordenacao(Usuario):
    """Esqueleto para futura geração do relatório mensal de horas."""
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

    def esta_disponivel(self):
        return self.aluno is None


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


class Aluno(Usuario):
    def __init__(self, nome, bloqueado=False):
        super().__init__(nome)
        self.bloqueado = bloqueado

    def marcar_monitoria(self, horario, duvida):
        if self.bloqueado:
            raise AlunoBloqueadoError(
                f"O aluno {self.nome} está bloqueado e não pode marcar monitoria."
            )
        if not horario.esta_disponivel():
            raise HorarioOcupadoError(
                f"O horário {horario.data_hora} já está ocupado."
            )

        horario.aluno = self
        horario.duvida = duvida
        return horario


def listar_horarios_disponiveis(monitores, disciplina):
    horarios_livres = []
    for monitor in monitores:
        if monitor.disciplina == disciplina:
            horarios_livres.extend(monitor.horarios_disponiveis())
    return horarios_livres

if __name__ == "__main__":
    monitor_calculo = Monitor("Vinicius", "Cálculo")
    monitor_poo = Monitor("Lucas", "POO")

    h1 = monitor_calculo.adicionar_disponibilidade("19/10 14:00")
    h2 = monitor_calculo.adicionar_disponibilidade("19/10 14:30")
    h3 = monitor_poo.adicionar_disponibilidade("20/10 10:00")

    monitores = [monitor_calculo, monitor_poo]

    aluno = Aluno("Ana")
    disponiveis_calculo = listar_horarios_disponiveis(monitores, "Cálculo")
    print(f"Horários livres de Cálculo antes da marcação: {len(disponiveis_calculo)}")

    aluno.marcar_monitoria(h1, "Dúvida sobre regra da cadeia")
    print(f"Monitoria marcada por {h1.aluno.nome} no horário {h1.data_hora}")
    print(f"Dúvida registrada: {h1.duvida}\n")

    disponiveis_calculo = listar_horarios_disponiveis(monitores, "Cálculo")
    print(f"Horários livres de Cálculo após a marcação: {len(disponiveis_calculo)}")