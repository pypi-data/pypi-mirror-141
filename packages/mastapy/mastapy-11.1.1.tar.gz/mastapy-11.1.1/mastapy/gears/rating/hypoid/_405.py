'''_405.py

HypoidGearMeshRating
'''


from typing import List

from mastapy.gears.rating.iso_10300 import _392, _391
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.hypoid.standards import _410
from mastapy.gears.gear_designs.hypoid import _944
from mastapy.gears.rating.conical import _506
from mastapy.gears.rating.hypoid import _406
from mastapy.gears.rating.agma_gleason_conical import _526
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid', 'HypoidGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshRating',)


class HypoidGearMeshRating(_526.AGMAGleasonConicalGearMeshRating):
    '''HypoidGearMeshRating

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b1(self) -> '_392.ISO10300MeshSingleFlankRatingMethodB1':
        '''ISO10300MeshSingleFlankRatingMethodB1: 'ISO10300HypoidMeshSingleFlankRatingMethodB1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_392.ISO10300MeshSingleFlankRatingMethodB1)(self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB1) if self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB1 is not None else None

    @property
    def iso10300_hypoid_mesh_single_flank_rating_method_b2(self) -> '_391.Iso10300MeshSingleFlankRatingHypoidMethodB2':
        '''Iso10300MeshSingleFlankRatingHypoidMethodB2: 'ISO10300HypoidMeshSingleFlankRatingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_391.Iso10300MeshSingleFlankRatingHypoidMethodB2)(self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB2) if self.wrapped.ISO10300HypoidMeshSingleFlankRatingMethodB2 is not None else None

    @property
    def gleason_hypoid_mesh_single_flank_rating(self) -> '_410.GleasonHypoidMeshSingleFlankRating':
        '''GleasonHypoidMeshSingleFlankRating: 'GleasonHypoidMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_410.GleasonHypoidMeshSingleFlankRating)(self.wrapped.GleasonHypoidMeshSingleFlankRating) if self.wrapped.GleasonHypoidMeshSingleFlankRating is not None else None

    @property
    def hypoid_gear_mesh(self) -> '_944.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'HypoidGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_944.HypoidGearMeshDesign)(self.wrapped.HypoidGearMesh) if self.wrapped.HypoidGearMesh is not None else None

    @property
    def meshed_gears(self) -> 'List[_506.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_506.ConicalMeshedGearRating))
        return value

    @property
    def gears_in_mesh(self) -> 'List[_506.ConicalMeshedGearRating]':
        '''List[ConicalMeshedGearRating]: 'GearsInMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsInMesh, constructor.new(_506.ConicalMeshedGearRating))
        return value

    @property
    def hypoid_gear_ratings(self) -> 'List[_406.HypoidGearRating]':
        '''List[HypoidGearRating]: 'HypoidGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearRatings, constructor.new(_406.HypoidGearRating))
        return value
