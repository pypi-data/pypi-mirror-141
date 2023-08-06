'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._910 import ZerolBevelGearDesign
    from ._911 import ZerolBevelGearMeshDesign
    from ._912 import ZerolBevelGearSetDesign
    from ._913 import ZerolBevelMeshedGearDesign
