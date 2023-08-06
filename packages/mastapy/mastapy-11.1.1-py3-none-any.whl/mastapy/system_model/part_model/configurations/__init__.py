'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2354 import ActiveFESubstructureSelection
    from ._2355 import ActiveFESubstructureSelectionGroup
    from ._2356 import ActiveShaftDesignSelection
    from ._2357 import ActiveShaftDesignSelectionGroup
    from ._2358 import BearingDetailConfiguration
    from ._2359 import BearingDetailSelection
    from ._2360 import PartDetailConfiguration
    from ._2361 import PartDetailSelection
