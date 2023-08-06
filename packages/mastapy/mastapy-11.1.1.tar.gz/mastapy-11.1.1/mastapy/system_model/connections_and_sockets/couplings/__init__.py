'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2087 import ClutchConnection
    from ._2088 import ClutchSocket
    from ._2089 import ConceptCouplingConnection
    from ._2090 import ConceptCouplingSocket
    from ._2091 import CouplingConnection
    from ._2092 import CouplingSocket
    from ._2093 import PartToPartShearCouplingConnection
    from ._2094 import PartToPartShearCouplingSocket
    from ._2095 import SpringDamperConnection
    from ._2096 import SpringDamperSocket
    from ._2097 import TorqueConverterConnection
    from ._2098 import TorqueConverterPumpSocket
    from ._2099 import TorqueConverterTurbineSocket
