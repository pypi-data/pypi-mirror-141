'''_2277.py

HypoidGear
'''


from mastapy.gears.gear_designs.hypoid import _943
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2256
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGear',)


class HypoidGear(_2256.AGMAGleasonConicalGear):
    '''HypoidGear

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_design(self) -> '_943.HypoidGearDesign':
        '''HypoidGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_943.HypoidGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign is not None else None

    @property
    def hypoid_gear_design(self) -> '_943.HypoidGearDesign':
        '''HypoidGearDesign: 'HypoidGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_943.HypoidGearDesign)(self.wrapped.HypoidGearDesign) if self.wrapped.HypoidGearDesign is not None else None
