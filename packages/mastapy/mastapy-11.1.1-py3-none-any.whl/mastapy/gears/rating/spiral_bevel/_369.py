'''_369.py

SpiralBevelGearMeshRating
'''


from typing import List

from mastapy.gears.gear_designs.spiral_bevel import _928
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.spiral_bevel import _370
from mastapy.gears.rating.bevel import _515
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.SpiralBevel', 'SpiralBevelGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshRating',)


class SpiralBevelGearMeshRating(_515.BevelGearMeshRating):
    '''SpiralBevelGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def spiral_bevel_gear_mesh(self) -> '_928.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'SpiralBevelGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_928.SpiralBevelGearMeshDesign)(self.wrapped.SpiralBevelGearMesh) if self.wrapped.SpiralBevelGearMesh is not None else None

    @property
    def spiral_bevel_gear_ratings(self) -> 'List[_370.SpiralBevelGearRating]':
        '''List[SpiralBevelGearRating]: 'SpiralBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearRatings, constructor.new(_370.SpiralBevelGearRating))
        return value
