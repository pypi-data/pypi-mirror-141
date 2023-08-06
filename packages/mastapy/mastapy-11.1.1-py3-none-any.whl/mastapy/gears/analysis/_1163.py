'''_1163.py

AbstractGearMeshAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import (
    _1162, _1165, _1166, _1167,
    _1168
)
from mastapy.gears.rating import _321, _325, _328
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.zerol_bevel import _337
from mastapy.gears.rating.worm import _339, _341
from mastapy.gears.rating.straight_bevel_diff import _363
from mastapy.gears.rating.straight_bevel import _367
from mastapy.gears.rating.spiral_bevel import _370
from mastapy.gears.rating.klingelnberg_spiral_bevel import _373
from mastapy.gears.rating.klingelnberg_hypoid import _376
from mastapy.gears.rating.klingelnberg_conical import _379
from mastapy.gears.rating.hypoid import _406
from mastapy.gears.rating.face import _412, _415
from mastapy.gears.rating.cylindrical import _419, _424
from mastapy.gears.rating.conical import _499, _501
from mastapy.gears.rating.concept import _509, _512
from mastapy.gears.rating.bevel import _516
from mastapy.gears.rating.agma_gleason_conical import _527
from mastapy.gears.manufacturing.cylindrical import _573, _577, _578
from mastapy.gears.manufacturing.bevel import (
    _736, _737, _738, _739,
    _749, _750, _755
)
from mastapy.gears.ltca import _801
from mastapy.gears.ltca.cylindrical import _817
from mastapy.gears.ltca.conical import _828
from mastapy.gears.load_case import _834
from mastapy.gears.load_case.worm import _837
from mastapy.gears.load_case.face import _840
from mastapy.gears.load_case.cylindrical import _843
from mastapy.gears.load_case.conical import _846
from mastapy.gears.load_case.concept import _849
from mastapy.gears.load_case.bevel import _852
from mastapy.gears.gear_two_d_fe_analysis import _859, _860
from mastapy.gears.gear_designs.face import _951
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1054, _1055
from mastapy.gears.fe_model import _1146
from mastapy.gears.fe_model.cylindrical import _1150
from mastapy.gears.fe_model.conical import _1153
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_MESH_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'AbstractGearMeshAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractGearMeshAnalysis',)


class AbstractGearMeshAnalysis(_0.APIBase):
    '''AbstractGearMeshAnalysis

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_GEAR_MESH_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractGearMeshAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mesh_name(self) -> 'str':
        '''str: 'MeshName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshName

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def gear_a(self) -> '_1162.AbstractGearAnalysis':
        '''AbstractGearAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1162.AbstractGearAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AbstractGearAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_abstract_gear_rating(self) -> '_321.AbstractGearRating':
        '''AbstractGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _321.AbstractGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AbstractGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_duty_cycle_rating(self) -> '_325.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.GearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_rating(self) -> '_328.GearRating':
        '''GearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _328.GearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_zerol_bevel_gear_rating(self) -> '_337.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.ZerolBevelGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ZerolBevelGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_gear_duty_cycle_rating(self) -> '_339.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _339.WormGearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_gear_rating(self) -> '_341.WormGearRating':
        '''WormGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _341.WormGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_straight_bevel_diff_gear_rating(self) -> '_363.StraightBevelDiffGearRating':
        '''StraightBevelDiffGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _363.StraightBevelDiffGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelDiffGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_straight_bevel_gear_rating(self) -> '_367.StraightBevelGearRating':
        '''StraightBevelGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _367.StraightBevelGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_spiral_bevel_gear_rating(self) -> '_370.SpiralBevelGearRating':
        '''SpiralBevelGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _370.SpiralBevelGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to SpiralBevelGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(self) -> '_373.KlingelnbergCycloPalloidSpiralBevelGearRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _373.KlingelnbergCycloPalloidSpiralBevelGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidSpiralBevelGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear_rating(self) -> '_376.KlingelnbergCycloPalloidHypoidGearRating':
        '''KlingelnbergCycloPalloidHypoidGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _376.KlingelnbergCycloPalloidHypoidGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidHypoidGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_conical_gear_rating(self) -> '_379.KlingelnbergCycloPalloidConicalGearRating':
        '''KlingelnbergCycloPalloidConicalGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _379.KlingelnbergCycloPalloidConicalGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidConicalGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_hypoid_gear_rating(self) -> '_406.HypoidGearRating':
        '''HypoidGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _406.HypoidGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to HypoidGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_duty_cycle_rating(self) -> '_412.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _412.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_rating(self) -> '_415.FaceGearRating':
        '''FaceGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _415.FaceGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_419.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _419.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_rating(self) -> '_424.CylindricalGearRating':
        '''CylindricalGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _424.CylindricalGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_duty_cycle_rating(self) -> '_499.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_rating(self) -> '_501.ConicalGearRating':
        '''ConicalGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.ConicalGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_concept_gear_duty_cycle_rating(self) -> '_509.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_concept_gear_rating(self) -> '_512.ConceptGearRating':
        '''ConceptGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _512.ConceptGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_bevel_gear_rating(self) -> '_516.BevelGearRating':
        '''BevelGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _516.BevelGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_agma_gleason_conical_gear_rating(self) -> '_527.AGMAGleasonConicalGearRating':
        '''AGMAGleasonConicalGearRating: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _527.AGMAGleasonConicalGearRating.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AGMAGleasonConicalGearRating. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_manufacturing_config(self) -> '_573.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _573.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_577.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _577.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_load_case(self) -> '_578.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _578.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_analysis(self) -> '_736.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_config(self) -> '_737.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _737.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config(self) -> '_738.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _738.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config_base(self) -> '_739.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _739.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_pinion_manufacturing_config(self) -> '_749.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_pinion_micro_geometry_config(self) -> '_750.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _750.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_wheel_manufacturing_config(self) -> '_755.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _755.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_load_distribution_analysis(self) -> '_801.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _801.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_817.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _817.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_load_distribution_analysis(self) -> '_828.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _828.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_load_case_base(self) -> '_834.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _834.GearLoadCaseBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_worm_gear_load_case(self) -> '_837.WormGearLoadCase':
        '''WormGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _837.WormGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_load_case(self) -> '_840.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _840.FaceGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_load_case(self) -> '_843.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _843.CylindricalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_load_case(self) -> '_846.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _846.ConicalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_concept_gear_load_case(self) -> '_849.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _849.ConceptGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_bevel_load_case(self) -> '_852.BevelLoadCase':
        '''BevelLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _852.BevelLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_tiff_analysis(self) -> '_859.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _859.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_tiff_analysis_duty_cycle(self) -> '_860.CylindricalGearTIFFAnalysisDutyCycle':
        '''CylindricalGearTIFFAnalysisDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _860.CylindricalGearTIFFAnalysisDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearTIFFAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_face_gear_micro_geometry(self) -> '_951.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _951.FaceGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry(self) -> '_1054.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1054.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_1055.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1055.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_fe_model(self) -> '_1146.GearFEModel':
        '''GearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1146.GearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_cylindrical_gear_fe_model(self) -> '_1150.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1150.CylindricalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_conical_gear_fe_model(self) -> '_1153.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1153.ConicalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_design_analysis(self) -> '_1165.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1165.GearDesignAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearDesignAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_implementation_analysis(self) -> '_1166.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1166.GearImplementationAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_implementation_analysis_duty_cycle(self) -> '_1167.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1167.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_a_of_type_gear_implementation_detail(self) -> '_1168.GearImplementationDetail':
        '''GearImplementationDetail: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1168.GearImplementationDetail.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearA.__class__)(self.wrapped.GearA) if self.wrapped.GearA is not None else None

    @property
    def gear_b(self) -> '_1162.AbstractGearAnalysis':
        '''AbstractGearAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1162.AbstractGearAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AbstractGearAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_abstract_gear_rating(self) -> '_321.AbstractGearRating':
        '''AbstractGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _321.AbstractGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AbstractGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_duty_cycle_rating(self) -> '_325.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.GearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_rating(self) -> '_328.GearRating':
        '''GearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _328.GearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_zerol_bevel_gear_rating(self) -> '_337.ZerolBevelGearRating':
        '''ZerolBevelGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _337.ZerolBevelGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ZerolBevelGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_gear_duty_cycle_rating(self) -> '_339.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _339.WormGearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_gear_rating(self) -> '_341.WormGearRating':
        '''WormGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _341.WormGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_straight_bevel_diff_gear_rating(self) -> '_363.StraightBevelDiffGearRating':
        '''StraightBevelDiffGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _363.StraightBevelDiffGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelDiffGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_straight_bevel_gear_rating(self) -> '_367.StraightBevelGearRating':
        '''StraightBevelGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _367.StraightBevelGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_spiral_bevel_gear_rating(self) -> '_370.SpiralBevelGearRating':
        '''SpiralBevelGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _370.SpiralBevelGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to SpiralBevelGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(self) -> '_373.KlingelnbergCycloPalloidSpiralBevelGearRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _373.KlingelnbergCycloPalloidSpiralBevelGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidSpiralBevelGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear_rating(self) -> '_376.KlingelnbergCycloPalloidHypoidGearRating':
        '''KlingelnbergCycloPalloidHypoidGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _376.KlingelnbergCycloPalloidHypoidGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidHypoidGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_conical_gear_rating(self) -> '_379.KlingelnbergCycloPalloidConicalGearRating':
        '''KlingelnbergCycloPalloidConicalGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _379.KlingelnbergCycloPalloidConicalGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidConicalGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_hypoid_gear_rating(self) -> '_406.HypoidGearRating':
        '''HypoidGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _406.HypoidGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to HypoidGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_duty_cycle_rating(self) -> '_412.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _412.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_rating(self) -> '_415.FaceGearRating':
        '''FaceGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _415.FaceGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_419.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _419.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_rating(self) -> '_424.CylindricalGearRating':
        '''CylindricalGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _424.CylindricalGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_duty_cycle_rating(self) -> '_499.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_rating(self) -> '_501.ConicalGearRating':
        '''ConicalGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _501.ConicalGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_concept_gear_duty_cycle_rating(self) -> '_509.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_concept_gear_rating(self) -> '_512.ConceptGearRating':
        '''ConceptGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _512.ConceptGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_bevel_gear_rating(self) -> '_516.BevelGearRating':
        '''BevelGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _516.BevelGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_agma_gleason_conical_gear_rating(self) -> '_527.AGMAGleasonConicalGearRating':
        '''AGMAGleasonConicalGearRating: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _527.AGMAGleasonConicalGearRating.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AGMAGleasonConicalGearRating. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_manufacturing_config(self) -> '_573.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _573.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_577.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _577.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_load_case(self) -> '_578.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _578.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_analysis(self) -> '_736.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_config(self) -> '_737.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _737.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config(self) -> '_738.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _738.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config_base(self) -> '_739.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _739.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_pinion_manufacturing_config(self) -> '_749.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_pinion_micro_geometry_config(self) -> '_750.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _750.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_wheel_manufacturing_config(self) -> '_755.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _755.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_load_distribution_analysis(self) -> '_801.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _801.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_817.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _817.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_load_distribution_analysis(self) -> '_828.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _828.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_load_case_base(self) -> '_834.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _834.GearLoadCaseBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_worm_gear_load_case(self) -> '_837.WormGearLoadCase':
        '''WormGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _837.WormGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_load_case(self) -> '_840.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _840.FaceGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_load_case(self) -> '_843.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _843.CylindricalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_load_case(self) -> '_846.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _846.ConicalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_concept_gear_load_case(self) -> '_849.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _849.ConceptGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_bevel_load_case(self) -> '_852.BevelLoadCase':
        '''BevelLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _852.BevelLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_tiff_analysis(self) -> '_859.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _859.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_tiff_analysis_duty_cycle(self) -> '_860.CylindricalGearTIFFAnalysisDutyCycle':
        '''CylindricalGearTIFFAnalysisDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _860.CylindricalGearTIFFAnalysisDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearTIFFAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_face_gear_micro_geometry(self) -> '_951.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _951.FaceGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry(self) -> '_1054.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1054.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_1055.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1055.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_fe_model(self) -> '_1146.GearFEModel':
        '''GearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1146.GearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_cylindrical_gear_fe_model(self) -> '_1150.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1150.CylindricalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_conical_gear_fe_model(self) -> '_1153.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1153.ConicalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_design_analysis(self) -> '_1165.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1165.GearDesignAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearDesignAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_implementation_analysis(self) -> '_1166.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1166.GearImplementationAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_implementation_analysis_duty_cycle(self) -> '_1167.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1167.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def gear_b_of_type_gear_implementation_detail(self) -> '_1168.GearImplementationDetail':
        '''GearImplementationDetail: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1168.GearImplementationDetail.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearB.__class__)(self.wrapped.GearB) if self.wrapped.GearB is not None else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
