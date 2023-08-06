'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._943 import HypoidGearDesign
    from ._944 import HypoidGearMeshDesign
    from ._945 import HypoidGearSetDesign
    from ._946 import HypoidMeshedGearDesign
