'''_2638.py

CylindricalGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2269, _2285
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical import _428, _429
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1060
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2636, _2637, _2650
from mastapy.system_model.analyses_and_results.system_deflections import _2482
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CylindricalGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundSystemDeflection',)


class CylindricalGearSetCompoundSystemDeflection(_2650.GearSetCompoundSystemDeflection):
    '''CylindricalGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2269.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2269.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def assembly_design(self) -> '_2269.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2269.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign is not None else None

    @property
    def cylindrical_gear_set_rating_using_basic_ltca(self) -> '_428.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetRatingUsingBasicLTCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_428.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetRatingUsingBasicLTCA) if self.wrapped.CylindricalGearSetRatingUsingBasicLTCA is not None else None

    @property
    def cylindrical_gear_set_rating(self) -> '_428.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'CylindricalGearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_428.CylindricalGearSetDutyCycleRating)(self.wrapped.CylindricalGearSetRating) if self.wrapped.CylindricalGearSetRating is not None else None

    @property
    def load_case_rating_with_lowest_safety_factor_for_scuffing(self) -> '_429.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'LoadCaseRatingWithLowestSafetyFactorForScuffing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_429.CylindricalGearSetRating)(self.wrapped.LoadCaseRatingWithLowestSafetyFactorForScuffing) if self.wrapped.LoadCaseRatingWithLowestSafetyFactorForScuffing is not None else None

    @property
    def basic_ltca_results(self) -> '_1060.CylindricalGearSetMicroGeometryDutyCycle':
        '''CylindricalGearSetMicroGeometryDutyCycle: 'BasicLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1060.CylindricalGearSetMicroGeometryDutyCycle)(self.wrapped.BasicLTCAResults) if self.wrapped.BasicLTCAResults is not None else None

    @property
    def basic_ltca_results_only_first_planetary_mesh(self) -> '_1060.CylindricalGearSetMicroGeometryDutyCycle':
        '''CylindricalGearSetMicroGeometryDutyCycle: 'BasicLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1060.CylindricalGearSetMicroGeometryDutyCycle)(self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.BasicLTCAResultsOnlyFirstPlanetaryMesh is not None else None

    @property
    def advanced_ltca_results(self) -> '_1060.CylindricalGearSetMicroGeometryDutyCycle':
        '''CylindricalGearSetMicroGeometryDutyCycle: 'AdvancedLTCAResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1060.CylindricalGearSetMicroGeometryDutyCycle)(self.wrapped.AdvancedLTCAResults) if self.wrapped.AdvancedLTCAResults is not None else None

    @property
    def advanced_ltca_results_only_first_planetary_mesh(self) -> '_1060.CylindricalGearSetMicroGeometryDutyCycle':
        '''CylindricalGearSetMicroGeometryDutyCycle: 'AdvancedLTCAResultsOnlyFirstPlanetaryMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1060.CylindricalGearSetMicroGeometryDutyCycle)(self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh) if self.wrapped.AdvancedLTCAResultsOnlyFirstPlanetaryMesh is not None else None

    @property
    def cylindrical_gears_compound_system_deflection(self) -> 'List[_2636.CylindricalGearCompoundSystemDeflection]':
        '''List[CylindricalGearCompoundSystemDeflection]: 'CylindricalGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundSystemDeflection, constructor.new(_2636.CylindricalGearCompoundSystemDeflection))
        return value

    @property
    def cylindrical_meshes_compound_system_deflection(self) -> 'List[_2637.CylindricalGearMeshCompoundSystemDeflection]':
        '''List[CylindricalGearMeshCompoundSystemDeflection]: 'CylindricalMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundSystemDeflection, constructor.new(_2637.CylindricalGearMeshCompoundSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2482.CylindricalGearSetSystemDeflectionWithLTCAResults]':
        '''List[CylindricalGearSetSystemDeflectionWithLTCAResults]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2482.CylindricalGearSetSystemDeflectionWithLTCAResults))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2482.CylindricalGearSetSystemDeflectionWithLTCAResults]':
        '''List[CylindricalGearSetSystemDeflectionWithLTCAResults]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2482.CylindricalGearSetSystemDeflectionWithLTCAResults))
        return value
