def test_devuelve_false_si_ningun_campo_del_objeto_en_memoria_es_distinto_en_su_version_persistente(miobjeto):
    assert miobjeto.any_field_changed() is False


def test_devuelve_true_si_algun_campo_del_objeto_en_memoria_es_distinto_en_su_version_persistente(miobjeto):
    miobjeto.nombre = 'ocjeto'
    assert miobjeto.any_field_changed() is True
