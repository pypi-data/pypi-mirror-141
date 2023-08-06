'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1244 import KeywayHalfRating
    from ._1245 import KeywayRating
