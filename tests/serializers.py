from vvmodel.serializers import SerializedObject


class SerializedMiTestModel(SerializedObject):
    @classmethod
    def model_string(cls):
        return "tests.mitestmodel"


class SerializedMiTestPolymorphModel(SerializedObject):

    @classmethod
    def model_string(cls):
        return "tests.mitestpolymorphmodel"


class SerializedMiTestPolymorphSubSubModel(SerializedObject):

    @classmethod
    def model_string(cls):
        return "tests.mitestpolymorphsubsubmodel"
