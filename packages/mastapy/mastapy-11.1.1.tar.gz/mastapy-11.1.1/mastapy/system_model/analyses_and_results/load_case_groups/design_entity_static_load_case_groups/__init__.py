'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5400 import AbstractAssemblyStaticLoadCaseGroup
    from ._5401 import ComponentStaticLoadCaseGroup
    from ._5402 import ConnectionStaticLoadCaseGroup
    from ._5403 import DesignEntityStaticLoadCaseGroup
    from ._5404 import GearSetStaticLoadCaseGroup
    from ._5405 import PartStaticLoadCaseGroup
