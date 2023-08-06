'''overridable.py

Implementations of 'Overridable' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from enum import Enum
from typing import Generic, TypeVar

from mastapy._internal import (
    mixins, constructor, enum_with_selected_value_runtime, conversion
)
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _222
from mastapy.gears import (
    _301, _286, _289, _304
)
from mastapy.bearings.bearing_designs.rolling import _1925, _1908, _1902
from mastapy.bearings import _1658
from mastapy.nodal_analysis.dev_tools_analyses import _176
from mastapy.nodal_analysis.fe_export_utility import _152
from mastapy.system_model.fe import _2146
from mastapy.materials.efficiency import _261, _263
from mastapy.bearings.bearing_results import _1700
from mastapy.system_model.part_model import _2222
from mastapy.bearings.bearing_results.rolling import _1728, _1822
from mastapy.gears.rating.cylindrical.iso6336 import _472
from mastapy.system_model.analyses_and_results.static_loads import _6643

_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'Overridable')


__docformat__ = 'restructuredtext en'
__all__ = (
    'Overridable_float', 'Overridable_int',
    'Overridable_CylindricalGearRatingMethods', 'Overridable_ISOToleranceStandard',
    'Overridable_CoefficientOfFrictionCalculationMethod', 'Overridable_T',
    'Overridable_WidthSeries', 'Overridable_HeightSeries',
    'Overridable_DiameterSeries', 'Overridable_bool',
    'Overridable_SealLocation', 'Overridable_RigidCouplingType',
    'Overridable_BoundaryConditionType', 'Overridable_NodeSelectionDepthOption',
    'Overridable_BearingEfficiencyRatingMethod', 'Overridable_CylindricalRollerMaxAxialLoadMethod',
    'Overridable_ContactRatioRequirements', 'Overridable_MicroGeometryModel',
    'Overridable_UnbalancedMassInclusionOption', 'Overridable_FrictionModelForGyroscopicMoment',
    'Overridable_RollerAnalysisMethod', 'Overridable_HelicalGearMicroGeometryOption',
    'Overridable_EfficiencyRatingMethod', 'Overridable_MeshStiffnessSource'
)


T = TypeVar('T')


class Overridable_float(float, mixins.OverridableMixin):
    '''Overridable_float

    A specific implementation of 'Overridable' for 'float' types.
    '''

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'Overridable_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else 0.0)

    def __init__(self, instance_to_wrap: 'Overridable_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def value(self) -> 'float':
        '''float: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'float':
        '''float: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'float':
        '''float: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue


class Overridable_int(int, mixins.OverridableMixin):
    '''Overridable_int

    A specific implementation of 'Overridable' for 'int' types.
    '''

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'Overridable_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else 0)

    def __init__(self, instance_to_wrap: 'Overridable_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def value(self) -> 'int':
        '''int: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'int':
        '''int: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'int':
        '''int: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue


class Overridable_CylindricalGearRatingMethods(mixins.OverridableMixin, Enum):
    '''Overridable_CylindricalGearRatingMethods

    A specific implementation of 'Overridable' for 'CylindricalGearRatingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_222.CylindricalGearRatingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _222.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_222.CylindricalGearRatingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _222.CylindricalGearRatingMethods.type_()

    @property
    def value(self) -> '_222.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_222.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_222.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_ISOToleranceStandard(mixins.OverridableMixin, Enum):
    '''Overridable_ISOToleranceStandard

    A specific implementation of 'Overridable' for 'ISOToleranceStandard' types.
    '''

    __hash__ = None
    __qualname__ = 'ISOToleranceStandard'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_301.ISOToleranceStandard':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _301.ISOToleranceStandard

    @classmethod
    def implicit_type(cls) -> '_301.ISOToleranceStandard.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _301.ISOToleranceStandard.type_()

    @property
    def value(self) -> '_301.ISOToleranceStandard':
        '''ISOToleranceStandard: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_301.ISOToleranceStandard':
        '''ISOToleranceStandard: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_301.ISOToleranceStandard':
        '''ISOToleranceStandard: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_CoefficientOfFrictionCalculationMethod(mixins.OverridableMixin, Enum):
    '''Overridable_CoefficientOfFrictionCalculationMethod

    A specific implementation of 'Overridable' for 'CoefficientOfFrictionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'CoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_286.CoefficientOfFrictionCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _286.CoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_286.CoefficientOfFrictionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _286.CoefficientOfFrictionCalculationMethod.type_()

    @property
    def value(self) -> '_286.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_286.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_286.CoefficientOfFrictionCalculationMethod':
        '''CoefficientOfFrictionCalculationMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_T(Generic[T], mixins.OverridableMixin):
    '''Overridable_T

    A specific implementation of 'Overridable' for 'T' types.
    '''

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'Overridable_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def value(self) -> 'T':
        '''T: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'T':
        '''T: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'T':
        '''T: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue


class Overridable_WidthSeries(mixins.OverridableMixin, Enum):
    '''Overridable_WidthSeries

    A specific implementation of 'Overridable' for 'WidthSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'WidthSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1925.WidthSeries':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1925.WidthSeries

    @classmethod
    def implicit_type(cls) -> '_1925.WidthSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1925.WidthSeries.type_()

    @property
    def value(self) -> '_1925.WidthSeries':
        '''WidthSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1925.WidthSeries':
        '''WidthSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1925.WidthSeries':
        '''WidthSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_HeightSeries(mixins.OverridableMixin, Enum):
    '''Overridable_HeightSeries

    A specific implementation of 'Overridable' for 'HeightSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'HeightSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1908.HeightSeries':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1908.HeightSeries

    @classmethod
    def implicit_type(cls) -> '_1908.HeightSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1908.HeightSeries.type_()

    @property
    def value(self) -> '_1908.HeightSeries':
        '''HeightSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1908.HeightSeries':
        '''HeightSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1908.HeightSeries':
        '''HeightSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_DiameterSeries(mixins.OverridableMixin, Enum):
    '''Overridable_DiameterSeries

    A specific implementation of 'Overridable' for 'DiameterSeries' types.
    '''

    __hash__ = None
    __qualname__ = 'DiameterSeries'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1902.DiameterSeries':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1902.DiameterSeries

    @classmethod
    def implicit_type(cls) -> '_1902.DiameterSeries.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1902.DiameterSeries.type_()

    @property
    def value(self) -> '_1902.DiameterSeries':
        '''DiameterSeries: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1902.DiameterSeries':
        '''DiameterSeries: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1902.DiameterSeries':
        '''DiameterSeries: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_bool(mixins.OverridableMixin):
    '''Overridable_bool

    A specific implementation of 'Overridable' for 'bool' types.
    '''

    __hash__ = None
    __qualname__ = 'bool'

    def __new__(cls, instance_to_wrap: 'Overridable_bool.TYPE'):
        return bool.__new__(cls, instance_to_wrap.Value if instance_to_wrap.Value is not None else False)

    def __init__(self, instance_to_wrap: 'Overridable_bool.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.Value
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls) -> 'bool':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return bool

    @property
    def value(self) -> 'bool':
        '''bool: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Value

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.Overridden

    @property
    def override_value(self) -> 'bool':
        '''bool: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.OverrideValue

    @property
    def calculated_value(self) -> 'bool':
        '''bool: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.CalculatedValue

    def __bool__(self):
        return self.value


class Overridable_SealLocation(mixins.OverridableMixin, Enum):
    '''Overridable_SealLocation

    A specific implementation of 'Overridable' for 'SealLocation' types.
    '''

    __hash__ = None
    __qualname__ = 'SealLocation'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1658.SealLocation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1658.SealLocation

    @classmethod
    def implicit_type(cls) -> '_1658.SealLocation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1658.SealLocation.type_()

    @property
    def value(self) -> '_1658.SealLocation':
        '''SealLocation: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1658.SealLocation':
        '''SealLocation: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1658.SealLocation':
        '''SealLocation: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_RigidCouplingType(mixins.OverridableMixin, Enum):
    '''Overridable_RigidCouplingType

    A specific implementation of 'Overridable' for 'RigidCouplingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidCouplingType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_176.RigidCouplingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _176.RigidCouplingType

    @classmethod
    def implicit_type(cls) -> '_176.RigidCouplingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _176.RigidCouplingType.type_()

    @property
    def value(self) -> '_176.RigidCouplingType':
        '''RigidCouplingType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_176.RigidCouplingType':
        '''RigidCouplingType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_176.RigidCouplingType':
        '''RigidCouplingType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_BoundaryConditionType(mixins.OverridableMixin, Enum):
    '''Overridable_BoundaryConditionType

    A specific implementation of 'Overridable' for 'BoundaryConditionType' types.
    '''

    __hash__ = None
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_152.BoundaryConditionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _152.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_152.BoundaryConditionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _152.BoundaryConditionType.type_()

    @property
    def value(self) -> '_152.BoundaryConditionType':
        '''BoundaryConditionType: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_152.BoundaryConditionType':
        '''BoundaryConditionType: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_152.BoundaryConditionType':
        '''BoundaryConditionType: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_NodeSelectionDepthOption(mixins.OverridableMixin, Enum):
    '''Overridable_NodeSelectionDepthOption

    A specific implementation of 'Overridable' for 'NodeSelectionDepthOption' types.
    '''

    __hash__ = None
    __qualname__ = 'NodeSelectionDepthOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_2146.NodeSelectionDepthOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2146.NodeSelectionDepthOption

    @classmethod
    def implicit_type(cls) -> '_2146.NodeSelectionDepthOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2146.NodeSelectionDepthOption.type_()

    @property
    def value(self) -> '_2146.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_2146.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_2146.NodeSelectionDepthOption':
        '''NodeSelectionDepthOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_BearingEfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    '''Overridable_BearingEfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'BearingEfficiencyRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingEfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_261.BearingEfficiencyRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _261.BearingEfficiencyRatingMethod

    @classmethod
    def implicit_type(cls) -> '_261.BearingEfficiencyRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _261.BearingEfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_261.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_261.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_261.BearingEfficiencyRatingMethod':
        '''BearingEfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_CylindricalRollerMaxAxialLoadMethod(mixins.OverridableMixin, Enum):
    '''Overridable_CylindricalRollerMaxAxialLoadMethod

    A specific implementation of 'Overridable' for 'CylindricalRollerMaxAxialLoadMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalRollerMaxAxialLoadMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1700.CylindricalRollerMaxAxialLoadMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1700.CylindricalRollerMaxAxialLoadMethod

    @classmethod
    def implicit_type(cls) -> '_1700.CylindricalRollerMaxAxialLoadMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1700.CylindricalRollerMaxAxialLoadMethod.type_()

    @property
    def value(self) -> '_1700.CylindricalRollerMaxAxialLoadMethod':
        '''CylindricalRollerMaxAxialLoadMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1700.CylindricalRollerMaxAxialLoadMethod':
        '''CylindricalRollerMaxAxialLoadMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1700.CylindricalRollerMaxAxialLoadMethod':
        '''CylindricalRollerMaxAxialLoadMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_ContactRatioRequirements(mixins.OverridableMixin, Enum):
    '''Overridable_ContactRatioRequirements

    A specific implementation of 'Overridable' for 'ContactRatioRequirements' types.
    '''

    __hash__ = None
    __qualname__ = 'ContactRatioRequirements'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_289.ContactRatioRequirements':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _289.ContactRatioRequirements

    @classmethod
    def implicit_type(cls) -> '_289.ContactRatioRequirements.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _289.ContactRatioRequirements.type_()

    @property
    def value(self) -> '_289.ContactRatioRequirements':
        '''ContactRatioRequirements: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_289.ContactRatioRequirements':
        '''ContactRatioRequirements: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_289.ContactRatioRequirements':
        '''ContactRatioRequirements: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_MicroGeometryModel(mixins.OverridableMixin, Enum):
    '''Overridable_MicroGeometryModel

    A specific implementation of 'Overridable' for 'MicroGeometryModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_304.MicroGeometryModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _304.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_304.MicroGeometryModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _304.MicroGeometryModel.type_()

    @property
    def value(self) -> '_304.MicroGeometryModel':
        '''MicroGeometryModel: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_304.MicroGeometryModel':
        '''MicroGeometryModel: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_304.MicroGeometryModel':
        '''MicroGeometryModel: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_UnbalancedMassInclusionOption(mixins.OverridableMixin, Enum):
    '''Overridable_UnbalancedMassInclusionOption

    A specific implementation of 'Overridable' for 'UnbalancedMassInclusionOption' types.
    '''

    __hash__ = None
    __qualname__ = 'UnbalancedMassInclusionOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_2222.UnbalancedMassInclusionOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2222.UnbalancedMassInclusionOption

    @classmethod
    def implicit_type(cls) -> '_2222.UnbalancedMassInclusionOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2222.UnbalancedMassInclusionOption.type_()

    @property
    def value(self) -> '_2222.UnbalancedMassInclusionOption':
        '''UnbalancedMassInclusionOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_2222.UnbalancedMassInclusionOption':
        '''UnbalancedMassInclusionOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_2222.UnbalancedMassInclusionOption':
        '''UnbalancedMassInclusionOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_FrictionModelForGyroscopicMoment(mixins.OverridableMixin, Enum):
    '''Overridable_FrictionModelForGyroscopicMoment

    A specific implementation of 'Overridable' for 'FrictionModelForGyroscopicMoment' types.
    '''

    __hash__ = None
    __qualname__ = 'FrictionModelForGyroscopicMoment'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1728.FrictionModelForGyroscopicMoment':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1728.FrictionModelForGyroscopicMoment

    @classmethod
    def implicit_type(cls) -> '_1728.FrictionModelForGyroscopicMoment.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1728.FrictionModelForGyroscopicMoment.type_()

    @property
    def value(self) -> '_1728.FrictionModelForGyroscopicMoment':
        '''FrictionModelForGyroscopicMoment: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1728.FrictionModelForGyroscopicMoment':
        '''FrictionModelForGyroscopicMoment: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1728.FrictionModelForGyroscopicMoment':
        '''FrictionModelForGyroscopicMoment: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_RollerAnalysisMethod(mixins.OverridableMixin, Enum):
    '''Overridable_RollerAnalysisMethod

    A specific implementation of 'Overridable' for 'RollerAnalysisMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'RollerAnalysisMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_1822.RollerAnalysisMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1822.RollerAnalysisMethod

    @classmethod
    def implicit_type(cls) -> '_1822.RollerAnalysisMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1822.RollerAnalysisMethod.type_()

    @property
    def value(self) -> '_1822.RollerAnalysisMethod':
        '''RollerAnalysisMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_1822.RollerAnalysisMethod':
        '''RollerAnalysisMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_1822.RollerAnalysisMethod':
        '''RollerAnalysisMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_HelicalGearMicroGeometryOption(mixins.OverridableMixin, Enum):
    '''Overridable_HelicalGearMicroGeometryOption

    A specific implementation of 'Overridable' for 'HelicalGearMicroGeometryOption' types.
    '''

    __hash__ = None
    __qualname__ = 'HelicalGearMicroGeometryOption'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_472.HelicalGearMicroGeometryOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _472.HelicalGearMicroGeometryOption

    @classmethod
    def implicit_type(cls) -> '_472.HelicalGearMicroGeometryOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _472.HelicalGearMicroGeometryOption.type_()

    @property
    def value(self) -> '_472.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_472.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_472.HelicalGearMicroGeometryOption':
        '''HelicalGearMicroGeometryOption: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_EfficiencyRatingMethod(mixins.OverridableMixin, Enum):
    '''Overridable_EfficiencyRatingMethod

    A specific implementation of 'Overridable' for 'EfficiencyRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'EfficiencyRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_263.EfficiencyRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _263.EfficiencyRatingMethod

    @classmethod
    def implicit_type(cls) -> '_263.EfficiencyRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _263.EfficiencyRatingMethod.type_()

    @property
    def value(self) -> '_263.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_263.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_263.EfficiencyRatingMethod':
        '''EfficiencyRatingMethod: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class Overridable_MeshStiffnessSource(mixins.OverridableMixin, Enum):
    '''Overridable_MeshStiffnessSource

    A specific implementation of 'Overridable' for 'MeshStiffnessSource' types.
    '''

    __hash__ = None
    __qualname__ = 'MeshStiffnessSource'

    @classmethod
    def wrapper_type(cls) -> '_OVERRIDABLE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls) -> '_6643.MeshStiffnessSource':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6643.MeshStiffnessSource

    @classmethod
    def implicit_type(cls) -> '_6643.MeshStiffnessSource.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6643.MeshStiffnessSource.type_()

    @property
    def value(self) -> '_6643.MeshStiffnessSource':
        '''MeshStiffnessSource: 'Value' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def overridden(self) -> 'bool':
        '''bool: 'Overridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def override_value(self) -> '_6643.MeshStiffnessSource':
        '''MeshStiffnessSource: 'OverrideValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def calculated_value(self) -> '_6643.MeshStiffnessSource':
        '''MeshStiffnessSource: 'CalculatedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None
