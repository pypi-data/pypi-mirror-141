'''_6689.py

SynchroniserHalfLoadCase
'''


from mastapy.system_model.part_model.couplings import _2347
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6691
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SynchroniserHalfLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfLoadCase',)


class SynchroniserHalfLoadCase(_6691.SynchroniserPartLoadCase):
    '''SynchroniserHalfLoadCase

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2347.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2347.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None
