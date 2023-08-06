'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._939 import KlingelnbergConicalGearDesign
    from ._940 import KlingelnbergConicalGearMeshDesign
    from ._941 import KlingelnbergConicalGearSetDesign
    from ._942 import KlingelnbergConicalMeshedGearDesign
