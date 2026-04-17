"""Testes para territorialguard.linhagem."""

from territorialguard.linhagem import classificar_upstream


def test_classificar_upstream_sem_linhagem():
    status, _ = classificar_upstream(0, 0, [])
    assert status == "SEM_LINHAGEM"


def test_classificar_upstream_zero_confirmado():
    upstream = [{"fonte": "fonte_a", "registros": 0}]
    status, _ = classificar_upstream(0, 0, upstream)
    assert status == "ZERO_CONFIRMADO_FONTE"


def test_classificar_upstream_perdeu_no_painel():
    upstream = [{"fonte": "fonte_b", "registros": 150}]
    status, mensagem = classificar_upstream(0, 0, upstream)
    assert status == "PERDEU_NO_PAINEL"
    assert "fonte_b" in mensagem


def test_classificar_upstream_valor_zerado():
    upstream = [{"fonte": "fonte_c", "registros": 10}]
    status, _ = classificar_upstream(5, 0, upstream)
    assert status == "VALOR_ZERADO_NO_PAINEL"


def test_classificar_upstream_ok():
    upstream = [{"fonte": "fonte_d", "registros": 20}]
    status, _ = classificar_upstream(5, 100, upstream)
    assert status == "OK_CONFIRMADO_FONTE"


def test_classificar_upstream_erro():
    upstream = [{"fonte": "fonte_e", "registros": None, "erro": "timeout"}]
    status, mensagem = classificar_upstream(0, 0, upstream)
    assert status == "UPSTREAM_ERRO"
    assert "timeout" in mensagem
