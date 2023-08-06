'''_241.py

MaterialDatabase
'''


from typing import Generic, TypeVar

from mastapy.utility.databases import _1599
from mastapy.materials import _240
from mastapy._internal.python_net import python_net_import

_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'MaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('MaterialDatabase',)


T = TypeVar('T', bound='_240.Material')


class MaterialDatabase(_1599.NamedDatabase['T'], Generic[T]):
    '''MaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
