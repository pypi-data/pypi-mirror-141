'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._919 import StraightBevelDiffGearDesign
    from ._920 import StraightBevelDiffGearMeshDesign
    from ._921 import StraightBevelDiffGearSetDesign
    from ._922 import StraightBevelDiffMeshedGearDesign
