'''_6370.py

StraightBevelDiffGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2289
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6683
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6368, _6369, _6279
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'StraightBevelDiffGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCriticalSpeedAnalysis',)


class StraightBevelDiffGearSetCriticalSpeedAnalysis(_6279.BevelGearSetCriticalSpeedAnalysis):
    '''StraightBevelDiffGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2289.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6683.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6683.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def straight_bevel_diff_gears_critical_speed_analysis(self) -> 'List[_6368.StraightBevelDiffGearCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearCriticalSpeedAnalysis]: 'StraightBevelDiffGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCriticalSpeedAnalysis, constructor.new(_6368.StraightBevelDiffGearCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_critical_speed_analysis(self) -> 'List[_6369.StraightBevelDiffGearMeshCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearMeshCriticalSpeedAnalysis]: 'StraightBevelDiffMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCriticalSpeedAnalysis, constructor.new(_6369.StraightBevelDiffGearMeshCriticalSpeedAnalysis))
        return value
