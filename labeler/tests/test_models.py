from django.test import TestCase

from model_mommy.mommy import generators, make
from django.contrib.auth.models import User
from labeler.models import Trabalho


# Adiciona Field nao suportado pela biblioteca model_mommy
generators.add('yamlfield.fields.YAMLField', lambda: None)


class Completude(TestCase):
    def test_completude_geral_da_campanha_uma_resposta(self):
        """
            Calcula o volume de tarefas ja respondidas por todos os usuarios.
        """
        campanha = make('labeler.Campanha')
        tarefas = make('labeler.Tarefa', _quantity=10, campanha=campanha)
        trabalhos = make('labeler.Trabalho', _quantity=5, tarefas=tarefas)

        # Uma Resposta
        make('labeler.Resposta', tarefa=tarefas[0], trabalho=trabalhos[0])

        completude_geral = campanha.obter_completude_geral()

        self.assertEqual(completude_geral, 10)

    def test_completude_geral_da_campanha_multiplas_respostas(self):
        """
            Calcula o volume de tarefas ja respondidas por todos os usuarios.
        """
        campanha = make('labeler.Campanha')
        tarefas = make('labeler.Tarefa', _quantity=10, campanha=campanha)
        trabalhos = make('labeler.Trabalho', _quantity=5, tarefas=tarefas)

        # Tres Respostas
        make('labeler.Resposta', tarefa=tarefas[0], trabalho=trabalhos[0])
        make('labeler.Resposta', tarefa=tarefas[1], trabalho=trabalhos[1])
        make('labeler.Resposta', tarefa=tarefas[2], trabalho=trabalhos[2])

        completude_geral = campanha.obter_completude_geral()

        self.assertEqual(completude_geral, 30)

    def test_completude_geral_da_com_duas_respostas_para_mesma_tarefa(self):
        campanha = make('labeler.Campanha')
        tarefas = make('labeler.Tarefa', _quantity=10, campanha=campanha)
        trabalhos = make('labeler.Trabalho', _quantity=5, tarefas=tarefas)

        # Duas Respostas na mesma Tarefa
        make('labeler.Resposta', tarefa=tarefas[0], trabalho=trabalhos[0])
        make('labeler.Resposta', tarefa=tarefas[0], trabalho=trabalhos[1])

        completude_geral = campanha.obter_completude_geral()

        self.assertEqual(completude_geral, 10)

    def test_completude_geral_da_com_duas_casas_decimais(self):
        campanha = make('labeler.Campanha')
        tarefas = make('labeler.Tarefa', _quantity=3, campanha=campanha)
        trabalhos = make('labeler.Trabalho', _quantity=5, tarefas=tarefas)

        # Duas Respostas
        make('labeler.Resposta', tarefa=tarefas[0], trabalho=trabalhos[0])
        make('labeler.Resposta', tarefa=tarefas[1], trabalho=trabalhos[1])

        completude_geral = campanha.obter_completude_geral()

        self.assertEqual(completude_geral, 66.67)


class AlocacaoTarefa(TestCase):
    def setUp(self):
        self.usuario = make(
            User,
            username='usuarioteste')

    def test_obtencao_quantidade_tarefas(self):
        campanha = make(
            'labeler.Campanha',
            nome='Nova Campanha',
            tarefas_por_trabalho=2)
        make('labeler.Tarefa', _quantity=4, campanha=campanha)

        tarefas = campanha.obter_tarefa(self.usuario.username)

        self.assertIsNotNone(tarefas)
        self.assertTrue(hasattr(tarefas, 'numero_documento'))
        self.assertEqual(
            len(Trabalho.objects.filter(
                username=self.usuario.username)),
            1)
        self.assertEqual(
            len(Trabalho.objects.filter(
                username=self.usuario.username).first().tarefas.all()),
            2)

    def test_obter_tarefas_alocaveis(self):
        campanha = make(
            'labeler.Campanha',
            nome='Nova Campanha',
            tarefas_por_trabalho=2)
        make('labeler.Tarefa', _quantity=4, campanha=campanha)

        tarefas = campanha._obter_tarefas_alocaveis()

        self.assertEqual(len(tarefas), 2)
