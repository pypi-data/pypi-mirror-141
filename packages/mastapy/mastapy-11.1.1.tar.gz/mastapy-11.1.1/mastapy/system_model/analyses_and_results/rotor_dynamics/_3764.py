'''_3764.py

ShaftForcedComplexShape
'''


from mastapy.system_model.analyses_and_results.rotor_dynamics import _3763
from mastapy.utility.units_and_measurements.measurements import _1458, _1411
from mastapy._internal.python_net import python_net_import

_SHAFT_FORCED_COMPLEX_SHAPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics', 'ShaftForcedComplexShape')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftForcedComplexShape',)


class ShaftForcedComplexShape(_3763.ShaftComplexShape['_1458.LengthVeryShort', '_1411.AngleSmall']):
    '''ShaftForcedComplexShape

    This is a mastapy class.
    '''

    TYPE = _SHAFT_FORCED_COMPLEX_SHAPE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftForcedComplexShape.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
