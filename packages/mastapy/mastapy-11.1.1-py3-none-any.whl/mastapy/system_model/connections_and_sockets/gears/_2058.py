'''_2058.py

GearMesh
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs import _907
from mastapy.gears.gear_designs.zerol_bevel import _911
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _916
from mastapy.gears.gear_designs.straight_bevel_diff import _920
from mastapy.gears.gear_designs.straight_bevel import _924
from mastapy.gears.gear_designs.spiral_bevel import _928
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _932
from mastapy.gears.gear_designs.klingelnberg_hypoid import _936
from mastapy.gears.gear_designs.klingelnberg_conical import _940
from mastapy.gears.gear_designs.hypoid import _944
from mastapy.gears.gear_designs.face import _949
from mastapy.gears.gear_designs.cylindrical import _977
from mastapy.gears.gear_designs.conical import _1104
from mastapy.gears.gear_designs.concept import _1126
from mastapy.gears.gear_designs.bevel import _1130
from mastapy.gears.gear_designs.agma_gleason_conical import _1143
from mastapy.system_model.connections_and_sockets import _2026
from mastapy._internal.python_net import python_net_import

_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMesh',)


class GearMesh(_2026.InterMountableComponentConnection):
    '''GearMesh

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def user_specified_mesh_stiffness(self) -> 'float':
        '''float: 'UserSpecifiedMeshStiffness' is the original name of this property.'''

        return self.wrapped.UserSpecifiedMeshStiffness

    @user_specified_mesh_stiffness.setter
    def user_specified_mesh_stiffness(self, value: 'float'):
        self.wrapped.UserSpecifiedMeshStiffness = float(value) if value else 0.0

    @property
    def use_specified_mesh_stiffness(self) -> 'bool':
        '''bool: 'UseSpecifiedMeshStiffness' is the original name of this property.'''

        return self.wrapped.UseSpecifiedMeshStiffness

    @use_specified_mesh_stiffness.setter
    def use_specified_mesh_stiffness(self, value: 'bool'):
        self.wrapped.UseSpecifiedMeshStiffness = bool(value) if value else False

    @property
    def mesh_efficiency(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MeshEfficiency' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MeshEfficiency) if self.wrapped.MeshEfficiency is not None else None

    @mesh_efficiency.setter
    def mesh_efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MeshEfficiency = value

    @property
    def active_gear_mesh_design(self) -> '_907.GearMeshDesign':
        '''GearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _907.GearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to GearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_zerol_bevel_gear_mesh_design(self) -> '_911.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _911.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_worm_gear_mesh_design(self) -> '_916.WormGearMeshDesign':
        '''WormGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _916.WormGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to WormGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_920.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _920.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_straight_bevel_gear_mesh_design(self) -> '_924.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.StraightBevelGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_spiral_bevel_gear_mesh_design(self) -> '_928.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _928.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_932.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _932.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_936.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _936.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_940.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _940.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_hypoid_gear_mesh_design(self) -> '_944.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _944.HypoidGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_face_gear_mesh_design(self) -> '_949.FaceGearMeshDesign':
        '''FaceGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _949.FaceGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to FaceGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_cylindrical_gear_mesh_design(self) -> '_977.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _977.CylindricalGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to CylindricalGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_conical_gear_mesh_design(self) -> '_1104.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1104.ConicalGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_concept_gear_mesh_design(self) -> '_1126.ConceptGearMeshDesign':
        '''ConceptGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1126.ConceptGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to ConceptGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_bevel_gear_mesh_design(self) -> '_1130.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1130.BevelGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None

    @property
    def active_gear_mesh_design_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_1143.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'ActiveGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1143.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.ActiveGearMeshDesign.__class__.__mro__:
            raise CastException('Failed to cast active_gear_mesh_design to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.ActiveGearMeshDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ActiveGearMeshDesign.__class__)(self.wrapped.ActiveGearMeshDesign) if self.wrapped.ActiveGearMeshDesign is not None else None
