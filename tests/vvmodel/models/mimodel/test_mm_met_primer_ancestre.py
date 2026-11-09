def test_devuelve_el_primer_ancestro_del_que_deriva_una_instancia_del_modelo(
        miobjetopolimorfico, misubsubobjetopolimorfico):
    assert misubsubobjetopolimorfico.primer_ancestre() == miobjetopolimorfico.get_class()


def test_devuelve_el_modelo_de_la_instancia_si_no_tiene_ancestros(miobjetopolimorfico):
    assert miobjetopolimorfico.primer_ancestre() == miobjetopolimorfico.get_class()
