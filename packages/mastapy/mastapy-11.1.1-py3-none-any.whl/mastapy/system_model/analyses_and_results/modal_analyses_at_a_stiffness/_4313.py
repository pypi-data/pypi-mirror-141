'''_4313.py

AssemblyModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2179, _2218
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6536, _6669
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4314, _4316, _4319, _4326,
    _4325, _4329, _4334, _4337,
    _4347, _4349, _4351, _4355,
    _4362, _4363, _4364, _4371,
    _4378, _4381, _4382, _4383,
    _4385, _4389, _4392, _4393,
    _4394, _4402, _4396, _4398,
    _4403, _4408, _4411, _4414,
    _4417, _4421, _4425, _4428,
    _4432, _4435, _4306
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'AssemblyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysisAtAStiffness',)


class AssemblyModalAnalysisAtAStiffness(_4306.AbstractAssemblyModalAnalysisAtAStiffness):
    '''AssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysisAtAStiffness.TYPE'):
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
    def bearings(self) -> 'List[_4314.BearingModalAnalysisAtAStiffness]':
        '''List[BearingModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4314.BearingModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4316.BeltDriveModalAnalysisAtAStiffness]':
        '''List[BeltDriveModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4316.BeltDriveModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4319.BevelDifferentialGearSetModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4319.BevelDifferentialGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4326.BoltModalAnalysisAtAStiffness]':
        '''List[BoltModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4326.BoltModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4325.BoltedJointModalAnalysisAtAStiffness]':
        '''List[BoltedJointModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4325.BoltedJointModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4329.ClutchModalAnalysisAtAStiffness]':
        '''List[ClutchModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4329.ClutchModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4334.ConceptCouplingModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4334.ConceptCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4337.ConceptGearSetModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4337.ConceptGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4347.CVTModalAnalysisAtAStiffness]':
        '''List[CVTModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4347.CVTModalAnalysisAtAStiffness))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_4349.CycloidalAssemblyModalAnalysisAtAStiffness]':
        '''List[CycloidalAssemblyModalAnalysisAtAStiffness]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_4349.CycloidalAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_4351.CycloidalDiscModalAnalysisAtAStiffness]':
        '''List[CycloidalDiscModalAnalysisAtAStiffness]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_4351.CycloidalDiscModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4355.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4355.CylindricalGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4362.FaceGearSetModalAnalysisAtAStiffness]':
        '''List[FaceGearSetModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4362.FaceGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def fe_parts(self) -> 'List[_4363.FEPartModalAnalysisAtAStiffness]':
        '''List[FEPartModalAnalysisAtAStiffness]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_4363.FEPartModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4364.FlexiblePinAssemblyModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4364.FlexiblePinAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4371.HypoidGearSetModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4371.HypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4378.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4378.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4381.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4381.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4382.MassDiscModalAnalysisAtAStiffness]':
        '''List[MassDiscModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4382.MassDiscModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4383.MeasurementComponentModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4383.MeasurementComponentModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4385.OilSealModalAnalysisAtAStiffness]':
        '''List[OilSealModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4385.OilSealModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4389.PartToPartShearCouplingModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4389.PartToPartShearCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4392.PlanetCarrierModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4392.PlanetCarrierModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4393.PointLoadModalAnalysisAtAStiffness]':
        '''List[PointLoadModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4393.PointLoadModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4394.PowerLoadModalAnalysisAtAStiffness]':
        '''List[PowerLoadModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4394.PowerLoadModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4402.ShaftHubConnectionModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4402.ShaftHubConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def ring_pins(self) -> 'List[_4396.RingPinsModalAnalysisAtAStiffness]':
        '''List[RingPinsModalAnalysisAtAStiffness]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_4396.RingPinsModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4398.RollingRingAssemblyModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4398.RollingRingAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4403.ShaftModalAnalysisAtAStiffness]':
        '''List[ShaftModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4403.ShaftModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4408.SpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4408.SpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4411.SpringDamperModalAnalysisAtAStiffness]':
        '''List[SpringDamperModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4411.SpringDamperModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4414.StraightBevelDiffGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4414.StraightBevelDiffGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4417.StraightBevelGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4417.StraightBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4421.SynchroniserModalAnalysisAtAStiffness]':
        '''List[SynchroniserModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4421.SynchroniserModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4425.TorqueConverterModalAnalysisAtAStiffness]':
        '''List[TorqueConverterModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4425.TorqueConverterModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4428.UnbalancedMassModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4428.UnbalancedMassModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4432.WormGearSetModalAnalysisAtAStiffness]':
        '''List[WormGearSetModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4432.WormGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4435.ZerolBevelGearSetModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4435.ZerolBevelGearSetModalAnalysisAtAStiffness))
        return value
