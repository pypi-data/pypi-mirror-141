'''_5666.py

AbstractPeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6616, _6564, _6581, _6590,
    _6591, _6592, _6593, _6594,
    _6612, _6658, _6674, _6701
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    '''AbstractPeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_load_data(self) -> '_6616.HarmonicLoadDataBase':
        '''HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6616.HarmonicLoadDataBase.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to HarmonicLoadDataBase. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6564.ConicalGearSetHarmonicLoadData':
        '''ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6564.ConicalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6581.CylindricalGearSetHarmonicLoadData':
        '''CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6581.CylindricalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6590.ElectricMachineHarmonicLoadData':
        '''ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6590.ElectricMachineHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6591.ElectricMachineHarmonicLoadDataFromExcel':
        '''ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6591.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_flux(self) -> '_6592.ElectricMachineHarmonicLoadDataFromFlux':
        '''ElectricMachineHarmonicLoadDataFromFlux: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6592.ElectricMachineHarmonicLoadDataFromFlux.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromFlux. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6593.ElectricMachineHarmonicLoadDataFromJMAG':
        '''ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6593.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6594.ElectricMachineHarmonicLoadDataFromMotorCAD':
        '''ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6594.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6612.GearSetHarmonicLoadData':
        '''GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6612.GearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6658.PointLoadHarmonicLoadData':
        '''PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6658.PointLoadHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_6674.SpeedDependentHarmonicLoadData':
        '''SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6674.SpeedDependentHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6701.UnbalancedMassHarmonicLoadData':
        '''UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6701.UnbalancedMassHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new_override(self.wrapped.HarmonicLoadData.__class__)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData is not None else None
