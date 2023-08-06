'''_5761.py

KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2282
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6637
from mastapy.system_model.analyses_and_results.system_deflections import _2510
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5759, _5760, _5758
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis(_5758.KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2282.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2282.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def assembly_load_case(self) -> '_6637.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6637.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase is not None else None

    @property
    def system_deflection_results(self) -> '_2510.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2510.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults is not None else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5759.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5759.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_harmonic_analysis(self) -> 'List[_5759.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsHarmonicAnalysis, constructor.new(_5759.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5760.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5760.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_harmonic_analysis(self) -> 'List[_5760.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesHarmonicAnalysis, constructor.new(_5760.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis))
        return value
