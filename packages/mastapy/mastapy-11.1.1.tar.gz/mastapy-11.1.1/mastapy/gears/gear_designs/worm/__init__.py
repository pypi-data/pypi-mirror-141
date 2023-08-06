'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._914 import WormDesign
    from ._915 import WormGearDesign
    from ._916 import WormGearMeshDesign
    from ._917 import WormGearSetDesign
    from ._918 import WormWheelDesign
