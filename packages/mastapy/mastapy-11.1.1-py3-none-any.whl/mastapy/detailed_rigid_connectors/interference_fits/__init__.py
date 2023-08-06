'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1246 import AssemblyMethods
    from ._1247 import CalculationMethods
    from ._1248 import InterferenceFitDesign
    from ._1249 import InterferenceFitHalfDesign
    from ._1250 import StressRegions
    from ._1251 import Table4JointInterfaceTypes
