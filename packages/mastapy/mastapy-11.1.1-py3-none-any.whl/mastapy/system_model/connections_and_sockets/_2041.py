'''_2041.py

Socket
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2189, _2181, _2182, _2185,
    _2187, _2192, _2193, _2196,
    _2197, _2199, _2206, _2207,
    _2208, _2210, _2213, _2215,
    _2216, _2221, _2223, _2190
)
from mastapy._internal.cast_exception import CastException
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
from mastapy.system_model.connections_and_sockets import _2017
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')


__docformat__ = 'restructuredtext en'
__all__ = ('Socket',)


class Socket(_0.APIBase):
    '''Socket

    This is a mastapy class.
    '''

    TYPE = _SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Socket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def owner(self) -> '_2189.Component':
        '''Component: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.Component.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Component. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_abstract_shaft(self) -> '_2181.AbstractShaft':
        '''AbstractShaft: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.AbstractShaft.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to AbstractShaft. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_abstract_shaft_or_housing(self) -> '_2182.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.AbstractShaftOrHousing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bearing(self) -> '_2185.Bearing':
        '''Bearing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.Bearing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Bearing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bolt(self) -> '_2187.Bolt':
        '''Bolt: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.Bolt.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Bolt. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_connector(self) -> '_2192.Connector':
        '''Connector: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.Connector.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Connector. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_datum(self) -> '_2193.Datum':
        '''Datum: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.Datum.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Datum. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_external_cad_model(self) -> '_2196.ExternalCADModel':
        '''ExternalCADModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.ExternalCADModel.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ExternalCADModel. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_fe_part(self) -> '_2197.FEPart':
        '''FEPart: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2197.FEPart.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to FEPart. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_guide_dxf_model(self) -> '_2199.GuideDxfModel':
        '''GuideDxfModel: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.GuideDxfModel.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to GuideDxfModel. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_mass_disc(self) -> '_2206.MassDisc':
        '''MassDisc: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2206.MassDisc.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MassDisc. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_measurement_component(self) -> '_2207.MeasurementComponent':
        '''MeasurementComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2207.MeasurementComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MeasurementComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_mountable_component(self) -> '_2208.MountableComponent':
        '''MountableComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2208.MountableComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to MountableComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_oil_seal(self) -> '_2210.OilSeal':
        '''OilSeal: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2210.OilSeal.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to OilSeal. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_planet_carrier(self) -> '_2213.PlanetCarrier':
        '''PlanetCarrier: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.PlanetCarrier.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PlanetCarrier. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_point_load(self) -> '_2215.PointLoad':
        '''PointLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.PointLoad.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PointLoad. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_power_load(self) -> '_2216.PowerLoad':
        '''PowerLoad: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.PowerLoad.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PowerLoad. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_unbalanced_mass(self) -> '_2221.UnbalancedMass':
        '''UnbalancedMass: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2221.UnbalancedMass.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to UnbalancedMass. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_virtual_component(self) -> '_2223.VirtualComponent':
        '''VirtualComponent: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2223.VirtualComponent.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to VirtualComponent. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_shaft(self) -> '_2226.Shaft':
        '''Shaft: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.Shaft.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Shaft. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_agma_gleason_conical_gear(self) -> '_2256.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.AGMAGleasonConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bevel_differential_gear(self) -> '_2258.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.BevelDifferentialGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bevel_differential_planet_gear(self) -> '_2260.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bevel_differential_sun_gear(self) -> '_2261.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2261.BevelDifferentialSunGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_bevel_gear(self) -> '_2262.BevelGear':
        '''BevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2262.BevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to BevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_concept_gear(self) -> '_2264.ConceptGear':
        '''ConceptGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2264.ConceptGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_conical_gear(self) -> '_2266.ConicalGear':
        '''ConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2266.ConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_cylindrical_gear(self) -> '_2268.CylindricalGear':
        '''CylindricalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2268.CylindricalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_cylindrical_planet_gear(self) -> '_2270.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2270.CylindricalPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_face_gear(self) -> '_2271.FaceGear':
        '''FaceGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2271.FaceGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to FaceGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_gear(self) -> '_2273.Gear':
        '''Gear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.Gear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Gear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_hypoid_gear(self) -> '_2277.HypoidGear':
        '''HypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.HypoidGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to HypoidGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2279.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2281.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2281.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2283.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_spiral_bevel_gear(self) -> '_2286.SpiralBevelGear':
        '''SpiralBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.SpiralBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_straight_bevel_diff_gear(self) -> '_2288.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2288.StraightBevelDiffGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_straight_bevel_gear(self) -> '_2290.StraightBevelGear':
        '''StraightBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2290.StraightBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_straight_bevel_planet_gear(self) -> '_2292.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2292.StraightBevelPlanetGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_straight_bevel_sun_gear(self) -> '_2293.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2293.StraightBevelSunGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_worm_gear(self) -> '_2294.WormGear':
        '''WormGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.WormGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to WormGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_zerol_bevel_gear(self) -> '_2296.ZerolBevelGear':
        '''ZerolBevelGear: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.ZerolBevelGear.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_cycloidal_disc(self) -> '_2312.CycloidalDisc':
        '''CycloidalDisc: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.CycloidalDisc.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CycloidalDisc. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_ring_pins(self) -> '_2313.RingPins':
        '''RingPins: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.RingPins.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to RingPins. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_clutch_half(self) -> '_2322.ClutchHalf':
        '''ClutchHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2322.ClutchHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ClutchHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_concept_coupling_half(self) -> '_2325.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2325.ConceptCouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_coupling_half(self) -> '_2327.CouplingHalf':
        '''CouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2327.CouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_cvt_pulley(self) -> '_2330.CVTPulley':
        '''CVTPulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2330.CVTPulley.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to CVTPulley. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_part_to_part_shear_coupling_half(self) -> '_2332.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2332.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_pulley(self) -> '_2333.Pulley':
        '''Pulley: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2333.Pulley.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to Pulley. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_rolling_ring(self) -> '_2339.RollingRing':
        '''RollingRing: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2339.RollingRing.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to RollingRing. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_shaft_hub_connection(self) -> '_2341.ShaftHubConnection':
        '''ShaftHubConnection: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.ShaftHubConnection.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_spring_damper_half(self) -> '_2344.SpringDamperHalf':
        '''SpringDamperHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2344.SpringDamperHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_synchroniser_half(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2347.SynchroniserHalf.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_synchroniser_part(self) -> '_2348.SynchroniserPart':
        '''SynchroniserPart: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2348.SynchroniserPart.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserPart. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_synchroniser_sleeve(self) -> '_2349.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2349.SynchroniserSleeve.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_torque_converter_pump(self) -> '_2351.TorqueConverterPump':
        '''TorqueConverterPump: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2351.TorqueConverterPump.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def owner_of_type_torque_converter_turbine(self) -> '_2353.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Owner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2353.TorqueConverterTurbine.TYPE not in self.wrapped.Owner.__class__.__mro__:
            raise CastException('Failed to cast owner to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Owner.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Owner.__class__)(self.wrapped.Owner) if self.wrapped.Owner is not None else None

    @property
    def connections(self) -> 'List[_2017.Connection]':
        '''List[Connection]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Connections, constructor.new(_2017.Connection))
        return value

    @property
    def connected_components(self) -> 'List[_2189.Component]':
        '''List[Component]: 'ConnectedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectedComponents, constructor.new(_2189.Component))
        return value

    def connect_to_socket(self, socket: 'Socket') -> '_2190.ComponentsConnectedResult':
        ''' 'ConnectTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        method_result = self.wrapped.ConnectTo.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def get_possible_sockets_to_connect_to(self, component_to_connect_to: '_2189.Component') -> 'List[Socket]':
        ''' 'GetPossibleSocketsToConnectTo' is the original name of this method.

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)

        Returns:
            List[mastapy.system_model.connections_and_sockets.Socket]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetPossibleSocketsToConnectTo(component_to_connect_to.wrapped if component_to_connect_to else None), constructor.new(Socket))

    def connect_to(self, component: '_2189.Component') -> '_2190.ComponentsConnectedResult':
        ''' 'ConnectTo' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        method_result = self.wrapped.ConnectTo.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def connection_to(self, socket: 'Socket') -> '_2017.Connection':
        ''' 'ConnectionTo' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        method_result = self.wrapped.ConnectionTo(socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None
