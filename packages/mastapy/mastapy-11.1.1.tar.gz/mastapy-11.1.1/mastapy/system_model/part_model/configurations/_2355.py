'''_2355.py

ActiveFESubstructureSelectionGroup
'''


from mastapy.system_model.part_model.configurations import _2360, _2354
from mastapy.system_model.part_model import _2197
from mastapy.system_model.fe import _2127
from mastapy._internal.python_net import python_net_import

_ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveFESubstructureSelectionGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveFESubstructureSelectionGroup',)


class ActiveFESubstructureSelectionGroup(_2360.PartDetailConfiguration['_2354.ActiveFESubstructureSelection', '_2197.FEPart', '_2127.FESubstructure']):
    '''ActiveFESubstructureSelectionGroup

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_FE_SUBSTRUCTURE_SELECTION_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveFESubstructureSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
