'''_7133.py

AssemblyCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7000
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7134, _7136, _7139, _7145,
    _7146, _7147, _7152, _7157,
    _7167, _7169, _7171, _7175,
    _7181, _7182, _7183, _7190,
    _7197, _7200, _7201, _7202,
    _7204, _7206, _7211, _7212,
    _7213, _7222, _7215, _7217,
    _7221, _7227, _7228, _7233,
    _7236, _7239, _7243, _7247,
    _7251, _7254, _7126
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AssemblyCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundAdvancedSystemDeflection',)


class AssemblyCompoundAdvancedSystemDeflection(_7126.AbstractAssemblyCompoundAdvancedSystemDeflection):
    '''AssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundAdvancedSystemDeflection.TYPE'):
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
    def assembly_analysis_cases_ready(self) -> 'List[_7000.AssemblyAdvancedSystemDeflection]':
        '''List[AssemblyAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_7000.AssemblyAdvancedSystemDeflection))
        return value

    @property
    def bearings(self) -> 'List[_7134.BearingCompoundAdvancedSystemDeflection]':
        '''List[BearingCompoundAdvancedSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_7134.BearingCompoundAdvancedSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_7136.BeltDriveCompoundAdvancedSystemDeflection]':
        '''List[BeltDriveCompoundAdvancedSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_7136.BeltDriveCompoundAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_7139.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetCompoundAdvancedSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_7139.BevelDifferentialGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_7145.BoltCompoundAdvancedSystemDeflection]':
        '''List[BoltCompoundAdvancedSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_7145.BoltCompoundAdvancedSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_7146.BoltedJointCompoundAdvancedSystemDeflection]':
        '''List[BoltedJointCompoundAdvancedSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_7146.BoltedJointCompoundAdvancedSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_7147.ClutchCompoundAdvancedSystemDeflection]':
        '''List[ClutchCompoundAdvancedSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_7147.ClutchCompoundAdvancedSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_7152.ConceptCouplingCompoundAdvancedSystemDeflection]':
        '''List[ConceptCouplingCompoundAdvancedSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_7152.ConceptCouplingCompoundAdvancedSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_7157.ConceptGearSetCompoundAdvancedSystemDeflection]':
        '''List[ConceptGearSetCompoundAdvancedSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_7157.ConceptGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_7167.CVTCompoundAdvancedSystemDeflection]':
        '''List[CVTCompoundAdvancedSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_7167.CVTCompoundAdvancedSystemDeflection))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_7169.CycloidalAssemblyCompoundAdvancedSystemDeflection]':
        '''List[CycloidalAssemblyCompoundAdvancedSystemDeflection]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_7169.CycloidalAssemblyCompoundAdvancedSystemDeflection))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_7171.CycloidalDiscCompoundAdvancedSystemDeflection]':
        '''List[CycloidalDiscCompoundAdvancedSystemDeflection]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_7171.CycloidalDiscCompoundAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_7175.CylindricalGearSetCompoundAdvancedSystemDeflection]':
        '''List[CylindricalGearSetCompoundAdvancedSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_7175.CylindricalGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_7181.FaceGearSetCompoundAdvancedSystemDeflection]':
        '''List[FaceGearSetCompoundAdvancedSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_7181.FaceGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def fe_parts(self) -> 'List[_7182.FEPartCompoundAdvancedSystemDeflection]':
        '''List[FEPartCompoundAdvancedSystemDeflection]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_7182.FEPartCompoundAdvancedSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_7183.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]':
        '''List[FlexiblePinAssemblyCompoundAdvancedSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_7183.FlexiblePinAssemblyCompoundAdvancedSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_7190.HypoidGearSetCompoundAdvancedSystemDeflection]':
        '''List[HypoidGearSetCompoundAdvancedSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_7190.HypoidGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_7197.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_7197.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_7200.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_7200.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_7201.MassDiscCompoundAdvancedSystemDeflection]':
        '''List[MassDiscCompoundAdvancedSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_7201.MassDiscCompoundAdvancedSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_7202.MeasurementComponentCompoundAdvancedSystemDeflection]':
        '''List[MeasurementComponentCompoundAdvancedSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_7202.MeasurementComponentCompoundAdvancedSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_7204.OilSealCompoundAdvancedSystemDeflection]':
        '''List[OilSealCompoundAdvancedSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_7204.OilSealCompoundAdvancedSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_7206.PartToPartShearCouplingCompoundAdvancedSystemDeflection]':
        '''List[PartToPartShearCouplingCompoundAdvancedSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_7206.PartToPartShearCouplingCompoundAdvancedSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_7211.PlanetCarrierCompoundAdvancedSystemDeflection]':
        '''List[PlanetCarrierCompoundAdvancedSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_7211.PlanetCarrierCompoundAdvancedSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_7212.PointLoadCompoundAdvancedSystemDeflection]':
        '''List[PointLoadCompoundAdvancedSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_7212.PointLoadCompoundAdvancedSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_7213.PowerLoadCompoundAdvancedSystemDeflection]':
        '''List[PowerLoadCompoundAdvancedSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_7213.PowerLoadCompoundAdvancedSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_7222.ShaftHubConnectionCompoundAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionCompoundAdvancedSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_7222.ShaftHubConnectionCompoundAdvancedSystemDeflection))
        return value

    @property
    def ring_pins(self) -> 'List[_7215.RingPinsCompoundAdvancedSystemDeflection]':
        '''List[RingPinsCompoundAdvancedSystemDeflection]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_7215.RingPinsCompoundAdvancedSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_7217.RollingRingAssemblyCompoundAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyCompoundAdvancedSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_7217.RollingRingAssemblyCompoundAdvancedSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_7221.ShaftCompoundAdvancedSystemDeflection]':
        '''List[ShaftCompoundAdvancedSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_7221.ShaftCompoundAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_7227.SpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[SpiralBevelGearSetCompoundAdvancedSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_7227.SpiralBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_7228.SpringDamperCompoundAdvancedSystemDeflection]':
        '''List[SpringDamperCompoundAdvancedSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_7228.SpringDamperCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_7233.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_7233.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_7236.StraightBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetCompoundAdvancedSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_7236.StraightBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_7239.SynchroniserCompoundAdvancedSystemDeflection]':
        '''List[SynchroniserCompoundAdvancedSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_7239.SynchroniserCompoundAdvancedSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_7243.TorqueConverterCompoundAdvancedSystemDeflection]':
        '''List[TorqueConverterCompoundAdvancedSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_7243.TorqueConverterCompoundAdvancedSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_7247.UnbalancedMassCompoundAdvancedSystemDeflection]':
        '''List[UnbalancedMassCompoundAdvancedSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_7247.UnbalancedMassCompoundAdvancedSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_7251.WormGearSetCompoundAdvancedSystemDeflection]':
        '''List[WormGearSetCompoundAdvancedSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_7251.WormGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_7254.ZerolBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetCompoundAdvancedSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_7254.ZerolBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_7000.AssemblyAdvancedSystemDeflection]':
        '''List[AssemblyAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_7000.AssemblyAdvancedSystemDeflection))
        return value
