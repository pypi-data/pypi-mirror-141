'''_2017.py

Connection
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _2041, _2011, _2012, _2019,
    _2021, _2023, _2024, _2025,
    _2027, _2028, _2029, _2030,
    _2031, _2033, _2034, _2035,
    _2038, _2039
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2045, _2047, _2049, _2051,
    _2053, _2055, _2057, _2059,
    _2061, _2062, _2066, _2067,
    _2069, _2071, _2073, _2075,
    _2077
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2078, _2079, _2081, _2082,
    _2084, _2085
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2088, _2090, _2092, _2094,
    _2096, _2098, _2099
)
from mastapy.system_model.part_model import (
    _2189, _2181, _2182, _2185,
    _2187, _2192, _2193, _2196,
    _2197, _2199, _2206, _2207,
    _2208, _2210, _2213, _2215,
    _2216, _2221, _2223
)
from mastapy.system_model.part_model.shaft_model import _2226
from mastapy.system_model.part_model.gears import (
    _2256, _2258, _2260, _2261,
    _2262, _2264, _2266, _2268,
    _2270, _2271, _2273, _2277,
    _2279, _2281, _2283, _2286,
    _2288, _2290, _2292, _2293,
    _2294, _2296
)
from mastapy.system_model.part_model.cycloidal import _2312, _2313
from mastapy.system_model.part_model.couplings import (
    _2322, _2325, _2327, _2330,
    _2332, _2333, _2339, _2341,
    _2344, _2347, _2348, _2349,
    _2351, _2353
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _1954

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_1954.DesignEntity):
    '''Connection

    This is a mastapy class.
    '''

    TYPE = _CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.DrawingPosition) if self.wrapped.DrawingPosition is not None else None

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioFromAToB

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioFromAToB

    @property
    def unique_name(self) -> 'str':
        '''str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UniqueName

    @property
    def connection_id(self) -> 'str':
        '''str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectionID

    @property
    def socket_a(self) -> '_2041.Socket':
        '''Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.Socket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_bearing_inner_socket(self) -> '_2011.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.BearingInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_bearing_outer_socket(self) -> '_2012.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.BearingOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_2019.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CVTPulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_2021.CylindricalSocket':
        '''CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.CylindricalSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_2023.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_2024.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.InnerShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_inner_shaft_socket_base(self) -> '_2025.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.InnerShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_mountable_component_inner_socket(self) -> '_2027.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_mountable_component_outer_socket(self) -> '_2028.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_mountable_component_socket(self) -> '_2029.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.MountableComponentSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_2030.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.OuterShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_outer_shaft_socket_base(self) -> '_2031.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.OuterShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_2033.PlanetarySocket':
        '''PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.PlanetarySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_planetary_socket_base(self) -> '_2034.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.PlanetarySocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_2035.PulleySocket':
        '''PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.PulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_2038.RollingRingSocket':
        '''RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.RollingRingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_2039.ShaftSocket':
        '''ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2045.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_2047.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_2049.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.BevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_2051.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_2053.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_2055.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_2057.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.FaceGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_2059.GearTeethSocket':
        '''GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.GearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_2061.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2062.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2066.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2067.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2069.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2071.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_2073.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_2075.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.WormGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2077.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_left_socket(self) -> '_2078.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_right_socket(self) -> '_2079.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_inner_socket(self) -> '_2081.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_outer_socket(self) -> '_2082.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2084.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_ring_pins_socket(self) -> '_2085.RingPinsSocket':
        '''RingPinsSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.RingPinsSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_2088.ClutchSocket':
        '''ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.ClutchSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_2090.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.ConceptCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_2092.CouplingSocket':
        '''CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.CouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_2094.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_2096.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.SpringDamperSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_2098.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_2099.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA is not None else None

    @property
    def socket_b(self) -> '_2041.Socket':
        '''Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.Socket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_bearing_inner_socket(self) -> '_2011.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.BearingInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_bearing_outer_socket(self) -> '_2012.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.BearingOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_2019.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CVTPulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_2021.CylindricalSocket':
        '''CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.CylindricalSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_2023.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_2024.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.InnerShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_inner_shaft_socket_base(self) -> '_2025.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.InnerShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_mountable_component_inner_socket(self) -> '_2027.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_mountable_component_outer_socket(self) -> '_2028.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_mountable_component_socket(self) -> '_2029.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.MountableComponentSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_2030.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.OuterShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_outer_shaft_socket_base(self) -> '_2031.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.OuterShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_2033.PlanetarySocket':
        '''PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.PlanetarySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_planetary_socket_base(self) -> '_2034.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.PlanetarySocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_2035.PulleySocket':
        '''PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.PulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_2038.RollingRingSocket':
        '''RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.RollingRingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_2039.ShaftSocket':
        '''ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2045.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_2047.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2047.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_2049.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.BevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_2051.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_2053.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_2055.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_2057.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.FaceGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_2059.GearTeethSocket':
        '''GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.GearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_2061.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2062.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2066.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2067.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2069.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2071.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_2073.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_2075.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.WormGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2077.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_left_socket(self) -> '_2078.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_right_socket(self) -> '_2079.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_inner_socket(self) -> '_2081.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_outer_socket(self) -> '_2082.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2084.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_ring_pins_socket(self) -> '_2085.RingPinsSocket':
        '''RingPinsSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.RingPinsSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_2088.ClutchSocket':
        '''ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.ClutchSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_2090.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.ConceptCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_2092.CouplingSocket':
        '''CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.CouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_2094.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_2096.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.SpringDamperSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_2098.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_2099.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB is not None else None

    @property
    def owner_a(self) -> '_2189.Component':
        '''Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.Component.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_abstract_shaft(self) -> '_2181.AbstractShaft':
        '''AbstractShaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.AbstractShaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2182.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bearing(self) -> '_2185.Bearing':
        '''Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Bearing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bolt(self) -> '_2187.Bolt':
        '''Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.Bolt.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_connector(self) -> '_2192.Connector':
        '''Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.Connector.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_datum(self) -> '_2193.Datum':
        '''Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.Datum.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2196.ExternalCADModel':
        '''ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.ExternalCADModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_fe_part(self) -> '_2197.FEPart':
        '''FEPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2197.FEPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FEPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2199.GuideDxfModel':
        '''GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.GuideDxfModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2206.MassDisc':
        '''MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2206.MassDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2207.MeasurementComponent':
        '''MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.MeasurementComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2208.MountableComponent':
        '''MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.MountableComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2210.OilSeal':
        '''OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2210.OilSeal.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2213.PlanetCarrier':
        '''PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.PlanetCarrier.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_point_load(self) -> '_2215.PointLoad':
        '''PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.PointLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_power_load(self) -> '_2216.PowerLoad':
        '''PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.PowerLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2221.UnbalancedMass':
        '''UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2221.UnbalancedMass.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2223.VirtualComponent':
        '''VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2223.VirtualComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_shaft(self) -> '_2226.Shaft':
        '''Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.Shaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2256.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2258.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.BevelDifferentialGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2260.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2261.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2262.BevelGear':
        '''BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2264.ConceptGear':
        '''ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.ConceptGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2266.ConicalGear':
        '''ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2268.CylindricalGear':
        '''CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2268.CylindricalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2270.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2270.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2271.FaceGear':
        '''FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.FaceGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_gear(self) -> '_2273.Gear':
        '''Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.Gear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2277.HypoidGear':
        '''HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.HypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2279.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2281.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2286.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.SpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2288.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2290.StraightBevelGear':
        '''StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2290.StraightBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2292.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2293.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2293.StraightBevelSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2294.WormGear':
        '''WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.WormGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2296.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.ZerolBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_cycloidal_disc(self) -> '_2312.CycloidalDisc':
        '''CycloidalDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.CycloidalDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_ring_pins(self) -> '_2313.RingPins':
        '''RingPins: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.RingPins.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RingPins. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2322.ClutchHalf':
        '''ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.ClutchHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2325.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2327.CouplingHalf':
        '''CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2327.CouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2330.CVTPulley':
        '''CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2330.CVTPulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2332.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2332.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_pulley(self) -> '_2333.Pulley':
        '''Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.Pulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2339.RollingRing':
        '''RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.RollingRing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2341.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.ShaftHubConnection.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2344.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2344.SpringDamperHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2347.SynchroniserHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2348.SynchroniserPart':
        '''SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2348.SynchroniserPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2349.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2349.SynchroniserSleeve.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2351.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2351.TorqueConverterPump.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2353.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2353.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA is not None else None

    @property
    def owner_b(self) -> '_2189.Component':
        '''Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.Component.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_abstract_shaft(self) -> '_2181.AbstractShaft':
        '''AbstractShaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.AbstractShaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2182.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bearing(self) -> '_2185.Bearing':
        '''Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Bearing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bolt(self) -> '_2187.Bolt':
        '''Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.Bolt.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_connector(self) -> '_2192.Connector':
        '''Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.Connector.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_datum(self) -> '_2193.Datum':
        '''Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.Datum.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2196.ExternalCADModel':
        '''ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.ExternalCADModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_fe_part(self) -> '_2197.FEPart':
        '''FEPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2197.FEPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FEPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2199.GuideDxfModel':
        '''GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.GuideDxfModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2206.MassDisc':
        '''MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2206.MassDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2207.MeasurementComponent':
        '''MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.MeasurementComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2208.MountableComponent':
        '''MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.MountableComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2210.OilSeal':
        '''OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2210.OilSeal.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2213.PlanetCarrier':
        '''PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.PlanetCarrier.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_point_load(self) -> '_2215.PointLoad':
        '''PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.PointLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_power_load(self) -> '_2216.PowerLoad':
        '''PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.PowerLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2221.UnbalancedMass':
        '''UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2221.UnbalancedMass.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2223.VirtualComponent':
        '''VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2223.VirtualComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_shaft(self) -> '_2226.Shaft':
        '''Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.Shaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2256.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2258.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.BevelDifferentialGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2260.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2261.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2262.BevelGear':
        '''BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2264.ConceptGear':
        '''ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.ConceptGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2266.ConicalGear':
        '''ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2268.CylindricalGear':
        '''CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2268.CylindricalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2270.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2270.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2271.FaceGear':
        '''FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.FaceGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_gear(self) -> '_2273.Gear':
        '''Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.Gear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2277.HypoidGear':
        '''HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.HypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2279.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2281.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2286.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.SpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2288.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2290.StraightBevelGear':
        '''StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2290.StraightBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2292.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2293.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2293.StraightBevelSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2294.WormGear':
        '''WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.WormGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2296.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.ZerolBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_cycloidal_disc(self) -> '_2312.CycloidalDisc':
        '''CycloidalDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.CycloidalDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_ring_pins(self) -> '_2313.RingPins':
        '''RingPins: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.RingPins.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RingPins. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2322.ClutchHalf':
        '''ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.ClutchHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2325.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2327.CouplingHalf':
        '''CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2327.CouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2330.CVTPulley':
        '''CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2330.CVTPulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2332.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2332.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_pulley(self) -> '_2333.Pulley':
        '''Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.Pulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2339.RollingRing':
        '''RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.RollingRing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2341.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.ShaftHubConnection.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2344.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2344.SpringDamperHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2347.SynchroniserHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2348.SynchroniserPart':
        '''SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2348.SynchroniserPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2349.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2349.SynchroniserSleeve.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2351.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2351.TorqueConverterPump.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2353.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2353.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB is not None else None

    def socket_for(self, component: '_2189.Component') -> '_2041.Socket':
        ''' 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def other_owner(self, component: '_2189.Component') -> '_2189.Component':
        ''' 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def other_socket_for_component(self, component: '_2189.Component') -> '_2041.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def other_socket(self, socket: '_2041.Socket') -> '_2041.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
