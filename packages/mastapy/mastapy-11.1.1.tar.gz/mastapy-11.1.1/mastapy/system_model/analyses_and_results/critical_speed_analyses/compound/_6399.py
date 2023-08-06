'''_6399.py

AssemblyCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6268
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6400, _6402, _6405, _6411,
    _6412, _6413, _6418, _6423,
    _6433, _6435, _6437, _6441,
    _6447, _6448, _6449, _6456,
    _6463, _6466, _6467, _6468,
    _6470, _6472, _6477, _6478,
    _6479, _6488, _6481, _6483,
    _6487, _6493, _6494, _6499,
    _6502, _6505, _6509, _6513,
    _6517, _6520, _6392
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'AssemblyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundCriticalSpeedAnalysis',)


class AssemblyCompoundCriticalSpeedAnalysis(_6392.AbstractAssemblyCompoundCriticalSpeedAnalysis):
    '''AssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2179.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_6268.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6268.AssemblyCriticalSpeedAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_6400.BearingCompoundCriticalSpeedAnalysis]':
        '''List[BearingCompoundCriticalSpeedAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6400.BearingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_6402.BeltDriveCompoundCriticalSpeedAnalysis]':
        '''List[BeltDriveCompoundCriticalSpeedAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6402.BeltDriveCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6405.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6405.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_6411.BoltCompoundCriticalSpeedAnalysis]':
        '''List[BoltCompoundCriticalSpeedAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6411.BoltCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_6412.BoltedJointCompoundCriticalSpeedAnalysis]':
        '''List[BoltedJointCompoundCriticalSpeedAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6412.BoltedJointCompoundCriticalSpeedAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_6413.ClutchCompoundCriticalSpeedAnalysis]':
        '''List[ClutchCompoundCriticalSpeedAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6413.ClutchCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_6418.ConceptCouplingCompoundCriticalSpeedAnalysis]':
        '''List[ConceptCouplingCompoundCriticalSpeedAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6418.ConceptCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6423.ConceptGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ConceptGearSetCompoundCriticalSpeedAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6423.ConceptGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6433.CVTCompoundCriticalSpeedAnalysis]':
        '''List[CVTCompoundCriticalSpeedAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6433.CVTCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6435.CycloidalAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalAssemblyCompoundCriticalSpeedAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6435.CycloidalAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6437.CycloidalDiscCompoundCriticalSpeedAnalysis]':
        '''List[CycloidalDiscCompoundCriticalSpeedAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6437.CycloidalDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6441.CylindricalGearSetCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearSetCompoundCriticalSpeedAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6441.CylindricalGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6447.FaceGearSetCompoundCriticalSpeedAnalysis]':
        '''List[FaceGearSetCompoundCriticalSpeedAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6447.FaceGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6448.FEPartCompoundCriticalSpeedAnalysis]':
        '''List[FEPartCompoundCriticalSpeedAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6448.FEPartCompoundCriticalSpeedAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6449.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[FlexiblePinAssemblyCompoundCriticalSpeedAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6449.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6456.HypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCompoundCriticalSpeedAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6456.HypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6463.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6463.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6466.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6466.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6467.MassDiscCompoundCriticalSpeedAnalysis]':
        '''List[MassDiscCompoundCriticalSpeedAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6467.MassDiscCompoundCriticalSpeedAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6468.MeasurementComponentCompoundCriticalSpeedAnalysis]':
        '''List[MeasurementComponentCompoundCriticalSpeedAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6468.MeasurementComponentCompoundCriticalSpeedAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6470.OilSealCompoundCriticalSpeedAnalysis]':
        '''List[OilSealCompoundCriticalSpeedAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6470.OilSealCompoundCriticalSpeedAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6472.PartToPartShearCouplingCompoundCriticalSpeedAnalysis]':
        '''List[PartToPartShearCouplingCompoundCriticalSpeedAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6472.PartToPartShearCouplingCompoundCriticalSpeedAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6477.PlanetCarrierCompoundCriticalSpeedAnalysis]':
        '''List[PlanetCarrierCompoundCriticalSpeedAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6477.PlanetCarrierCompoundCriticalSpeedAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6478.PointLoadCompoundCriticalSpeedAnalysis]':
        '''List[PointLoadCompoundCriticalSpeedAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6478.PointLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6479.PowerLoadCompoundCriticalSpeedAnalysis]':
        '''List[PowerLoadCompoundCriticalSpeedAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6479.PowerLoadCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6488.ShaftHubConnectionCompoundCriticalSpeedAnalysis]':
        '''List[ShaftHubConnectionCompoundCriticalSpeedAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6488.ShaftHubConnectionCompoundCriticalSpeedAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6481.RingPinsCompoundCriticalSpeedAnalysis]':
        '''List[RingPinsCompoundCriticalSpeedAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6481.RingPinsCompoundCriticalSpeedAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6483.RollingRingAssemblyCompoundCriticalSpeedAnalysis]':
        '''List[RollingRingAssemblyCompoundCriticalSpeedAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6483.RollingRingAssemblyCompoundCriticalSpeedAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6487.ShaftCompoundCriticalSpeedAnalysis]':
        '''List[ShaftCompoundCriticalSpeedAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6487.ShaftCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6493.SpiralBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6493.SpiralBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6494.SpringDamperCompoundCriticalSpeedAnalysis]':
        '''List[SpringDamperCompoundCriticalSpeedAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6494.SpringDamperCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6499.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6499.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6502.StraightBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelGearSetCompoundCriticalSpeedAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6502.StraightBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6505.SynchroniserCompoundCriticalSpeedAnalysis]':
        '''List[SynchroniserCompoundCriticalSpeedAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6505.SynchroniserCompoundCriticalSpeedAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6509.TorqueConverterCompoundCriticalSpeedAnalysis]':
        '''List[TorqueConverterCompoundCriticalSpeedAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6509.TorqueConverterCompoundCriticalSpeedAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6513.UnbalancedMassCompoundCriticalSpeedAnalysis]':
        '''List[UnbalancedMassCompoundCriticalSpeedAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6513.UnbalancedMassCompoundCriticalSpeedAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6517.WormGearSetCompoundCriticalSpeedAnalysis]':
        '''List[WormGearSetCompoundCriticalSpeedAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6517.WormGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6520.ZerolBevelGearSetCompoundCriticalSpeedAnalysis]':
        '''List[ZerolBevelGearSetCompoundCriticalSpeedAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6520.ZerolBevelGearSetCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6268.AssemblyCriticalSpeedAnalysis]':
        '''List[AssemblyCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6268.AssemblyCriticalSpeedAnalysis))
        return value
