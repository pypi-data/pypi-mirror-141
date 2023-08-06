'''_6737.py

AssemblyAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6536, _6669
from mastapy.system_model.analyses_and_results.system_deflections import _2435, _2538
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _6739, _6741, _6744, _6750,
    _6751, _6752, _6757, _6762,
    _6771, _6774, _6775, _6780,
    _6786, _6787, _6788, _6796,
    _6803, _6806, _6807, _6808,
    _6810, _6812, _6817, _6818,
    _6819, _6828, _6821, _6824,
    _6827, _6833, _6834, _6839,
    _6842, _6845, _6849, _6853,
    _6857, _6860, _6727
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'AssemblyAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedTimeSteppingAnalysisForModulation',)


class AssemblyAdvancedTimeSteppingAnalysisForModulation(_6727.AbstractAssemblyAdvancedTimeSteppingAnalysisForModulation):
    '''AssemblyAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def system_deflection_results(self) -> '_2435.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2435.AssemblySystemDeflection.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to AssemblySystemDeflection. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SystemDeflectionResults.__class__)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def bearings(self) -> 'List[_6739.BearingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BearingAdvancedTimeSteppingAnalysisForModulation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6739.BearingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def belt_drives(self) -> 'List[_6741.BeltDriveAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BeltDriveAdvancedTimeSteppingAnalysisForModulation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6741.BeltDriveAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6744.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6744.BevelDifferentialGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolts(self) -> 'List[_6750.BoltAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltAdvancedTimeSteppingAnalysisForModulation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6750.BoltAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def bolted_joints(self) -> 'List[_6751.BoltedJointAdvancedTimeSteppingAnalysisForModulation]':
        '''List[BoltedJointAdvancedTimeSteppingAnalysisForModulation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6751.BoltedJointAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def clutches(self) -> 'List[_6752.ClutchAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ClutchAdvancedTimeSteppingAnalysisForModulation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6752.ClutchAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_couplings(self) -> 'List[_6757.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptCouplingAdvancedTimeSteppingAnalysisForModulation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6757.ConceptCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6762.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ConceptGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6762.ConceptGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cv_ts(self) -> 'List[_6771.CVTAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CVTAdvancedTimeSteppingAnalysisForModulation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6771.CVTAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6774.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6774.CycloidalAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6775.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CycloidalDiscAdvancedTimeSteppingAnalysisForModulation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6775.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6780.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6780.CylindricalGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6786.FaceGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FaceGearSetAdvancedTimeSteppingAnalysisForModulation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6786.FaceGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def fe_parts(self) -> 'List[_6787.FEPartAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FEPartAdvancedTimeSteppingAnalysisForModulation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6787.FEPartAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6788.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6788.FlexiblePinAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6796.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[HypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6796.HypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6803.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6803.KlingelnbergCycloPalloidHypoidGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6806.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6806.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def mass_discs(self) -> 'List[_6807.MassDiscAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MassDiscAdvancedTimeSteppingAnalysisForModulation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6807.MassDiscAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def measurement_components(self) -> 'List[_6808.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]':
        '''List[MeasurementComponentAdvancedTimeSteppingAnalysisForModulation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6808.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def oil_seals(self) -> 'List[_6810.OilSealAdvancedTimeSteppingAnalysisForModulation]':
        '''List[OilSealAdvancedTimeSteppingAnalysisForModulation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6810.OilSealAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6812.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6812.PartToPartShearCouplingAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def planet_carriers(self) -> 'List[_6817.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetCarrierAdvancedTimeSteppingAnalysisForModulation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6817.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def point_loads(self) -> 'List[_6818.PointLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PointLoadAdvancedTimeSteppingAnalysisForModulation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6818.PointLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def power_loads(self) -> 'List[_6819.PowerLoadAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PowerLoadAdvancedTimeSteppingAnalysisForModulation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6819.PowerLoadAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6828.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6828.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def ring_pins(self) -> 'List[_6821.RingPinsAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RingPinsAdvancedTimeSteppingAnalysisForModulation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6821.RingPinsAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6824.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]':
        '''List[RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6824.RollingRingAssemblyAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def shafts(self) -> 'List[_6827.ShaftAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ShaftAdvancedTimeSteppingAnalysisForModulation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6827.ShaftAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6833.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6833.SpiralBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def spring_dampers(self) -> 'List[_6834.SpringDamperAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SpringDamperAdvancedTimeSteppingAnalysisForModulation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6834.SpringDamperAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6839.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6839.StraightBevelDiffGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6842.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6842.StraightBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def synchronisers(self) -> 'List[_6845.SynchroniserAdvancedTimeSteppingAnalysisForModulation]':
        '''List[SynchroniserAdvancedTimeSteppingAnalysisForModulation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6845.SynchroniserAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def torque_converters(self) -> 'List[_6849.TorqueConverterAdvancedTimeSteppingAnalysisForModulation]':
        '''List[TorqueConverterAdvancedTimeSteppingAnalysisForModulation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6849.TorqueConverterAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6853.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]':
        '''List[UnbalancedMassAdvancedTimeSteppingAnalysisForModulation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6853.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6857.WormGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[WormGearSetAdvancedTimeSteppingAnalysisForModulation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6857.WormGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6860.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6860.ZerolBevelGearSetAdvancedTimeSteppingAnalysisForModulation))
        return value
