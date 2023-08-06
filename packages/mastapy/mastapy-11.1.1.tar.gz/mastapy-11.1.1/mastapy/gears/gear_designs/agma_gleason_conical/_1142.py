'''_1142.py

AGMAGleasonConicalGearDesign
'''


from mastapy.gears.gear_designs.conical import (
    _1113, _1107, _1106, _1102,
    _1112, _1103
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.bevel.cutters import (
    _774, _775, _776, _777
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears import _281
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1085, _1089, _1094
from mastapy.gears.gear_designs.agma_gleason_conical import _1141
from mastapy.gears.materials import (
    _555, _544, _546, _548,
    _552, _558, _562, _564
)

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_AGMA_GLEASON_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.AGMAGleasonConical', 'AGMAGleasonConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearDesign',)


class AGMAGleasonConicalGearDesign(_1103.ConicalGearDesign):
    '''AGMAGleasonConicalGearDesign

    This is a mastapy class.
    '''

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def front_end_type(self) -> '_1113.FrontEndTypes':
        '''FrontEndTypes: 'FrontEndType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FrontEndType)
        return constructor.new(_1113.FrontEndTypes)(value) if value is not None else None

    @front_end_type.setter
    def front_end_type(self, value: '_1113.FrontEndTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FrontEndType = value

    @property
    def manufacture_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods: 'ManufactureMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.ManufactureMethod, value) if self.wrapped.ManufactureMethod is not None else None

    @manufacture_method.setter
    def manufacture_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalManufactureMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ManufactureMethod = value

    @property
    def machine_setting_calculation_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods: 'MachineSettingCalculationMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.MachineSettingCalculationMethod, value) if self.wrapped.MachineSettingCalculationMethod is not None else None

    @machine_setting_calculation_method.setter
    def machine_setting_calculation_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ConicalMachineSettingCalculationMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.MachineSettingCalculationMethod = value

    @property
    def material(self) -> 'str':
        '''str: 'Material' is the original name of this property.'''

        return self.wrapped.Material.SelectedItemName

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else '')

    @property
    def allowable_bending_stress(self) -> 'float':
        '''float: 'AllowableBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableBendingStress

    @property
    def allowable_contact_stress(self) -> 'float':
        '''float: 'AllowableContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableContactStress

    @property
    def face_width(self) -> 'float':
        '''float: 'FaceWidth' is the original name of this property.'''

        return self.wrapped.FaceWidth

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def cutter(self) -> '_1102.ConicalGearCutter':
        '''ConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1102.ConicalGearCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to ConicalGearCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def cutter_of_type_pinion_finish_cutter(self) -> '_774.PinionFinishCutter':
        '''PinionFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _774.PinionFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def cutter_of_type_pinion_rough_cutter(self) -> '_775.PinionRoughCutter':
        '''PinionRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _775.PinionRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to PinionRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def cutter_of_type_wheel_finish_cutter(self) -> '_776.WheelFinishCutter':
        '''WheelFinishCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _776.WheelFinishCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelFinishCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def cutter_of_type_wheel_rough_cutter(self) -> '_777.WheelRoughCutter':
        '''WheelRoughCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _777.WheelRoughCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to WheelRoughCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def cutter_of_type_dummy_conical_gear_cutter(self) -> '_1112.DummyConicalGearCutter':
        '''DummyConicalGearCutter: 'Cutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1112.DummyConicalGearCutter.TYPE not in self.wrapped.Cutter.__class__.__mro__:
            raise CastException('Failed to cast cutter to DummyConicalGearCutter. Expected: {}.'.format(self.wrapped.Cutter.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Cutter.__class__)(self.wrapped.Cutter) if self.wrapped.Cutter is not None else None

    @property
    def accuracy_grades(self) -> '_281.AccuracyGrades':
        '''AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _281.AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AccuracyGrades.__class__)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades is not None else None

    @property
    def accuracy_grades_of_type_agma20151_accuracy_grades(self) -> '_1085.AGMA20151AccuracyGrades':
        '''AGMA20151AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1085.AGMA20151AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMA20151AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AccuracyGrades.__class__)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades is not None else None

    @property
    def accuracy_grades_of_type_cylindrical_accuracy_grades(self) -> '_1089.CylindricalAccuracyGrades':
        '''CylindricalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1089.CylindricalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to CylindricalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AccuracyGrades.__class__)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades is not None else None

    @property
    def accuracy_grades_of_type_iso1328_accuracy_grades(self) -> '_1094.ISO1328AccuracyGrades':
        '''ISO1328AccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1094.ISO1328AccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to ISO1328AccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AccuracyGrades.__class__)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades is not None else None

    @property
    def accuracy_grades_of_type_agma_gleason_conical_accuracy_grades(self) -> '_1141.AGMAGleasonConicalAccuracyGrades':
        '''AGMAGleasonConicalAccuracyGrades: 'AccuracyGrades' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1141.AGMAGleasonConicalAccuracyGrades.TYPE not in self.wrapped.AccuracyGrades.__class__.__mro__:
            raise CastException('Failed to cast accuracy_grades to AGMAGleasonConicalAccuracyGrades. Expected: {}.'.format(self.wrapped.AccuracyGrades.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AccuracyGrades.__class__)(self.wrapped.AccuracyGrades) if self.wrapped.AccuracyGrades is not None else None

    @property
    def bevel_gear_material(self) -> '_555.GearMaterial':
        '''GearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _555.GearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to GearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_agma_cylindrical_gear_material(self) -> '_544.AGMACylindricalGearMaterial':
        '''AGMACylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _544.AGMACylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to AGMACylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_bevel_gear_iso_material(self) -> '_546.BevelGearISOMaterial':
        '''BevelGearISOMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _546.BevelGearISOMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearISOMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_bevel_gear_material(self) -> '_548.BevelGearMaterial':
        '''BevelGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _548.BevelGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to BevelGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_cylindrical_gear_material(self) -> '_552.CylindricalGearMaterial':
        '''CylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _552.CylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to CylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_iso_cylindrical_gear_material(self) -> '_558.ISOCylindricalGearMaterial':
        '''ISOCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _558.ISOCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to ISOCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_klingelnberg_cyclo_palloid_conical_gear_material(self) -> '_562.KlingelnbergCycloPalloidConicalGearMaterial':
        '''KlingelnbergCycloPalloidConicalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _562.KlingelnbergCycloPalloidConicalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to KlingelnbergCycloPalloidConicalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None

    @property
    def bevel_gear_material_of_type_plastic_cylindrical_gear_material(self) -> '_564.PlasticCylindricalGearMaterial':
        '''PlasticCylindricalGearMaterial: 'BevelGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _564.PlasticCylindricalGearMaterial.TYPE not in self.wrapped.BevelGearMaterial.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_material to PlasticCylindricalGearMaterial. Expected: {}.'.format(self.wrapped.BevelGearMaterial.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BevelGearMaterial.__class__)(self.wrapped.BevelGearMaterial) if self.wrapped.BevelGearMaterial is not None else None
