"""Testes para territorialguard.metricas."""

from territorialguard.metricas import METRICAS, INSTRUCOES_DASHBOARD


def test_metricas_e_lista_nao_vazia():
    assert isinstance(METRICAS, list)
    assert len(METRICAS) > 0


def test_cada_metrica_tem_campos_obrigatorios():
    obrigatorios = {"nome", "tabela", "expressao", "coluna_municipio"}
    for metrica in METRICAS:
        faltando = obrigatorios - set(metrica.keys())
        assert not faltando, f"Metrica {metrica.get('nome')} sem campos: {faltando}"


def test_instrucoes_dashboard_e_string():
    assert isinstance(INSTRUCOES_DASHBOARD, str)
    assert len(INSTRUCOES_DASHBOARD) > 0
