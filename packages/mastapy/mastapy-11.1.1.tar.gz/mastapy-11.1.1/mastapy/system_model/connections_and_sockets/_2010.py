'''_2010.py

AbstractShaftToMountableComponentConnection
'''


from mastapy.system_model.part_model import (
    _2208, _2185, _2192, _2206,
    _2207, _2210, _2213, _2215,
    _2216, _2221, _2223, _2181
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.gears import (
    _2256, _2258, _2260, _2261,
    _2262, _2264, _2266, _2268,
    _2270, _2271, _2273, _2277,
    _2279, _2281, _2283, _2286,
    _2288, _2290, _2292, _2293,
    _2294, _2296
)
from mastapy.system_model.part_model.cycloidal import _2313, _2312
from mastapy.system_model.part_model.couplings import (
    _2322, _2325, _2327, _2330,
    _2332, _2333, _2339, _2341,
    _2344, _2347, _2348, _2349,
    _2351, _2353
)
from mastapy.system_model.part_model.shaft_model import _2226
from mastapy.system_model.connections_and_sockets import _2017
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnection',)


class AbstractShaftToMountableComponentConnection(_2017.Connection):
    '''AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mountable_component(self) -> '_2208.MountableComponent':
        '''MountableComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.MountableComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MountableComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bearing(self) -> '_2185.Bearing':
        '''Bearing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Bearing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Bearing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_connector(self) -> '_2192.Connector':
        '''Connector: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.Connector.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Connector. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_mass_disc(self) -> '_2206.MassDisc':
        '''MassDisc: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2206.MassDisc.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MassDisc. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_measurement_component(self) -> '_2207.MeasurementComponent':
        '''MeasurementComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.MeasurementComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_oil_seal(self) -> '_2210.OilSeal':
        '''OilSeal: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2210.OilSeal.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to OilSeal. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_planet_carrier(self) -> '_2213.PlanetCarrier':
        '''PlanetCarrier: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.PlanetCarrier.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_point_load(self) -> '_2215.PointLoad':
        '''PointLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.PointLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PointLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_power_load(self) -> '_2216.PowerLoad':
        '''PowerLoad: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.PowerLoad.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PowerLoad. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_unbalanced_mass(self) -> '_2221.UnbalancedMass':
        '''UnbalancedMass: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2221.UnbalancedMass.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_virtual_component(self) -> '_2223.VirtualComponent':
        '''VirtualComponent: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2223.VirtualComponent.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to VirtualComponent. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_agma_gleason_conical_gear(self) -> '_2256.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.AGMAGleasonConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_gear(self) -> '_2258.BevelDifferentialGear':
        '''BevelDifferentialGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.BevelDifferentialGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_planet_gear(self) -> '_2260.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.BevelDifferentialPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_differential_sun_gear(self) -> '_2261.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.BevelDifferentialSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_bevel_gear(self) -> '_2262.BevelGear':
        '''BevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to BevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_concept_gear(self) -> '_2264.ConceptGear':
        '''ConceptGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.ConceptGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_conical_gear(self) -> '_2266.ConicalGear':
        '''ConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cylindrical_gear(self) -> '_2268.CylindricalGear':
        '''CylindricalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2268.CylindricalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cylindrical_planet_gear(self) -> '_2270.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2270.CylindricalPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_face_gear(self) -> '_2271.FaceGear':
        '''FaceGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.FaceGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to FaceGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_gear(self) -> '_2273.Gear':
        '''Gear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.Gear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Gear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_hypoid_gear(self) -> '_2277.HypoidGear':
        '''HypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.HypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to HypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2279.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2281.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_spiral_bevel_gear(self) -> '_2286.SpiralBevelGear':
        '''SpiralBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.SpiralBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_diff_gear(self) -> '_2288.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.StraightBevelDiffGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_gear(self) -> '_2290.StraightBevelGear':
        '''StraightBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2290.StraightBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_planet_gear(self) -> '_2292.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.StraightBevelPlanetGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_straight_bevel_sun_gear(self) -> '_2293.StraightBevelSunGear':
        '''StraightBevelSunGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2293.StraightBevelSunGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_worm_gear(self) -> '_2294.WormGear':
        '''WormGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.WormGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to WormGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_zerol_bevel_gear(self) -> '_2296.ZerolBevelGear':
        '''ZerolBevelGear: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.ZerolBevelGear.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_ring_pins(self) -> '_2313.RingPins':
        '''RingPins: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.RingPins.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RingPins. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_clutch_half(self) -> '_2322.ClutchHalf':
        '''ClutchHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.ClutchHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ClutchHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_concept_coupling_half(self) -> '_2325.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.ConceptCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_coupling_half(self) -> '_2327.CouplingHalf':
        '''CouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2327.CouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_cvt_pulley(self) -> '_2330.CVTPulley':
        '''CVTPulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2330.CVTPulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to CVTPulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_part_to_part_shear_coupling_half(self) -> '_2332.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2332.PartToPartShearCouplingHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_pulley(self) -> '_2333.Pulley':
        '''Pulley: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.Pulley.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to Pulley. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_rolling_ring(self) -> '_2339.RollingRing':
        '''RollingRing: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.RollingRing.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to RollingRing. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_shaft_hub_connection(self) -> '_2341.ShaftHubConnection':
        '''ShaftHubConnection: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.ShaftHubConnection.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_spring_damper_half(self) -> '_2344.SpringDamperHalf':
        '''SpringDamperHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2344.SpringDamperHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_half(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2347.SynchroniserHalf.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_part(self) -> '_2348.SynchroniserPart':
        '''SynchroniserPart: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2348.SynchroniserPart.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_synchroniser_sleeve(self) -> '_2349.SynchroniserSleeve':
        '''SynchroniserSleeve: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2349.SynchroniserSleeve.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_torque_converter_pump(self) -> '_2351.TorqueConverterPump':
        '''TorqueConverterPump: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2351.TorqueConverterPump.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def mountable_component_of_type_torque_converter_turbine(self) -> '_2353.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'MountableComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2353.TorqueConverterTurbine.TYPE not in self.wrapped.MountableComponent.__class__.__mro__:
            raise CastException('Failed to cast mountable_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.MountableComponent.__class__.__qualname__))

        return constructor.new_override(self.wrapped.MountableComponent.__class__)(self.wrapped.MountableComponent) if self.wrapped.MountableComponent is not None else None

    @property
    def shaft(self) -> '_2181.AbstractShaft':
        '''AbstractShaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.AbstractShaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to AbstractShaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None

    @property
    def shaft_of_type_shaft(self) -> '_2226.Shaft':
        '''Shaft: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.Shaft.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to Shaft. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None

    @property
    def shaft_of_type_cycloidal_disc(self) -> '_2312.CycloidalDisc':
        '''CycloidalDisc: 'Shaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.CycloidalDisc.TYPE not in self.wrapped.Shaft.__class__.__mro__:
            raise CastException('Failed to cast shaft to CycloidalDisc. Expected: {}.'.format(self.wrapped.Shaft.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Shaft.__class__)(self.wrapped.Shaft) if self.wrapped.Shaft is not None else None
