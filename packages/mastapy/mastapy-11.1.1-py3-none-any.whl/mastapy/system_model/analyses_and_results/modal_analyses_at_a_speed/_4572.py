'''_4572.py

AssemblyModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6536, _6669
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _4573, _4575, _4578, _4585,
    _4584, _4588, _4593, _4596,
    _4606, _4608, _4610, _4614,
    _4620, _4621, _4622, _4629,
    _4636, _4639, _4640, _4641,
    _4643, _4647, _4650, _4651,
    _4652, _4660, _4654, _4656,
    _4661, _4666, _4669, _4672,
    _4675, _4679, _4683, _4686,
    _4690, _4693, _4565
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'AssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysisAtASpeed',)


class AssemblyModalAnalysisAtASpeed(_4565.AbstractAssemblyModalAnalysisAtASpeed):
    '''AssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2179.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6536.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6536.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def bearings(self) -> 'List[_4573.BearingModalAnalysisAtASpeed]':
        '''List[BearingModalAnalysisAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4573.BearingModalAnalysisAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_4575.BeltDriveModalAnalysisAtASpeed]':
        '''List[BeltDriveModalAnalysisAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4575.BeltDriveModalAnalysisAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4578.BevelDifferentialGearSetModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearSetModalAnalysisAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4578.BevelDifferentialGearSetModalAnalysisAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_4585.BoltModalAnalysisAtASpeed]':
        '''List[BoltModalAnalysisAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4585.BoltModalAnalysisAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_4584.BoltedJointModalAnalysisAtASpeed]':
        '''List[BoltedJointModalAnalysisAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4584.BoltedJointModalAnalysisAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_4588.ClutchModalAnalysisAtASpeed]':
        '''List[ClutchModalAnalysisAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4588.ClutchModalAnalysisAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_4593.ConceptCouplingModalAnalysisAtASpeed]':
        '''List[ConceptCouplingModalAnalysisAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4593.ConceptCouplingModalAnalysisAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4596.ConceptGearSetModalAnalysisAtASpeed]':
        '''List[ConceptGearSetModalAnalysisAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4596.ConceptGearSetModalAnalysisAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_4606.CVTModalAnalysisAtASpeed]':
        '''List[CVTModalAnalysisAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4606.CVTModalAnalysisAtASpeed))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4608.CycloidalAssemblyModalAnalysisAtASpeed]':
        '''List[CycloidalAssemblyModalAnalysisAtASpeed]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4608.CycloidalAssemblyModalAnalysisAtASpeed))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4610.CycloidalDiscModalAnalysisAtASpeed]':
        '''List[CycloidalDiscModalAnalysisAtASpeed]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4610.CycloidalDiscModalAnalysisAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4614.CylindricalGearSetModalAnalysisAtASpeed]':
        '''List[CylindricalGearSetModalAnalysisAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4614.CylindricalGearSetModalAnalysisAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4620.FaceGearSetModalAnalysisAtASpeed]':
        '''List[FaceGearSetModalAnalysisAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4620.FaceGearSetModalAnalysisAtASpeed))
        return value

    @property
    def fe_parts(self) -> 'List[_4621.FEPartModalAnalysisAtASpeed]':
        '''List[FEPartModalAnalysisAtASpeed]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4621.FEPartModalAnalysisAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4622.FlexiblePinAssemblyModalAnalysisAtASpeed]':
        '''List[FlexiblePinAssemblyModalAnalysisAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4622.FlexiblePinAssemblyModalAnalysisAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4629.HypoidGearSetModalAnalysisAtASpeed]':
        '''List[HypoidGearSetModalAnalysisAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4629.HypoidGearSetModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4636.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4636.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4639.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4639.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_4640.MassDiscModalAnalysisAtASpeed]':
        '''List[MassDiscModalAnalysisAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4640.MassDiscModalAnalysisAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_4641.MeasurementComponentModalAnalysisAtASpeed]':
        '''List[MeasurementComponentModalAnalysisAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4641.MeasurementComponentModalAnalysisAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_4643.OilSealModalAnalysisAtASpeed]':
        '''List[OilSealModalAnalysisAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4643.OilSealModalAnalysisAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4647.PartToPartShearCouplingModalAnalysisAtASpeed]':
        '''List[PartToPartShearCouplingModalAnalysisAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4647.PartToPartShearCouplingModalAnalysisAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_4650.PlanetCarrierModalAnalysisAtASpeed]':
        '''List[PlanetCarrierModalAnalysisAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4650.PlanetCarrierModalAnalysisAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_4651.PointLoadModalAnalysisAtASpeed]':
        '''List[PointLoadModalAnalysisAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4651.PointLoadModalAnalysisAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_4652.PowerLoadModalAnalysisAtASpeed]':
        '''List[PowerLoadModalAnalysisAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4652.PowerLoadModalAnalysisAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4660.ShaftHubConnectionModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionModalAnalysisAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4660.ShaftHubConnectionModalAnalysisAtASpeed))
        return value

    @property
    def ring_pins(self) -> 'List[_4654.RingPinsModalAnalysisAtASpeed]':
        '''List[RingPinsModalAnalysisAtASpeed]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4654.RingPinsModalAnalysisAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4656.RollingRingAssemblyModalAnalysisAtASpeed]':
        '''List[RollingRingAssemblyModalAnalysisAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4656.RollingRingAssemblyModalAnalysisAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_4661.ShaftModalAnalysisAtASpeed]':
        '''List[ShaftModalAnalysisAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4661.ShaftModalAnalysisAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4666.SpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearSetModalAnalysisAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4666.SpiralBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_4669.SpringDamperModalAnalysisAtASpeed]':
        '''List[SpringDamperModalAnalysisAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4669.SpringDamperModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4672.StraightBevelDiffGearSetModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4672.StraightBevelDiffGearSetModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4675.StraightBevelGearSetModalAnalysisAtASpeed]':
        '''List[StraightBevelGearSetModalAnalysisAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4675.StraightBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_4679.SynchroniserModalAnalysisAtASpeed]':
        '''List[SynchroniserModalAnalysisAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4679.SynchroniserModalAnalysisAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_4683.TorqueConverterModalAnalysisAtASpeed]':
        '''List[TorqueConverterModalAnalysisAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4683.TorqueConverterModalAnalysisAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4686.UnbalancedMassModalAnalysisAtASpeed]':
        '''List[UnbalancedMassModalAnalysisAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4686.UnbalancedMassModalAnalysisAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4690.WormGearSetModalAnalysisAtASpeed]':
        '''List[WormGearSetModalAnalysisAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4690.WormGearSetModalAnalysisAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4693.ZerolBevelGearSetModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearSetModalAnalysisAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4693.ZerolBevelGearSetModalAnalysisAtASpeed))
        return value
