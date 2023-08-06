'''_2495.py

FEPartSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2197
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6605
from mastapy.system_model.analyses_and_results.power_flows import _3825
from mastapy.nodal_analysis.component_mode_synthesis import _208
from mastapy.nodal_analysis import _75
from mastapy.math_utility.measured_vectors import _1366, _1362
from mastapy.system_model.fe import _2154
from mastapy.system_model.analyses_and_results.system_deflections import _2429
from mastapy._internal.python_net import python_net_import

_FE_PART_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FEPartSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartSystemDeflection',)


class FEPartSystemDeflection(_2429.AbstractShaftOrHousingSystemDeflection):
    '''FEPartSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FE_PART_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2197.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign is not None else None

    @property
    def component_load_case(self) -> '_6605.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6605.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase is not None else None

    @property
    def power_flow_results(self) -> '_3825.FEPartPowerFlow':
        '''FEPartPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3825.FEPartPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults is not None else None

    @property
    def full_fe_results(self) -> '_208.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_208.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults is not None else None

    @property
    def stiffness_in_world_coordinate_system_mn_rad(self) -> '_75.NodalMatrix':
        '''NodalMatrix: 'StiffnessInWorldCoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_75.NodalMatrix)(self.wrapped.StiffnessInWorldCoordinateSystemMNRad) if self.wrapped.StiffnessInWorldCoordinateSystemMNRad is not None else None

    @property
    def mass_in_world_coordinate_system_mn_rad_s_kg(self) -> '_75.NodalMatrix':
        '''NodalMatrix: 'MassInWorldCoordinateSystemMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_75.NodalMatrix)(self.wrapped.MassInWorldCoordinateSystemMNRadSKg) if self.wrapped.MassInWorldCoordinateSystemMNRadSKg is not None else None

    @property
    def planetaries(self) -> 'List[FEPartSystemDeflection]':
        '''List[FEPartSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartSystemDeflection))
        return value

    @property
    def applied_internal_forces_in_world_coordinate_system(self) -> 'List[_1366.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'AppliedInternalForcesInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AppliedInternalForcesInWorldCoordinateSystem, constructor.new(_1366.VectorWithLinearAndAngularComponents))
        return value

    @property
    def node_results_in_shaft_coordinate_system(self) -> 'List[_1362.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'NodeResultsInShaftCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsInShaftCoordinateSystem, constructor.new(_1362.ForceAndDisplacementResults))
        return value

    @property
    def export(self) -> '_2154.SystemDeflectionFEExportOptions':
        '''SystemDeflectionFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2154.SystemDeflectionFEExportOptions)(self.wrapped.Export) if self.wrapped.Export is not None else None

    def export_displacements(self):
        ''' 'ExportDisplacements' is the original name of this method.'''

        self.wrapped.ExportDisplacements()

    def export_forces(self):
        ''' 'ExportForces' is the original name of this method.'''

        self.wrapped.ExportForces()
