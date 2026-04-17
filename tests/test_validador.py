"""Testes para territorialguard.validador."""

from territorialguard.validador import parsear_municipio


def test_parsear_municipio_formato_padrao():
    cidade, uf = parsear_municipio("Andradina - SP")
    assert cidade == "Andradina"
    assert uf == "SP"


def test_parsear_municipio_sem_separador():
    cidade, uf = parsear_municipio("Brasilia")
    assert cidade == "Brasilia"
    assert uf == ""


def test_parsear_municipio_com_hifen_no_nome():
    cidade, uf = parsear_municipio("Caldas Novas - GO")
    assert cidade == "Caldas Novas"
    assert uf == "GO"


def test_parsear_municipio_remove_whitespace():
    cidade, uf = parsear_municipio("  Rio  -  RJ  ")
    assert cidade == "Rio"
    assert uf == "RJ"
