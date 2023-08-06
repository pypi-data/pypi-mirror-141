'''_3575.py

KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2284
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6640
from mastapy.system_model.analyses_and_results.stability_analyses import _3576, _3574, _3569
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis(_3569.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2284.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2284.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6640.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6640.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_stability_analysis(self) -> 'List[_3576.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsStabilityAnalysis, constructor.new(_3576.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_stability_analysis(self) -> 'List[_3574.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesStabilityAnalysis, constructor.new(_3574.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis))
        return value
