'''_5674.py

BearingHarmonicAnalysis
'''


from typing import List

from mastapy.bearings.bearing_results.rolling import _1824
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2185
from mastapy.system_model.analyses_and_results.static_loads import _6537
from mastapy.system_model.analyses_and_results.system_deflections import _2436
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5703
from mastapy._internal.python_net import python_net_import

_BEARING_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'BearingHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingHarmonicAnalysis',)


class BearingHarmonicAnalysis(_5703.ConnectorHarmonicAnalysis):
    '''BearingHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rolling_bearing_speed_results(self) -> '_1824.RollingBearingSpeedResults':
        '''RollingBearingSpeedResults: 'RollingBearingSpeedResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1824.RollingBearingSpeedResults)(self.wrapped.RollingBearingSpeedResults) if self.wrapped.RollingBearingSpeedResults is not None else None

    @property
    def component_design(self) -> '_2185.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6537.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6537.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2436.BearingSystemDeflection':
        '''BearingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2436.BearingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def planetaries(self) -> 'List[BearingHarmonicAnalysis]':
        '''List[BearingHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingHarmonicAnalysis))
        return value
