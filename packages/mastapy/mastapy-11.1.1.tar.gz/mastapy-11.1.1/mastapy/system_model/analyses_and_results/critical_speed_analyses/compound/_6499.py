'''_6499.py

StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2289
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6497, _6498, _6410
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6370
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis',)


class StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis(_6410.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2289.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2289.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def straight_bevel_diff_gears_compound_critical_speed_analysis(self) -> 'List[_6497.StraightBevelDiffGearCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundCriticalSpeedAnalysis, constructor.new(_6497.StraightBevelDiffGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_critical_speed_analysis(self) -> 'List[_6498.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis]: 'StraightBevelDiffMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6498.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6370.StraightBevelDiffGearSetCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6370.StraightBevelDiffGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6370.StraightBevelDiffGearSetCriticalSpeedAnalysis]':
        '''List[StraightBevelDiffGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6370.StraightBevelDiffGearSetCriticalSpeedAnalysis))
        return value
