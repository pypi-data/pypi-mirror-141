'''_372.py

KlingelnbergCycloPalloidSpiralBevelGearMeshRating
'''


from typing import List

from mastapy.gears.rating.klingelnberg_conical.kn3030 import _386
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _932
from mastapy.gears.rating.klingelnberg_spiral_bevel import _373
from mastapy.gears.rating.klingelnberg_conical import _378
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergSpiralBevel', 'KlingelnbergCycloPalloidSpiralBevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshRating',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshRating(_378.KlingelnbergCycloPalloidConicalGearMeshRating):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def kn3030_klingelnberg_mesh_single_flank_rating(self) -> '_386.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating':
        '''KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating: 'KN3030KlingelnbergMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_386.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating)(self.wrapped.KN3030KlingelnbergMeshSingleFlankRating) if self.wrapped.KN3030KlingelnbergMeshSingleFlankRating is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_932.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'KlingelnbergCycloPalloidSpiralBevelGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_932.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign)(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearMesh) if self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearMesh is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_ratings(self) -> 'List[_373.KlingelnbergCycloPalloidSpiralBevelGearRating]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearRating]: 'KlingelnbergCycloPalloidSpiralBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearRatings, constructor.new(_373.KlingelnbergCycloPalloidSpiralBevelGearRating))
        return value
