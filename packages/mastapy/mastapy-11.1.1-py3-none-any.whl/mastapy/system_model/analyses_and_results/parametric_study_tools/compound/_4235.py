'''_4235.py

GearCompoundParametricStudyTool
'''


from typing import List

from mastapy.gears.rating import _325
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _339
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _412
from mastapy.gears.rating.cylindrical import _419
from mastapy.gears.rating.conical import _499
from mastapy.gears.rating.concept import _509
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4096
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4254
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'GearCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundParametricStudyTool',)


class GearCompoundParametricStudyTool(_4254.MountableComponentCompoundParametricStudyTool):
    '''GearCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_results(self) -> '_325.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _325.GearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to GearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def gear_duty_cycle_results_of_type_worm_gear_duty_cycle_rating(self) -> '_339.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _339.WormGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def gear_duty_cycle_results_of_type_face_gear_duty_cycle_rating(self) -> '_412.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _412.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def gear_duty_cycle_results_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_419.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _419.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def gear_duty_cycle_results_of_type_conical_gear_duty_cycle_rating(self) -> '_499.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _499.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def gear_duty_cycle_results_of_type_concept_gear_duty_cycle_rating(self) -> '_509.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_results to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleResults.__class__)(self.wrapped.GearDutyCycleResults) if self.wrapped.GearDutyCycleResults is not None else None

    @property
    def component_analysis_cases(self) -> 'List[_4096.GearParametricStudyTool]':
        '''List[GearParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4096.GearParametricStudyTool))
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_4096.GearParametricStudyTool]':
        '''List[GearParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4096.GearParametricStudyTool))
        return value
