'''_2375.py

HarmonicAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5468
from mastapy.system_model.analyses_and_results.analysis_cases import _7257
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysis',)


class HarmonicAnalysis(_7257.CompoundAnalysisCase):
    '''HarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def time_to_run_single_excitations(self) -> 'float':
        '''float: 'TimeToRunSingleExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TimeToRunSingleExcitations

    @property
    def time_for_single_excitations_post_analysis(self) -> 'float':
        '''float: 'TimeForSingleExcitationsPostAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TimeForSingleExcitationsPostAnalysis

    @property
    def time_for_modal_analysis(self) -> 'float':
        '''float: 'TimeForModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TimeForModalAnalysis

    @property
    def harmonic_analyses_of_single_excitations(self) -> 'List[_5468.HarmonicAnalysisOfSingleExcitation]':
        '''List[HarmonicAnalysisOfSingleExcitation]: 'HarmonicAnalysesOfSingleExcitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HarmonicAnalysesOfSingleExcitations, constructor.new(_5468.HarmonicAnalysisOfSingleExcitation))
        return value
