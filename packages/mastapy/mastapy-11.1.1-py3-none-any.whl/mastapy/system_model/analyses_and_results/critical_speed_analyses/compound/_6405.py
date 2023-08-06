'''_6405.py

BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2259
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6403, _6404, _6410
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6274
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundCriticalSpeedAnalysis',)


class BevelDifferentialGearSetCompoundCriticalSpeedAnalysis(_6410.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''BevelDifferentialGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2259.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2259.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def bevel_differential_gears_compound_critical_speed_analysis(self) -> 'List[_6403.BevelDifferentialGearCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearCompoundCriticalSpeedAnalysis]: 'BevelDifferentialGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundCriticalSpeedAnalysis, constructor.new(_6403.BevelDifferentialGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def bevel_differential_meshes_compound_critical_speed_analysis(self) -> 'List[_6404.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis]: 'BevelDifferentialMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6404.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6274.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6274.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6274.BevelDifferentialGearSetCriticalSpeedAnalysis]':
        '''List[BevelDifferentialGearSetCriticalSpeedAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6274.BevelDifferentialGearSetCriticalSpeedAnalysis))
        return value
