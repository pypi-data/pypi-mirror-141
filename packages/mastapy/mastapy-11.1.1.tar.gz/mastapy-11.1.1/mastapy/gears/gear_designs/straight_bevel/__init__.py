'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._923 import StraightBevelGearDesign
    from ._924 import StraightBevelGearMeshDesign
    from ._925 import StraightBevelGearSetDesign
    from ._926 import StraightBevelMeshedGearDesign
