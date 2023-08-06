'''_3923.py

ClutchConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2087
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3789
from mastapy.system_model.analyses_and_results.power_flows.compound import _3939
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ClutchConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionCompoundPowerFlow',)


class ClutchConnectionCompoundPowerFlow(_3939.CouplingConnectionCompoundPowerFlow):
    '''ClutchConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2087.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def connection_design(self) -> '_2087.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_3789.ClutchConnectionPowerFlow]':
        '''List[ClutchConnectionPowerFlow]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCasesReady, constructor.new(_3789.ClutchConnectionPowerFlow))
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_3789.ClutchConnectionPowerFlow]':
        '''List[ClutchConnectionPowerFlow]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAnalysisCases, constructor.new(_3789.ClutchConnectionPowerFlow))
        return value
