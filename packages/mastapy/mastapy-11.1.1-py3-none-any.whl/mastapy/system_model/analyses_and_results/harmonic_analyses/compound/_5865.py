'''_5865.py

AssemblyCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5673
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import (
    _5866, _5868, _5871, _5877,
    _5878, _5879, _5884, _5889,
    _5899, _5901, _5903, _5907,
    _5913, _5914, _5915, _5922,
    _5929, _5932, _5933, _5934,
    _5936, _5938, _5943, _5944,
    _5945, _5954, _5947, _5949,
    _5953, _5959, _5960, _5965,
    _5968, _5971, _5975, _5979,
    _5983, _5986, _5858
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'AssemblyCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundHarmonicAnalysis',)


class AssemblyCompoundHarmonicAnalysis(_5858.AbstractAssemblyCompoundHarmonicAnalysis):
    '''AssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundHarmonicAnalysis.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_5673.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_5673.AssemblyHarmonicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5866.BearingCompoundHarmonicAnalysis]':
        '''List[BearingCompoundHarmonicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5866.BearingCompoundHarmonicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5868.BeltDriveCompoundHarmonicAnalysis]':
        '''List[BeltDriveCompoundHarmonicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5868.BeltDriveCompoundHarmonicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5871.BevelDifferentialGearSetCompoundHarmonicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundHarmonicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5871.BevelDifferentialGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5877.BoltCompoundHarmonicAnalysis]':
        '''List[BoltCompoundHarmonicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5877.BoltCompoundHarmonicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5878.BoltedJointCompoundHarmonicAnalysis]':
        '''List[BoltedJointCompoundHarmonicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5878.BoltedJointCompoundHarmonicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5879.ClutchCompoundHarmonicAnalysis]':
        '''List[ClutchCompoundHarmonicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5879.ClutchCompoundHarmonicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5884.ConceptCouplingCompoundHarmonicAnalysis]':
        '''List[ConceptCouplingCompoundHarmonicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5884.ConceptCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5889.ConceptGearSetCompoundHarmonicAnalysis]':
        '''List[ConceptGearSetCompoundHarmonicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5889.ConceptGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5899.CVTCompoundHarmonicAnalysis]':
        '''List[CVTCompoundHarmonicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5899.CVTCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5901.CycloidalAssemblyCompoundHarmonicAnalysis]':
        '''List[CycloidalAssemblyCompoundHarmonicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5901.CycloidalAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5903.CycloidalDiscCompoundHarmonicAnalysis]':
        '''List[CycloidalDiscCompoundHarmonicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5903.CycloidalDiscCompoundHarmonicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5907.CylindricalGearSetCompoundHarmonicAnalysis]':
        '''List[CylindricalGearSetCompoundHarmonicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5907.CylindricalGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5913.FaceGearSetCompoundHarmonicAnalysis]':
        '''List[FaceGearSetCompoundHarmonicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5913.FaceGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5914.FEPartCompoundHarmonicAnalysis]':
        '''List[FEPartCompoundHarmonicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5914.FEPartCompoundHarmonicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5915.FlexiblePinAssemblyCompoundHarmonicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundHarmonicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5915.FlexiblePinAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5922.HypoidGearSetCompoundHarmonicAnalysis]':
        '''List[HypoidGearSetCompoundHarmonicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5922.HypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5929.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5929.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5932.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5932.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5933.MassDiscCompoundHarmonicAnalysis]':
        '''List[MassDiscCompoundHarmonicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5933.MassDiscCompoundHarmonicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5934.MeasurementComponentCompoundHarmonicAnalysis]':
        '''List[MeasurementComponentCompoundHarmonicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5934.MeasurementComponentCompoundHarmonicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5936.OilSealCompoundHarmonicAnalysis]':
        '''List[OilSealCompoundHarmonicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5936.OilSealCompoundHarmonicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5938.PartToPartShearCouplingCompoundHarmonicAnalysis]':
        '''List[PartToPartShearCouplingCompoundHarmonicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5938.PartToPartShearCouplingCompoundHarmonicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5943.PlanetCarrierCompoundHarmonicAnalysis]':
        '''List[PlanetCarrierCompoundHarmonicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5943.PlanetCarrierCompoundHarmonicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5944.PointLoadCompoundHarmonicAnalysis]':
        '''List[PointLoadCompoundHarmonicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5944.PointLoadCompoundHarmonicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5945.PowerLoadCompoundHarmonicAnalysis]':
        '''List[PowerLoadCompoundHarmonicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5945.PowerLoadCompoundHarmonicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5954.ShaftHubConnectionCompoundHarmonicAnalysis]':
        '''List[ShaftHubConnectionCompoundHarmonicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5954.ShaftHubConnectionCompoundHarmonicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5947.RingPinsCompoundHarmonicAnalysis]':
        '''List[RingPinsCompoundHarmonicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5947.RingPinsCompoundHarmonicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5949.RollingRingAssemblyCompoundHarmonicAnalysis]':
        '''List[RollingRingAssemblyCompoundHarmonicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5949.RollingRingAssemblyCompoundHarmonicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5953.ShaftCompoundHarmonicAnalysis]':
        '''List[ShaftCompoundHarmonicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5953.ShaftCompoundHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5959.SpiralBevelGearSetCompoundHarmonicAnalysis]':
        '''List[SpiralBevelGearSetCompoundHarmonicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5959.SpiralBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5960.SpringDamperCompoundHarmonicAnalysis]':
        '''List[SpringDamperCompoundHarmonicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5960.SpringDamperCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5965.StraightBevelDiffGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundHarmonicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5965.StraightBevelDiffGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5968.StraightBevelGearSetCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearSetCompoundHarmonicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5968.StraightBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5971.SynchroniserCompoundHarmonicAnalysis]':
        '''List[SynchroniserCompoundHarmonicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5971.SynchroniserCompoundHarmonicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5975.TorqueConverterCompoundHarmonicAnalysis]':
        '''List[TorqueConverterCompoundHarmonicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5975.TorqueConverterCompoundHarmonicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5979.UnbalancedMassCompoundHarmonicAnalysis]':
        '''List[UnbalancedMassCompoundHarmonicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5979.UnbalancedMassCompoundHarmonicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5983.WormGearSetCompoundHarmonicAnalysis]':
        '''List[WormGearSetCompoundHarmonicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5983.WormGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5986.ZerolBevelGearSetCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearSetCompoundHarmonicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5986.ZerolBevelGearSetCompoundHarmonicAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5673.AssemblyHarmonicAnalysis]':
        '''List[AssemblyHarmonicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_5673.AssemblyHarmonicAnalysis))
        return value
