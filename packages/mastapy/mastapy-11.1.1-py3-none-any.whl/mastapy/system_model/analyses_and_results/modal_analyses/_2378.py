'''_2378.py

ModalAnalysis
'''


from mastapy.system_model.analyses_and_results.dynamic_analyses import _2369
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3291
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.stability_analyses import _2373
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4358
from mastapy.system_model.analyses_and_results.modal_analyses import _2372, _4904, _4902
from mastapy.system_model.analyses_and_results.harmonic_analyses import _2371
from mastapy.system_model.analyses_and_results.analysis_cases import _7270
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysis',)


class ModalAnalysis(_7270.StaticLoadAnalysisCase):
    '''ModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analysis_results(self) -> '_2369.DynamicAnalysis':
        '''DynamicAnalysis: 'ModalAnalysisResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2369.DynamicAnalysis.TYPE not in self.wrapped.ModalAnalysisResults.__class__.__mro__:
            raise CastException('Failed to cast modal_analysis_results to DynamicAnalysis. Expected: {}.'.format(self.wrapped.ModalAnalysisResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ModalAnalysisResults.__class__)(self.wrapped.ModalAnalysisResults) if self.wrapped.ModalAnalysisResults is not None else None

    @property
    def analysis_settings(self) -> '_4904.ModalAnalysisOptions':
        '''ModalAnalysisOptions: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4904.ModalAnalysisOptions)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings is not None else None

    @property
    def bar_model_export(self) -> '_4902.ModalAnalysisBarModelFEExportOptions':
        '''ModalAnalysisBarModelFEExportOptions: 'BarModelExport' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4902.ModalAnalysisBarModelFEExportOptions)(self.wrapped.BarModelExport) if self.wrapped.BarModelExport is not None else None
