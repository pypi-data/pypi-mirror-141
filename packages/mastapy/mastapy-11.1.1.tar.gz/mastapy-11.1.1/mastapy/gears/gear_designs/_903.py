'''_903.py

DesignConstraintCollectionDatabase
'''


from mastapy.utility.databases import _1599
from mastapy.gears.gear_designs import _904
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT_COLLECTION_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintCollectionDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintCollectionDatabase',)


class DesignConstraintCollectionDatabase(_1599.NamedDatabase['_904.DesignConstraintsCollection']):
    '''DesignConstraintCollectionDatabase

    This is a mastapy class.
    '''

    TYPE = _DESIGN_CONSTRAINT_COLLECTION_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignConstraintCollectionDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
