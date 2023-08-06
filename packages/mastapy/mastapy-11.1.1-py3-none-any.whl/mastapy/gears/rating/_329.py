'''_329.py

GearSetDutyCycleRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs import _908
from mastapy.gears.gear_designs.zerol_bevel import _912
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _917
from mastapy.gears.gear_designs.straight_bevel_diff import _921
from mastapy.gears.gear_designs.straight_bevel import _925
from mastapy.gears.gear_designs.spiral_bevel import _929
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _933
from mastapy.gears.gear_designs.klingelnberg_hypoid import _937
from mastapy.gears.gear_designs.klingelnberg_conical import _941
from mastapy.gears.gear_designs.hypoid import _945
from mastapy.gears.gear_designs.face import _953
from mastapy.gears.gear_designs.cylindrical import _985, _996
from mastapy.gears.gear_designs.conical import _1105
from mastapy.gears.gear_designs.concept import _1127
from mastapy.gears.gear_designs.bevel import _1131
from mastapy.gears.gear_designs.agma_gleason_conical import _1144
from mastapy.gears.rating import _325, _332, _322
from mastapy._internal.python_net import python_net_import

_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDutyCycleRating',)


class GearSetDutyCycleRating(_322.AbstractGearSetRating):
    '''GearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    @property
    def total_duty_cycle_gear_set_reliability(self) -> 'float':
        '''float: 'TotalDutyCycleGearSetReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDutyCycleGearSetReliability

    @property
    def duty_cycle_name(self) -> 'str':
        '''str: 'DutyCycleName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DutyCycleName

    @property
    def gear_set_design(self) -> '_908.GearSetDesign':
        '''GearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.GearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to GearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_912.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.ZerolBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_worm_gear_set_design(self) -> '_917.WormGearSetDesign':
        '''WormGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.WormGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to WormGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_921.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.StraightBevelDiffGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_925.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.StraightBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_929.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _929.SpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_933.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _933.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_937.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_klingelnberg_conical_gear_set_design(self) -> '_941.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.KlingelnbergConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_hypoid_gear_set_design(self) -> '_945.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _945.HypoidGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_face_gear_set_design(self) -> '_953.FaceGearSetDesign':
        '''FaceGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _953.FaceGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to FaceGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_cylindrical_gear_set_design(self) -> '_985.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _985.CylindricalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_cylindrical_planetary_gear_set_design(self) -> '_996.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _996.CylindricalPlanetaryGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_conical_gear_set_design(self) -> '_1105.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1105.ConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_concept_gear_set_design(self) -> '_1127.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1127.ConceptGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to ConceptGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_bevel_gear_set_design(self) -> '_1131.BevelGearSetDesign':
        '''BevelGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1131.BevelGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to BevelGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_set_design_of_type_agma_gleason_conical_gear_set_design(self) -> '_1144.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'GearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1144.AGMAGleasonConicalGearSetDesign.TYPE not in self.wrapped.GearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.wrapped.GearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearSetDesign.__class__)(self.wrapped.GearSetDesign) if self.wrapped.GearSetDesign is not None else None

    @property
    def gear_ratings(self) -> 'List[_325.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_325.GearDutyCycleRating))
        return value

    @property
    def gear_duty_cycle_ratings(self) -> 'List[_325.GearDutyCycleRating]':
        '''List[GearDutyCycleRating]: 'GearDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearDutyCycleRatings, constructor.new(_325.GearDutyCycleRating))
        return value

    @property
    def gear_mesh_ratings(self) -> 'List[_332.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshRatings, constructor.new(_332.MeshDutyCycleRating))
        return value

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_332.MeshDutyCycleRating]':
        '''List[MeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshDutyCycleRatings, constructor.new(_332.MeshDutyCycleRating))
        return value

    def set_face_widths_for_specified_safety_factors(self):
        ''' 'SetFaceWidthsForSpecifiedSafetyFactors' is the original name of this method.'''

        self.wrapped.SetFaceWidthsForSpecifiedSafetyFactors()
