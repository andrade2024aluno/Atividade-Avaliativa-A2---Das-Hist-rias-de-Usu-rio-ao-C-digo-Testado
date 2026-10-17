import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from monitoria import (
    Aluno,
    AlunoBloqueadoError,
    HorarioOcupadoError,
    Monitor,
    listar_horarios_disponiveis,
)


class TestMarcarMonitoria(unittest.TestCase):

    def setUp(self):
        self.monitor_calculo = Monitor("Marcos", "Cálculo")
        self.monitor_poo = Monitor("Julia", "POO")

        self.horario_calc_1 = self.monitor_calculo.adicionar_disponibilidade("19/10 14:00")
        self.horario_calc_2 = self.monitor_calculo.adicionar_disponibilidade("19/10 14:30")
        self.horario_poo_1 = self.monitor_poo.adicionar_disponibilidade("20/10 10:00")

        self.monitores = [self.monitor_calculo, self.monitor_poo]
        self.aluno = Aluno("Pedro")

    def test_lista_somente_horarios_livres_da_disciplina(self):
        outro_aluno = Aluno("Mariana")
        outro_aluno.marcar_monitoria(self.horario_calc_1, "Limites laterais")

        disponiveis = listar_horarios_disponiveis(self.monitores, "Cálculo")

        self.assertEqual(len(disponiveis), 1)
        self.assertIn(self.horario_calc_2, disponiveis)
        self.assertNotIn(self.horario_calc_1, disponiveis)
        self.assertNotIn(self.horario_poo_1, disponiveis)

    def test_marcacao_salva_a_duvida(self):
        duvida = "Como aplicar polimorfismo e herança"
        self.aluno.marcar_monitoria(self.horario_poo_1, duvida)

        self.assertEqual(self.horario_poo_1.aluno, self.aluno)
        self.assertEqual(self.horario_poo_1.duvida, duvida)

    def test_horario_marcado_nao_aparece_na_lista(self):
        self.aluno.marcar_monitoria(self.horario_calc_1, "Integrais por partes")

        disponiveis = listar_horarios_disponiveis(self.monitores, "Cálculo")

        self.assertFalse(self.horario_calc_1.esta_disponivel())
        self.assertNotIn(self.horario_calc_1, disponiveis)
        self.assertIn(self.horario_calc_2, disponiveis)

    def test_marcar_horario_ocupado_lanca_excecao(self):
        aluno_1 = Aluno("Beatriz")
        aluno_2 = Aluno("Rafael")

        aluno_1.marcar_monitoria(self.horario_calc_1, "Derivadas implícitas")

        with self.assertRaises(HorarioOcupadoError):
            aluno_2.marcar_monitoria(self.horario_calc_1, "Taxa de variação")

    def test_aluno_bloqueado_nao_marca(self):
        aluno_bloqueado = Aluno("Carlos", bloqueado=True)

        with self.assertRaises(AlunoBloqueadoError):
            aluno_bloqueado.marcar_monitoria(self.horario_calc_2, "Séries e sequências")

        self.assertTrue(self.horario_calc_2.esta_disponivel())


if __name__ == "__main__":
    unittest.main()