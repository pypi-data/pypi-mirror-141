'''_3602.py

SpiralBevelGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2287
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6677
from mastapy.system_model.analyses_and_results.stability_analyses import _3603, _3601, _3518
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SpiralBevelGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetStabilityAnalysis',)


class SpiralBevelGearSetStabilityAnalysis(_3518.BevelGearSetStabilityAnalysis):
    '''SpiralBevelGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2287.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2287.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6677.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6677.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def spiral_bevel_gears_stability_analysis(self) -> 'List[_3603.SpiralBevelGearStabilityAnalysis]':
        '''List[SpiralBevelGearStabilityAnalysis]: 'SpiralBevelGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsStabilityAnalysis, constructor.new(_3603.SpiralBevelGearStabilityAnalysis))
        return value

    @property
    def spiral_bevel_meshes_stability_analysis(self) -> 'List[_3601.SpiralBevelGearMeshStabilityAnalysis]':
        '''List[SpiralBevelGearMeshStabilityAnalysis]: 'SpiralBevelMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesStabilityAnalysis, constructor.new(_3601.SpiralBevelGearMeshStabilityAnalysis))
        return value
