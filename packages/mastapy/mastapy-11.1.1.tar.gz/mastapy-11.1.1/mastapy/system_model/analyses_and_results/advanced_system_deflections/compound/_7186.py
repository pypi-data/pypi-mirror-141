'''_7186.py

GearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.gears.rating import _329
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _342
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _416
from mastapy.gears.rating.cylindrical import _428
from mastapy.gears.rating.conical import _502
from mastapy.gears.rating.concept import _513
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7055
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7224
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundAdvancedSystemDeflection',)


class GearSetCompoundAdvancedSystemDeflection(_7224.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    '''GearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_duty_cycle_rating(self) -> '_329.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _329.GearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def gear_duty_cycle_rating_of_type_worm_gear_set_duty_cycle_rating(self) -> '_342.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _342.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def gear_duty_cycle_rating_of_type_face_gear_set_duty_cycle_rating(self) -> '_416.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _416.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def gear_duty_cycle_rating_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_428.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _428.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def gear_duty_cycle_rating_of_type_conical_gear_set_duty_cycle_rating(self) -> '_502.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def gear_duty_cycle_rating_of_type_concept_gear_set_duty_cycle_rating(self) -> '_513.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _513.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new_override(self.wrapped.GearDutyCycleRating.__class__)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating is not None else None

    @property
    def assembly_analysis_cases(self) -> 'List[_7055.GearSetAdvancedSystemDeflection]':
        '''List[GearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_7055.GearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7055.GearSetAdvancedSystemDeflection]':
        '''List[GearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_7055.GearSetAdvancedSystemDeflection))
        return value
