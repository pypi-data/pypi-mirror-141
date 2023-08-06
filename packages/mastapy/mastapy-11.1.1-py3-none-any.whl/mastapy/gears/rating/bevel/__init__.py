'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._515 import BevelGearMeshRating
    from ._516 import BevelGearRating
    from ._517 import BevelGearSetRating
