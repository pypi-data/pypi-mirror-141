'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._935 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._936 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._937 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._938 import KlingelnbergCycloPalloidHypoidMeshedGearDesign
