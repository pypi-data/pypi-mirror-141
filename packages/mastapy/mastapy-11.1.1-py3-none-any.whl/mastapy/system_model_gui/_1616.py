'''_1616.py

MASTAGUI
'''


from typing import List, Dict

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.system_model import _1954, _1950
from mastapy.system_model.connections_and_sockets import (
    _2010, _2013, _2014, _2017,
    _2018, _2026, _2032, _2037,
    _2040
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2044, _2046, _2048, _2050,
    _2052, _2054, _2056, _2058,
    _2060, _2063, _2064, _2065,
    _2068, _2070, _2072, _2074,
    _2076
)
from mastapy.system_model.connections_and_sockets.cycloidal import _2080, _2083, _2086
from mastapy.system_model.connections_and_sockets.couplings import (
    _2087, _2089, _2091, _2093,
    _2095, _2097
)
from mastapy.system_model.part_model import (
    _2179, _2180, _2181, _2182,
    _2185, _2187, _2188, _2189,
    _2192, _2193, _2196, _2197,
    _2198, _2199, _2206, _2207,
    _2208, _2210, _2212, _2213,
    _2215, _2216, _2218, _2220,
    _2221, _2223
)
from mastapy.system_model.part_model.shaft_model import _2226
from mastapy.system_model.part_model.gears import (
    _2256, _2257, _2258, _2259,
    _2260, _2261, _2262, _2263,
    _2264, _2265, _2266, _2267,
    _2268, _2269, _2270, _2271,
    _2272, _2273, _2275, _2277,
    _2278, _2279, _2280, _2281,
    _2282, _2283, _2284, _2285,
    _2286, _2287, _2288, _2289,
    _2290, _2291, _2292, _2293,
    _2294, _2295, _2296, _2297
)
from mastapy.system_model.part_model.cycloidal import _2311, _2312, _2313
from mastapy.system_model.part_model.couplings import (
    _2319, _2321, _2322, _2324,
    _2325, _2326, _2327, _2329,
    _2330, _2331, _2332, _2333,
    _2339, _2340, _2341, _2343,
    _2344, _2345, _2347, _2348,
    _2349, _2350, _2351, _2353
)
from mastapy._math.color import Color
from mastapy._math.vector_3d import Vector3D
from mastapy.utility.operation_modes import _1564
from mastapy.math_utility import _1294, _1313
from mastapy.nodal_analysis.geometry_modeller_link import _151
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_FACETED_BODY = python_net_import('SMT.MastaAPI.MathUtility', 'FacetedBody')
_STRING = python_net_import('System', 'String')
_MASTAGUI = python_net_import('SMT.MastaAPI.SystemModelGUI', 'MASTAGUI')


__docformat__ = 'restructuredtext en'
__all__ = ('MASTAGUI',)


class MASTAGUI(_0.APIBase):
    '''MASTAGUI

    This is a mastapy class.
    '''

    TYPE = _MASTAGUI

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MASTAGUI.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_paused(self) -> 'bool':
        '''bool: 'IsPaused' is the original name of this property.'''

        return self.wrapped.IsPaused

    @is_paused.setter
    def is_paused(self, value: 'bool'):
        self.wrapped.IsPaused = bool(value) if value else False

    @property
    def is_initialised(self) -> 'bool':
        '''bool: 'IsInitialised' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsInitialised

    @property
    def is_remoting(self) -> 'bool':
        '''bool: 'IsRemoting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsRemoting

    @property
    def selected_design_entity(self) -> '_1954.DesignEntity':
        '''DesignEntity: 'SelectedDesignEntity' is the original name of this property.'''

        if _1954.DesignEntity.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to DesignEntity. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity.setter
    def selected_design_entity(self, value: '_1954.DesignEntity'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_2010.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2010.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_abstract_shaft_to_mountable_component_connection(self, value: '_2010.AbstractShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_connection(self) -> '_2013.BeltConnection':
        '''BeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2013.BeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_belt_connection.setter
    def selected_design_entity_of_type_belt_connection(self, value: '_2013.BeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coaxial_connection(self) -> '_2014.CoaxialConnection':
        '''CoaxialConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2014.CoaxialConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CoaxialConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_coaxial_connection.setter
    def selected_design_entity_of_type_coaxial_connection(self, value: '_2014.CoaxialConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connection(self) -> '_2017.Connection':
        '''Connection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2017.Connection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_connection.setter
    def selected_design_entity_of_type_connection(self, value: '_2017.Connection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_belt_connection(self) -> '_2018.CVTBeltConnection':
        '''CVTBeltConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2018.CVTBeltConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTBeltConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cvt_belt_connection.setter
    def selected_design_entity_of_type_cvt_belt_connection(self, value: '_2018.CVTBeltConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_inter_mountable_component_connection(self) -> '_2026.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2026.InterMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_inter_mountable_component_connection.setter
    def selected_design_entity_of_type_inter_mountable_component_connection(self, value: '_2026.InterMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_connection(self) -> '_2032.PlanetaryConnection':
        '''PlanetaryConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2032.PlanetaryConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_planetary_connection.setter
    def selected_design_entity_of_type_planetary_connection(self, value: '_2032.PlanetaryConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_connection(self) -> '_2037.RollingRingConnection':
        '''RollingRingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2037.RollingRingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_rolling_ring_connection.setter
    def selected_design_entity_of_type_rolling_ring_connection(self, value: '_2037.RollingRingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self) -> '_2040.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2040.ShaftToMountableComponentConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_shaft_to_mountable_component_connection.setter
    def selected_design_entity_of_type_shaft_to_mountable_component_connection(self, value: '_2040.ShaftToMountableComponentConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self) -> '_2044.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2044.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_mesh.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_mesh(self, value: '_2044.AGMAGleasonConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self) -> '_2046.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2046.BevelDifferentialGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_mesh.setter
    def selected_design_entity_of_type_bevel_differential_gear_mesh(self, value: '_2046.BevelDifferentialGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_mesh(self) -> '_2048.BevelGearMesh':
        '''BevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2048.BevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_gear_mesh.setter
    def selected_design_entity_of_type_bevel_gear_mesh(self, value: '_2048.BevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_mesh(self) -> '_2050.ConceptGearMesh':
        '''ConceptGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2050.ConceptGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_gear_mesh.setter
    def selected_design_entity_of_type_concept_gear_mesh(self, value: '_2050.ConceptGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_mesh(self) -> '_2052.ConicalGearMesh':
        '''ConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2052.ConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_conical_gear_mesh.setter
    def selected_design_entity_of_type_conical_gear_mesh(self, value: '_2052.ConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_mesh(self) -> '_2054.CylindricalGearMesh':
        '''CylindricalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2054.CylindricalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cylindrical_gear_mesh.setter
    def selected_design_entity_of_type_cylindrical_gear_mesh(self, value: '_2054.CylindricalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_mesh(self) -> '_2056.FaceGearMesh':
        '''FaceGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2056.FaceGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_face_gear_mesh.setter
    def selected_design_entity_of_type_face_gear_mesh(self, value: '_2056.FaceGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_mesh(self) -> '_2058.GearMesh':
        '''GearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2058.GearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_gear_mesh.setter
    def selected_design_entity_of_type_gear_mesh(self, value: '_2058.GearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_mesh(self) -> '_2060.HypoidGearMesh':
        '''HypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2060.HypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_hypoid_gear_mesh(self, value: '_2060.HypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_2063.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2063.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self, value: '_2063.KlingelnbergCycloPalloidConicalGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_2064.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2064.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, value: '_2064.KlingelnbergCycloPalloidHypoidGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_2065.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2065.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, value: '_2065.KlingelnbergCycloPalloidSpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self) -> '_2068.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2068.SpiralBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_mesh.setter
    def selected_design_entity_of_type_spiral_bevel_gear_mesh(self, value: '_2068.SpiralBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self) -> '_2070.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2070.StraightBevelDiffGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_mesh(self, value: '_2070.StraightBevelDiffGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self) -> '_2072.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2072.StraightBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_mesh.setter
    def selected_design_entity_of_type_straight_bevel_gear_mesh(self, value: '_2072.StraightBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_mesh(self) -> '_2074.WormGearMesh':
        '''WormGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2074.WormGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_worm_gear_mesh.setter
    def selected_design_entity_of_type_worm_gear_mesh(self, value: '_2074.WormGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self) -> '_2076.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'SelectedDesignEntity' is the original name of this property.'''

        if _2076.ZerolBevelGearMesh.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_mesh.setter
    def selected_design_entity_of_type_zerol_bevel_gear_mesh(self, value: '_2076.ZerolBevelGearMesh'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self) -> '_2080.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2080.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cycloidal_disc_central_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_central_bearing_connection(self, value: '_2080.CycloidalDiscCentralBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_2083.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2083.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection.setter
    def selected_design_entity_of_type_cycloidal_disc_planetary_bearing_connection(self, value: '_2083.CycloidalDiscPlanetaryBearingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self) -> '_2086.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2086.RingPinsToDiscConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_ring_pins_to_disc_connection.setter
    def selected_design_entity_of_type_ring_pins_to_disc_connection(self, value: '_2086.RingPinsToDiscConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_connection(self) -> '_2087.ClutchConnection':
        '''ClutchConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2087.ClutchConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_clutch_connection.setter
    def selected_design_entity_of_type_clutch_connection(self, value: '_2087.ClutchConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_connection(self) -> '_2089.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2089.ConceptCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_coupling_connection.setter
    def selected_design_entity_of_type_concept_coupling_connection(self, value: '_2089.ConceptCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_connection(self) -> '_2091.CouplingConnection':
        '''CouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2091.CouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_coupling_connection.setter
    def selected_design_entity_of_type_coupling_connection(self, value: '_2091.CouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self) -> '_2093.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2093.PartToPartShearCouplingConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_connection.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_connection(self, value: '_2093.PartToPartShearCouplingConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_connection(self) -> '_2095.SpringDamperConnection':
        '''SpringDamperConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2095.SpringDamperConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spring_damper_connection.setter
    def selected_design_entity_of_type_spring_damper_connection(self, value: '_2095.SpringDamperConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_connection(self) -> '_2097.TorqueConverterConnection':
        '''TorqueConverterConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2097.TorqueConverterConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_torque_converter_connection.setter
    def selected_design_entity_of_type_torque_converter_connection(self, value: '_2097.TorqueConverterConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_assembly(self) -> '_2179.Assembly':
        '''Assembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2179.Assembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Assembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_assembly.setter
    def selected_design_entity_of_type_assembly(self, value: '_2179.Assembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_assembly(self) -> '_2180.AbstractAssembly':
        '''AbstractAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2180.AbstractAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_abstract_assembly.setter
    def selected_design_entity_of_type_abstract_assembly(self, value: '_2180.AbstractAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft(self) -> '_2181.AbstractShaft':
        '''AbstractShaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2181.AbstractShaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_abstract_shaft.setter
    def selected_design_entity_of_type_abstract_shaft(self, value: '_2181.AbstractShaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_abstract_shaft_or_housing(self) -> '_2182.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2182.AbstractShaftOrHousing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_abstract_shaft_or_housing.setter
    def selected_design_entity_of_type_abstract_shaft_or_housing(self, value: '_2182.AbstractShaftOrHousing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bearing(self) -> '_2185.Bearing':
        '''Bearing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2185.Bearing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bearing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bearing.setter
    def selected_design_entity_of_type_bearing(self, value: '_2185.Bearing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolt(self) -> '_2187.Bolt':
        '''Bolt: 'SelectedDesignEntity' is the original name of this property.'''

        if _2187.Bolt.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Bolt. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bolt.setter
    def selected_design_entity_of_type_bolt(self, value: '_2187.Bolt'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bolted_joint(self) -> '_2188.BoltedJoint':
        '''BoltedJoint: 'SelectedDesignEntity' is the original name of this property.'''

        if _2188.BoltedJoint.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BoltedJoint. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bolted_joint.setter
    def selected_design_entity_of_type_bolted_joint(self, value: '_2188.BoltedJoint'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_component(self) -> '_2189.Component':
        '''Component: 'SelectedDesignEntity' is the original name of this property.'''

        if _2189.Component.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Component. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_component.setter
    def selected_design_entity_of_type_component(self, value: '_2189.Component'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_connector(self) -> '_2192.Connector':
        '''Connector: 'SelectedDesignEntity' is the original name of this property.'''

        if _2192.Connector.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Connector. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_connector.setter
    def selected_design_entity_of_type_connector(self, value: '_2192.Connector'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_datum(self) -> '_2193.Datum':
        '''Datum: 'SelectedDesignEntity' is the original name of this property.'''

        if _2193.Datum.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Datum. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_datum.setter
    def selected_design_entity_of_type_datum(self, value: '_2193.Datum'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_external_cad_model(self) -> '_2196.ExternalCADModel':
        '''ExternalCADModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2196.ExternalCADModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ExternalCADModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_external_cad_model.setter
    def selected_design_entity_of_type_external_cad_model(self, value: '_2196.ExternalCADModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_fe_part(self) -> '_2197.FEPart':
        '''FEPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2197.FEPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FEPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_fe_part.setter
    def selected_design_entity_of_type_fe_part(self, value: '_2197.FEPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_flexible_pin_assembly(self) -> '_2198.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2198.FlexiblePinAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_flexible_pin_assembly.setter
    def selected_design_entity_of_type_flexible_pin_assembly(self, value: '_2198.FlexiblePinAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_guide_dxf_model(self) -> '_2199.GuideDxfModel':
        '''GuideDxfModel: 'SelectedDesignEntity' is the original name of this property.'''

        if _2199.GuideDxfModel.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GuideDxfModel. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_guide_dxf_model.setter
    def selected_design_entity_of_type_guide_dxf_model(self, value: '_2199.GuideDxfModel'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mass_disc(self) -> '_2206.MassDisc':
        '''MassDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2206.MassDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MassDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_mass_disc.setter
    def selected_design_entity_of_type_mass_disc(self, value: '_2206.MassDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_measurement_component(self) -> '_2207.MeasurementComponent':
        '''MeasurementComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2207.MeasurementComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MeasurementComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_measurement_component.setter
    def selected_design_entity_of_type_measurement_component(self, value: '_2207.MeasurementComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_mountable_component(self) -> '_2208.MountableComponent':
        '''MountableComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2208.MountableComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to MountableComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_mountable_component.setter
    def selected_design_entity_of_type_mountable_component(self, value: '_2208.MountableComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_oil_seal(self) -> '_2210.OilSeal':
        '''OilSeal: 'SelectedDesignEntity' is the original name of this property.'''

        if _2210.OilSeal.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to OilSeal. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_oil_seal.setter
    def selected_design_entity_of_type_oil_seal(self, value: '_2210.OilSeal'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part(self) -> '_2212.Part':
        '''Part: 'SelectedDesignEntity' is the original name of this property.'''

        if _2212.Part.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Part. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_part.setter
    def selected_design_entity_of_type_part(self, value: '_2212.Part'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planet_carrier(self) -> '_2213.PlanetCarrier':
        '''PlanetCarrier: 'SelectedDesignEntity' is the original name of this property.'''

        if _2213.PlanetCarrier.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetCarrier. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_planet_carrier.setter
    def selected_design_entity_of_type_planet_carrier(self, value: '_2213.PlanetCarrier'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_point_load(self) -> '_2215.PointLoad':
        '''PointLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2215.PointLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PointLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_point_load.setter
    def selected_design_entity_of_type_point_load(self, value: '_2215.PointLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_power_load(self) -> '_2216.PowerLoad':
        '''PowerLoad: 'SelectedDesignEntity' is the original name of this property.'''

        if _2216.PowerLoad.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PowerLoad. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_power_load.setter
    def selected_design_entity_of_type_power_load(self, value: '_2216.PowerLoad'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_root_assembly(self) -> '_2218.RootAssembly':
        '''RootAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2218.RootAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RootAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_root_assembly.setter
    def selected_design_entity_of_type_root_assembly(self, value: '_2218.RootAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_specialised_assembly(self) -> '_2220.SpecialisedAssembly':
        '''SpecialisedAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2220.SpecialisedAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_specialised_assembly.setter
    def selected_design_entity_of_type_specialised_assembly(self, value: '_2220.SpecialisedAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_unbalanced_mass(self) -> '_2221.UnbalancedMass':
        '''UnbalancedMass: 'SelectedDesignEntity' is the original name of this property.'''

        if _2221.UnbalancedMass.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to UnbalancedMass. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_unbalanced_mass.setter
    def selected_design_entity_of_type_unbalanced_mass(self, value: '_2221.UnbalancedMass'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_virtual_component(self) -> '_2223.VirtualComponent':
        '''VirtualComponent: 'SelectedDesignEntity' is the original name of this property.'''

        if _2223.VirtualComponent.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to VirtualComponent. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_virtual_component.setter
    def selected_design_entity_of_type_virtual_component(self, value: '_2223.VirtualComponent'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft(self) -> '_2226.Shaft':
        '''Shaft: 'SelectedDesignEntity' is the original name of this property.'''

        if _2226.Shaft.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Shaft. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_shaft.setter
    def selected_design_entity_of_type_shaft(self, value: '_2226.Shaft'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear(self) -> '_2256.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2256.AGMAGleasonConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear(self, value: '_2256.AGMAGleasonConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self) -> '_2257.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2257.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_agma_gleason_conical_gear_set.setter
    def selected_design_entity_of_type_agma_gleason_conical_gear_set(self, value: '_2257.AGMAGleasonConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear(self) -> '_2258.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2258.BevelDifferentialGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_differential_gear.setter
    def selected_design_entity_of_type_bevel_differential_gear(self, value: '_2258.BevelDifferentialGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_gear_set(self) -> '_2259.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2259.BevelDifferentialGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_differential_gear_set.setter
    def selected_design_entity_of_type_bevel_differential_gear_set(self, value: '_2259.BevelDifferentialGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_planet_gear(self) -> '_2260.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2260.BevelDifferentialPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_differential_planet_gear.setter
    def selected_design_entity_of_type_bevel_differential_planet_gear(self, value: '_2260.BevelDifferentialPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_differential_sun_gear(self) -> '_2261.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2261.BevelDifferentialSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_differential_sun_gear.setter
    def selected_design_entity_of_type_bevel_differential_sun_gear(self, value: '_2261.BevelDifferentialSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear(self) -> '_2262.BevelGear':
        '''BevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2262.BevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_gear.setter
    def selected_design_entity_of_type_bevel_gear(self, value: '_2262.BevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_bevel_gear_set(self) -> '_2263.BevelGearSet':
        '''BevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2263.BevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_bevel_gear_set.setter
    def selected_design_entity_of_type_bevel_gear_set(self, value: '_2263.BevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear(self) -> '_2264.ConceptGear':
        '''ConceptGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2264.ConceptGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_gear.setter
    def selected_design_entity_of_type_concept_gear(self, value: '_2264.ConceptGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_gear_set(self) -> '_2265.ConceptGearSet':
        '''ConceptGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2265.ConceptGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_gear_set.setter
    def selected_design_entity_of_type_concept_gear_set(self, value: '_2265.ConceptGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear(self) -> '_2266.ConicalGear':
        '''ConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2266.ConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_conical_gear.setter
    def selected_design_entity_of_type_conical_gear(self, value: '_2266.ConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_conical_gear_set(self) -> '_2267.ConicalGearSet':
        '''ConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2267.ConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_conical_gear_set.setter
    def selected_design_entity_of_type_conical_gear_set(self, value: '_2267.ConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear(self) -> '_2268.CylindricalGear':
        '''CylindricalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2268.CylindricalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cylindrical_gear.setter
    def selected_design_entity_of_type_cylindrical_gear(self, value: '_2268.CylindricalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_gear_set(self) -> '_2269.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2269.CylindricalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cylindrical_gear_set.setter
    def selected_design_entity_of_type_cylindrical_gear_set(self, value: '_2269.CylindricalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cylindrical_planet_gear(self) -> '_2270.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2270.CylindricalPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cylindrical_planet_gear.setter
    def selected_design_entity_of_type_cylindrical_planet_gear(self, value: '_2270.CylindricalPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear(self) -> '_2271.FaceGear':
        '''FaceGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2271.FaceGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_face_gear.setter
    def selected_design_entity_of_type_face_gear(self, value: '_2271.FaceGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_face_gear_set(self) -> '_2272.FaceGearSet':
        '''FaceGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2272.FaceGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to FaceGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_face_gear_set.setter
    def selected_design_entity_of_type_face_gear_set(self, value: '_2272.FaceGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear(self) -> '_2273.Gear':
        '''Gear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2273.Gear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Gear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_gear.setter
    def selected_design_entity_of_type_gear(self, value: '_2273.Gear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_gear_set(self) -> '_2275.GearSet':
        '''GearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2275.GearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to GearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_gear_set.setter
    def selected_design_entity_of_type_gear_set(self, value: '_2275.GearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear(self) -> '_2277.HypoidGear':
        '''HypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2277.HypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_hypoid_gear.setter
    def selected_design_entity_of_type_hypoid_gear(self, value: '_2277.HypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_hypoid_gear_set(self) -> '_2278.HypoidGearSet':
        '''HypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2278.HypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to HypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_hypoid_gear_set.setter
    def selected_design_entity_of_type_hypoid_gear_set(self, value: '_2278.HypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2279.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2279.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear(self, value: '_2279.KlingelnbergCycloPalloidConicalGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2280.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2280.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, value: '_2280.KlingelnbergCycloPalloidConicalGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2281.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2281.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, value: '_2281.KlingelnbergCycloPalloidHypoidGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2282.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2282.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, value: '_2282.KlingelnbergCycloPalloidHypoidGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2283.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2283.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, value: '_2283.KlingelnbergCycloPalloidSpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2284.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2284.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, value: '_2284.KlingelnbergCycloPalloidSpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_planetary_gear_set(self) -> '_2285.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2285.PlanetaryGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_planetary_gear_set.setter
    def selected_design_entity_of_type_planetary_gear_set(self, value: '_2285.PlanetaryGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear(self) -> '_2286.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2286.SpiralBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear.setter
    def selected_design_entity_of_type_spiral_bevel_gear(self, value: '_2286.SpiralBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spiral_bevel_gear_set(self) -> '_2287.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2287.SpiralBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spiral_bevel_gear_set.setter
    def selected_design_entity_of_type_spiral_bevel_gear_set(self, value: '_2287.SpiralBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear(self) -> '_2288.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2288.StraightBevelDiffGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear(self, value: '_2288.StraightBevelDiffGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self) -> '_2289.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2289.StraightBevelDiffGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_diff_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_diff_gear_set(self, value: '_2289.StraightBevelDiffGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear(self) -> '_2290.StraightBevelGear':
        '''StraightBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2290.StraightBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_gear.setter
    def selected_design_entity_of_type_straight_bevel_gear(self, value: '_2290.StraightBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_gear_set(self) -> '_2291.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2291.StraightBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_gear_set.setter
    def selected_design_entity_of_type_straight_bevel_gear_set(self, value: '_2291.StraightBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_planet_gear(self) -> '_2292.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2292.StraightBevelPlanetGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_planet_gear.setter
    def selected_design_entity_of_type_straight_bevel_planet_gear(self, value: '_2292.StraightBevelPlanetGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_straight_bevel_sun_gear(self) -> '_2293.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2293.StraightBevelSunGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_straight_bevel_sun_gear.setter
    def selected_design_entity_of_type_straight_bevel_sun_gear(self, value: '_2293.StraightBevelSunGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear(self) -> '_2294.WormGear':
        '''WormGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2294.WormGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_worm_gear.setter
    def selected_design_entity_of_type_worm_gear(self, value: '_2294.WormGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_worm_gear_set(self) -> '_2295.WormGearSet':
        '''WormGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2295.WormGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to WormGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_worm_gear_set.setter
    def selected_design_entity_of_type_worm_gear_set(self, value: '_2295.WormGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear(self) -> '_2296.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedDesignEntity' is the original name of this property.'''

        if _2296.ZerolBevelGear.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGear. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear.setter
    def selected_design_entity_of_type_zerol_bevel_gear(self, value: '_2296.ZerolBevelGear'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_zerol_bevel_gear_set(self) -> '_2297.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedDesignEntity' is the original name of this property.'''

        if _2297.ZerolBevelGearSet.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_zerol_bevel_gear_set.setter
    def selected_design_entity_of_type_zerol_bevel_gear_set(self, value: '_2297.ZerolBevelGearSet'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_assembly(self) -> '_2311.CycloidalAssembly':
        '''CycloidalAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2311.CycloidalAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cycloidal_assembly.setter
    def selected_design_entity_of_type_cycloidal_assembly(self, value: '_2311.CycloidalAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cycloidal_disc(self) -> '_2312.CycloidalDisc':
        '''CycloidalDisc: 'SelectedDesignEntity' is the original name of this property.'''

        if _2312.CycloidalDisc.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CycloidalDisc. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cycloidal_disc.setter
    def selected_design_entity_of_type_cycloidal_disc(self, value: '_2312.CycloidalDisc'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_ring_pins(self) -> '_2313.RingPins':
        '''RingPins: 'SelectedDesignEntity' is the original name of this property.'''

        if _2313.RingPins.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RingPins. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_ring_pins.setter
    def selected_design_entity_of_type_ring_pins(self, value: '_2313.RingPins'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_belt_drive(self) -> '_2319.BeltDrive':
        '''BeltDrive: 'SelectedDesignEntity' is the original name of this property.'''

        if _2319.BeltDrive.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to BeltDrive. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_belt_drive.setter
    def selected_design_entity_of_type_belt_drive(self, value: '_2319.BeltDrive'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch(self) -> '_2321.Clutch':
        '''Clutch: 'SelectedDesignEntity' is the original name of this property.'''

        if _2321.Clutch.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Clutch. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_clutch.setter
    def selected_design_entity_of_type_clutch(self, value: '_2321.Clutch'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_clutch_half(self) -> '_2322.ClutchHalf':
        '''ClutchHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2322.ClutchHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ClutchHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_clutch_half.setter
    def selected_design_entity_of_type_clutch_half(self, value: '_2322.ClutchHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling(self) -> '_2324.ConceptCoupling':
        '''ConceptCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2324.ConceptCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_coupling.setter
    def selected_design_entity_of_type_concept_coupling(self, value: '_2324.ConceptCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_concept_coupling_half(self) -> '_2325.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2325.ConceptCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_concept_coupling_half.setter
    def selected_design_entity_of_type_concept_coupling_half(self, value: '_2325.ConceptCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling(self) -> '_2326.Coupling':
        '''Coupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2326.Coupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Coupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_coupling.setter
    def selected_design_entity_of_type_coupling(self, value: '_2326.Coupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_coupling_half(self) -> '_2327.CouplingHalf':
        '''CouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2327.CouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_coupling_half.setter
    def selected_design_entity_of_type_coupling_half(self, value: '_2327.CouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt(self) -> '_2329.CVT':
        '''CVT: 'SelectedDesignEntity' is the original name of this property.'''

        if _2329.CVT.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVT. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cvt.setter
    def selected_design_entity_of_type_cvt(self, value: '_2329.CVT'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_cvt_pulley(self) -> '_2330.CVTPulley':
        '''CVTPulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2330.CVTPulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to CVTPulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_cvt_pulley.setter
    def selected_design_entity_of_type_cvt_pulley(self, value: '_2330.CVTPulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling(self) -> '_2331.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'SelectedDesignEntity' is the original name of this property.'''

        if _2331.PartToPartShearCoupling.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling(self, value: '_2331.PartToPartShearCoupling'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self) -> '_2332.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2332.PartToPartShearCouplingHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_part_to_part_shear_coupling_half.setter
    def selected_design_entity_of_type_part_to_part_shear_coupling_half(self, value: '_2332.PartToPartShearCouplingHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_pulley(self) -> '_2333.Pulley':
        '''Pulley: 'SelectedDesignEntity' is the original name of this property.'''

        if _2333.Pulley.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Pulley. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_pulley.setter
    def selected_design_entity_of_type_pulley(self, value: '_2333.Pulley'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring(self) -> '_2339.RollingRing':
        '''RollingRing: 'SelectedDesignEntity' is the original name of this property.'''

        if _2339.RollingRing.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRing. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_rolling_ring.setter
    def selected_design_entity_of_type_rolling_ring(self, value: '_2339.RollingRing'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_rolling_ring_assembly(self) -> '_2340.RollingRingAssembly':
        '''RollingRingAssembly: 'SelectedDesignEntity' is the original name of this property.'''

        if _2340.RollingRingAssembly.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to RollingRingAssembly. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_rolling_ring_assembly.setter
    def selected_design_entity_of_type_rolling_ring_assembly(self, value: '_2340.RollingRingAssembly'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_shaft_hub_connection(self) -> '_2341.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedDesignEntity' is the original name of this property.'''

        if _2341.ShaftHubConnection.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to ShaftHubConnection. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_shaft_hub_connection.setter
    def selected_design_entity_of_type_shaft_hub_connection(self, value: '_2341.ShaftHubConnection'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper(self) -> '_2343.SpringDamper':
        '''SpringDamper: 'SelectedDesignEntity' is the original name of this property.'''

        if _2343.SpringDamper.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamper. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spring_damper.setter
    def selected_design_entity_of_type_spring_damper(self, value: '_2343.SpringDamper'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_spring_damper_half(self) -> '_2344.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2344.SpringDamperHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SpringDamperHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_spring_damper_half.setter
    def selected_design_entity_of_type_spring_damper_half(self, value: '_2344.SpringDamperHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser(self) -> '_2345.Synchroniser':
        '''Synchroniser: 'SelectedDesignEntity' is the original name of this property.'''

        if _2345.Synchroniser.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to Synchroniser. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_synchroniser.setter
    def selected_design_entity_of_type_synchroniser(self, value: '_2345.Synchroniser'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_half(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedDesignEntity' is the original name of this property.'''

        if _2347.SynchroniserHalf.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserHalf. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_synchroniser_half.setter
    def selected_design_entity_of_type_synchroniser_half(self, value: '_2347.SynchroniserHalf'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_part(self) -> '_2348.SynchroniserPart':
        '''SynchroniserPart: 'SelectedDesignEntity' is the original name of this property.'''

        if _2348.SynchroniserPart.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserPart. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_synchroniser_part.setter
    def selected_design_entity_of_type_synchroniser_part(self, value: '_2348.SynchroniserPart'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_synchroniser_sleeve(self) -> '_2349.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedDesignEntity' is the original name of this property.'''

        if _2349.SynchroniserSleeve.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_synchroniser_sleeve.setter
    def selected_design_entity_of_type_synchroniser_sleeve(self, value: '_2349.SynchroniserSleeve'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter(self) -> '_2350.TorqueConverter':
        '''TorqueConverter: 'SelectedDesignEntity' is the original name of this property.'''

        if _2350.TorqueConverter.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverter. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_torque_converter.setter
    def selected_design_entity_of_type_torque_converter(self, value: '_2350.TorqueConverter'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_pump(self) -> '_2351.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedDesignEntity' is the original name of this property.'''

        if _2351.TorqueConverterPump.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterPump. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_torque_converter_pump.setter
    def selected_design_entity_of_type_torque_converter_pump(self, value: '_2351.TorqueConverterPump'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def selected_design_entity_of_type_torque_converter_turbine(self) -> '_2353.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedDesignEntity' is the original name of this property.'''

        if _2353.TorqueConverterTurbine.TYPE not in self.wrapped.SelectedDesignEntity.__class__.__mro__:
            raise CastException('Failed to cast selected_design_entity to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.SelectedDesignEntity.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SelectedDesignEntity.__class__)(self.wrapped.SelectedDesignEntity) if self.wrapped.SelectedDesignEntity is not None else None

    @selected_design_entity_of_type_torque_converter_turbine.setter
    def selected_design_entity_of_type_torque_converter_turbine(self, value: '_2353.TorqueConverterTurbine'):
        value = value.wrapped if value else None
        self.wrapped.SelectedDesignEntity = value

    @property
    def active_design(self) -> '_1950.Design':
        '''Design: 'ActiveDesign' is the original name of this property.'''

        return constructor.new(_1950.Design)(self.wrapped.ActiveDesign) if self.wrapped.ActiveDesign is not None else None

    @active_design.setter
    def active_design(self, value: '_1950.Design'):
        value = value.wrapped if value else None
        self.wrapped.ActiveDesign = value

    @property
    def open_designs(self) -> 'List[_1950.Design]':
        '''List[Design]: 'OpenDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OpenDesigns, constructor.new(_1950.Design))
        return value

    @property
    def restart_geometry_modeller_flag(self) -> 'bool':
        '''bool: 'RestartGeometryModellerFlag' is the original name of this property.'''

        return self.wrapped.RestartGeometryModellerFlag

    @restart_geometry_modeller_flag.setter
    def restart_geometry_modeller_flag(self, value: 'bool'):
        self.wrapped.RestartGeometryModellerFlag = bool(value) if value else False

    @property
    def geometry_modeller_process_id(self) -> 'int':
        '''int: 'GeometryModellerProcessID' is the original name of this property.'''

        return self.wrapped.GeometryModellerProcessID

    @geometry_modeller_process_id.setter
    def geometry_modeller_process_id(self, value: 'int'):
        self.wrapped.GeometryModellerProcessID = int(value) if value else 0

    @property
    def restart_geometry_modeller_save_file(self) -> 'str':
        '''str: 'RestartGeometryModellerSaveFile' is the original name of this property.'''

        return self.wrapped.RestartGeometryModellerSaveFile

    @restart_geometry_modeller_save_file.setter
    def restart_geometry_modeller_save_file(self, value: 'str'):
        self.wrapped.RestartGeometryModellerSaveFile = str(value) if value else ''

    @property
    def color_of_new_problem_node_group(self) -> 'Color':
        '''Color: 'ColorOfNewProblemNodeGroup' is the original name of this property.'''

        value = conversion.pn_to_mp_color(self.wrapped.ColorOfNewProblemNodeGroup)
        return value

    @color_of_new_problem_node_group.setter
    def color_of_new_problem_node_group(self, value: 'Color'):
        value = value if value else None
        value = conversion.mp_to_pn_color(value)
        self.wrapped.ColorOfNewProblemNodeGroup = value

    @property
    def name_of_new_problem_node_group(self) -> 'str':
        '''str: 'NameOfNewProblemNodeGroup' is the original name of this property.'''

        return self.wrapped.NameOfNewProblemNodeGroup

    @name_of_new_problem_node_group.setter
    def name_of_new_problem_node_group(self, value: 'str'):
        self.wrapped.NameOfNewProblemNodeGroup = str(value) if value else ''

    @property
    def positions_of_problem_node_group(self) -> 'List[Vector3D]':
        '''List[Vector3D]: 'PositionsOfProblemNodeGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PositionsOfProblemNodeGroup, Vector3D)
        return value

    @property
    def operation_mode(self) -> '_1564.OperationMode':
        '''OperationMode: 'OperationMode' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OperationMode)
        return constructor.new(_1564.OperationMode)(value) if value is not None else None

    @operation_mode.setter
    def operation_mode(self, value: '_1564.OperationMode'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OperationMode = value

    @property
    def is_connected_to_geometry_modeller(self) -> 'bool':
        '''bool: 'IsConnectedToGeometryModeller' is the original name of this property.'''

        return self.wrapped.IsConnectedToGeometryModeller

    @is_connected_to_geometry_modeller.setter
    def is_connected_to_geometry_modeller(self, value: 'bool'):
        self.wrapped.IsConnectedToGeometryModeller = bool(value) if value else False

    @property
    def process_id(self) -> 'int':
        '''int: 'ProcessId' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProcessId

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ReportNames, str)
        return value

    @staticmethod
    def get_mastagui(process_id: 'int') -> 'MASTAGUI':
        ''' 'GetMASTAGUI' is the original name of this method.

        Args:
            process_id (int)

        Returns:
            mastapy.system_model_gui.MASTAGUI
        '''

        process_id = int(process_id)
        method_result = MASTAGUI.TYPE.GetMASTAGUI(process_id if process_id else 0)
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def resume(self):
        ''' 'Resume' is the original name of this method.'''

        self.wrapped.Resume()

    def pause(self):
        ''' 'Pause' is the original name of this method.'''

        self.wrapped.Pause()

    def start_remoting(self):
        ''' 'StartRemoting' is the original name of this method.'''

        self.wrapped.StartRemoting()

    def stop_remoting(self):
        ''' 'StopRemoting' is the original name of this method.'''

        self.wrapped.StopRemoting()

    def open_design_in_new_tab(self, design: '_1950.Design'):
        ''' 'OpenDesignInNewTab' is the original name of this method.

        Args:
            design (mastapy.system_model.Design)
        '''

        self.wrapped.OpenDesignInNewTab(design.wrapped if design else None)

    def select_tab(self, tab_text: 'str'):
        ''' 'SelectTab' is the original name of this method.

        Args:
            tab_text (str)
        '''

        tab_text = str(tab_text)
        self.wrapped.SelectTab(tab_text if tab_text else '')

    def move_selected_component(self, origin: 'Vector3D', axis: 'Vector3D'):
        ''' 'MoveSelectedComponent' is the original name of this method.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        '''

        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        self.wrapped.MoveSelectedComponent(origin, axis)

    def run_command(self, command: 'str'):
        ''' 'RunCommand' is the original name of this method.

        Args:
            command (str)
        '''

        command = str(command)
        self.wrapped.RunCommand(command if command else '')

    def add_line_from_geometry_modeller(self, circles_on_axis: '_1294.CirclesOnAxis'):
        ''' 'AddLineFromGeometryModeller' is the original name of this method.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        '''

        self.wrapped.AddLineFromGeometryModeller(circles_on_axis.wrapped if circles_on_axis else None)

    def show_boxes(self, small_box: 'List[Vector3D]', big_box: 'List[Vector3D]'):
        ''' 'ShowBoxes' is the original name of this method.

        Args:
            small_box (List[Vector3D])
            big_box (List[Vector3D])
        '''

        small_box = conversion.mp_to_pn_objects_in_list(small_box)
        big_box = conversion.mp_to_pn_objects_in_list(big_box)
        self.wrapped.ShowBoxes(small_box, big_box)

    def circle_pairs_from_geometry_modeller(self, preselection_circles: '_1294.CirclesOnAxis', selected_circles: 'List[_1294.CirclesOnAxis]'):
        ''' 'CirclePairsFromGeometryModeller' is the original name of this method.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        '''

        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        self.wrapped.CirclePairsFromGeometryModeller(preselection_circles.wrapped if preselection_circles else None, selected_circles)

    def add_fe_substructure_from_data(self, vertices_and_facets: '_1313.FacetedBody', dimensions: 'Dict[str, _151.SpaceClaimDimension]', moniker: 'str'):
        ''' 'AddFESubstructureFromData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.SpaceClaimDimension])
            moniker (str)
        '''

        moniker = str(moniker)
        self.wrapped.AddFESubstructureFromData(vertices_and_facets.wrapped if vertices_and_facets else None, dimensions, moniker if moniker else '')

    def add_fe_substructure_from_file(self, length_scale: 'float', stl_file_name: 'str', dimensions: 'Dict[str, _151.SpaceClaimDimension]'):
        ''' 'AddFESubstructureFromFile' is the original name of this method.

        Args:
            length_scale (float)
            stl_file_name (str)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.SpaceClaimDimension])
        '''

        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        self.wrapped.AddFESubstructureFromFile(length_scale if length_scale else 0.0, stl_file_name if stl_file_name else '', dimensions)

    def flag_message_received(self):
        ''' 'FlagMessageReceived' is the original name of this method.'''

        self.wrapped.FlagMessageReceived()

    def geometry_modeller_document_loaded(self):
        ''' 'GeometryModellerDocumentLoaded' is the original name of this method.'''

        self.wrapped.GeometryModellerDocumentLoaded()

    def set_error(self, error: 'str'):
        ''' 'SetError' is the original name of this method.

        Args:
            error (str)
        '''

        error = str(error)
        self.wrapped.SetError(error if error else '')

    def new_dimensions(self, dimensions: 'Dict[str, _151.SpaceClaimDimension]'):
        ''' 'NewDimensions' is the original name of this method.

        Args:
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.SpaceClaimDimension])
        '''

        self.wrapped.NewDimensions(dimensions)

    def create_geometry_modeller_dimension(self) -> '_151.SpaceClaimDimension':
        ''' 'CreateGeometryModellerDimension' is the original name of this method.

        Returns:
            mastapy.nodal_analysis.geometry_modeller_link.SpaceClaimDimension
        '''

        method_result = self.wrapped.CreateGeometryModellerDimension()
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def new_mesh_data(self, vertices_and_facets: '_1313.FacetedBody'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
        '''

        self.wrapped.NewMeshData.Overloads[_FACETED_BODY](vertices_and_facets.wrapped if vertices_and_facets else None)

    def new_mesh_data_from_file(self, stl_file_name: 'str'):
        ''' 'NewMeshData' is the original name of this method.

        Args:
            stl_file_name (str)
        '''

        stl_file_name = str(stl_file_name)
        self.wrapped.NewMeshData.Overloads[_STRING](stl_file_name if stl_file_name else '')

    def create_new_circles_on_axis(self) -> '_1294.CirclesOnAxis':
        ''' 'CreateNewCirclesOnAxis' is the original name of this method.

        Returns:
            mastapy.math_utility.CirclesOnAxis
        '''

        method_result = self.wrapped.CreateNewCirclesOnAxis()
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

    def create_new_faceted_body(self) -> '_1313.FacetedBody':
        ''' 'CreateNewFacetedBody' is the original name of this method.

        Returns:
            mastapy.math_utility.FacetedBody
        '''

        method_result = self.wrapped.CreateNewFacetedBody()
        return constructor.new_override(method_result.__class__)(method_result) if method_result is not None else None

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
