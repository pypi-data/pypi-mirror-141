'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1240 import KeyedJointDesign
    from ._1241 import KeyTypes
    from ._1242 import KeywayJointHalfDesign
    from ._1243 import NumberOfKeys
