'''_4443.py

AssemblyCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4313
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _4444, _4446, _4449, _4455,
    _4456, _4457, _4462, _4467,
    _4477, _4479, _4481, _4485,
    _4491, _4492, _4493, _4500,
    _4507, _4510, _4511, _4512,
    _4514, _4516, _4521, _4522,
    _4523, _4532, _4525, _4527,
    _4531, _4537, _4538, _4543,
    _4546, _4549, _4553, _4557,
    _4561, _4564, _4436
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'AssemblyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtAStiffness',)


class AssemblyCompoundModalAnalysisAtAStiffness(_4436.AbstractAssemblyCompoundModalAnalysisAtAStiffness):
    '''AssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtAStiffness.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_4313.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_4313.AssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def bearings(self) -> 'List[_4444.BearingCompoundModalAnalysisAtAStiffness]':
        '''List[BearingCompoundModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4444.BearingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4446.BeltDriveCompoundModalAnalysisAtAStiffness]':
        '''List[BeltDriveCompoundModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4446.BeltDriveCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4449.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4449.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4455.BoltCompoundModalAnalysisAtAStiffness]':
        '''List[BoltCompoundModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4455.BoltCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4456.BoltedJointCompoundModalAnalysisAtAStiffness]':
        '''List[BoltedJointCompoundModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4456.BoltedJointCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4457.ClutchCompoundModalAnalysisAtAStiffness]':
        '''List[ClutchCompoundModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4457.ClutchCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4462.ConceptCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingCompoundModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4462.ConceptCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4467.ConceptGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetCompoundModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4467.ConceptGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4477.CVTCompoundModalAnalysisAtAStiffness]':
        '''List[CVTCompoundModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4477.CVTCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4479.CycloidalAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[CycloidalAssemblyCompoundModalAnalysisAtAStiffness]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4479.CycloidalAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4481.CycloidalDiscCompoundModalAnalysisAtAStiffness]':
        '''List[CycloidalDiscCompoundModalAnalysisAtAStiffness]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4481.CycloidalDiscCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4485.CylindricalGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetCompoundModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4485.CylindricalGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4491.FaceGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[FaceGearSetCompoundModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4491.FaceGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def fe_parts(self) -> 'List[_4492.FEPartCompoundModalAnalysisAtAStiffness]':
        '''List[FEPartCompoundModalAnalysisAtAStiffness]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4492.FEPartCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4493.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4493.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4500.HypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetCompoundModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4500.HypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4507.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4507.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4510.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4510.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4511.MassDiscCompoundModalAnalysisAtAStiffness]':
        '''List[MassDiscCompoundModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4511.MassDiscCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4512.MeasurementComponentCompoundModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentCompoundModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4512.MeasurementComponentCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4514.OilSealCompoundModalAnalysisAtAStiffness]':
        '''List[OilSealCompoundModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4514.OilSealCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4516.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4516.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4521.PlanetCarrierCompoundModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierCompoundModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4521.PlanetCarrierCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4522.PointLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PointLoadCompoundModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4522.PointLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4523.PowerLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PowerLoadCompoundModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4523.PowerLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4532.ShaftHubConnectionCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4532.ShaftHubConnectionCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def ring_pins(self) -> 'List[_4525.RingPinsCompoundModalAnalysisAtAStiffness]':
        '''List[RingPinsCompoundModalAnalysisAtAStiffness]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4525.RingPinsCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4527.RollingRingAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyCompoundModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4527.RollingRingAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4531.ShaftCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftCompoundModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4531.ShaftCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4537.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4537.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4538.SpringDamperCompoundModalAnalysisAtAStiffness]':
        '''List[SpringDamperCompoundModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4538.SpringDamperCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4543.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4543.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4546.StraightBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4546.StraightBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4549.SynchroniserCompoundModalAnalysisAtAStiffness]':
        '''List[SynchroniserCompoundModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4549.SynchroniserCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4553.TorqueConverterCompoundModalAnalysisAtAStiffness]':
        '''List[TorqueConverterCompoundModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4553.TorqueConverterCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4557.UnbalancedMassCompoundModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassCompoundModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4557.UnbalancedMassCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4561.WormGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[WormGearSetCompoundModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4561.WormGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4564.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4564.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4313.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_4313.AssemblyModalAnalysisAtAStiffness))
        return value
