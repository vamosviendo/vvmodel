from vvmodel.cleaners import Cleaner


class MiTestCleaner(Cleaner):
    def metodo_uno(self):
        print("método 1")

    def metodo_dos(self):
        print("metodo 2")

    def _metodo_protegido(self):
        print("metodo protegido")


class OtroTestCleaner(Cleaner):
    def metodo_uno(self):
        print("método 1 de otro test cleaner")
