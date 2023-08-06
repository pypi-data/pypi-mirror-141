'''_996.py

CylindricalPlanetaryGearSetDesign
'''


from mastapy._internal import constructor
from mastapy.utility_gui.charts import (
    _1629, _1620, _1625, _1626
)
from mastapy._internal.cast_exception import CastException
from mastapy.math_utility import _1315
from mastapy.gears.gear_designs.cylindrical import _985
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalPlanetaryGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetaryGearSetDesign',)


class CylindricalPlanetaryGearSetDesign(_985.CylindricalGearSetDesign):
    '''CylindricalPlanetaryGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANETARY_GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetaryGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def equally_spaced_planets_are_assemblable(self) -> 'bool':
        '''bool: 'EquallySpacedPlanetsAreAssemblable' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquallySpacedPlanetsAreAssemblable

    @property
    def least_mesh_angle(self) -> 'float':
        '''float: 'LeastMeshAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LeastMeshAngle

    @property
    def planet_gear_phasing_chart(self) -> '_1629.TwoDChartDefinition':
        '''TwoDChartDefinition: 'PlanetGearPhasingChart' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1629.TwoDChartDefinition.TYPE not in self.wrapped.PlanetGearPhasingChart.__class__.__mro__:
            raise CastException('Failed to cast planet_gear_phasing_chart to TwoDChartDefinition. Expected: {}.'.format(self.wrapped.PlanetGearPhasingChart.__class__.__qualname__))

        return constructor.new_override(self.wrapped.PlanetGearPhasingChart.__class__)(self.wrapped.PlanetGearPhasingChart) if self.wrapped.PlanetGearPhasingChart is not None else None

    @property
    def planetary_sideband_fourier_series_for_rotating_planet_carrier(self) -> '_1315.FourierSeries':
        '''FourierSeries: 'PlanetarySidebandFourierSeriesForRotatingPlanetCarrier' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1315.FourierSeries)(self.wrapped.PlanetarySidebandFourierSeriesForRotatingPlanetCarrier) if self.wrapped.PlanetarySidebandFourierSeriesForRotatingPlanetCarrier is not None else None
