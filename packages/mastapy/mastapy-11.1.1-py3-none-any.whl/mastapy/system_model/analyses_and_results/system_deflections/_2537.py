'''_2537.py

RollingRingSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2339
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6668
from mastapy.system_model.analyses_and_results.power_flows import _3864
from mastapy.system_model.analyses_and_results.system_deflections import _2468
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'RollingRingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingSystemDeflection',)


class RollingRingSystemDeflection(_2468.CouplingHalfSystemDeflection):
    '''RollingRingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2339.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2339.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6668.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6668.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3864.RollingRingPowerFlow':
        '''RollingRingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3864.RollingRingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingSystemDeflection]':
        '''List[RollingRingSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingSystemDeflection))
        return value
