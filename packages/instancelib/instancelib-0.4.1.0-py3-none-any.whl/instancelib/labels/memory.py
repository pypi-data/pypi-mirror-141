# Copyright (C) 2021 The InstanceLib Authors. All Rights Reserved.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import annotations

from typing import (Any, Dict, FrozenSet, Generic, Iterable, Optional,
                    Sequence, Set, Tuple, Union)

from ..instances import Instance
from ..typehints import KT, LT
from ..utils.func import list_unzip, union
from ..utils.to_key import to_key
from .base import LabelProvider


class MemoryLabelProvider(LabelProvider[KT, LT], Generic[KT, LT]):
    """A Memory based implementation to test and benchmark AL algorithms
    """
    _labelset: FrozenSet[LT]
    _labeldict: Dict[KT, Set[LT]]
    _labeldict_inv: Dict[LT, Set[KT]]

    def __init__(self, 
            labelset: Iterable[LT], 
            labeldict: Dict[KT, Set[LT]], 
            labeldict_inv: Optional[Dict[LT, Set[KT]]] = None) -> None:
        self._labelset = frozenset(labelset)
        self._labeldict = labeldict
        if labeldict_inv is None:
            self._labeldict_inv = {label: set() for label in self._labelset}
            for key in self._labeldict.keys():
                for label in self._labeldict[key]:
                    self._labeldict_inv[label].add(key)
        else:
            self._labeldict_inv = labeldict_inv

    @classmethod
    def from_data(
            cls, 
            labelset: Iterable[LT], 
            indices: Sequence[KT], 
            labels: Sequence[Iterable[LT]]
        ) -> MemoryLabelProvider[KT, LT]:
        labelset = frozenset(labelset)
        labeldict = {
            idx: set(labellist) for (idx, labellist) in zip(indices, labels)
        }
        labeldict_inv: Dict[LT, Set[KT]] = {label: set() for label in labelset}
        # Store all instances in a Dictionary<LT, Set[ID]>
        for key, labellist in labeldict.items():
            for label in labellist:
                labeldict_inv[label].add(key)
        return cls(labelset, labeldict, labeldict_inv)

    @classmethod
    def from_provider(cls, provider: LabelProvider[KT, LT]) -> MemoryLabelProvider[KT, LT]:
        labelset = provider.labelset
        labeldict_inv = {label: set(provider.get_instances_by_label(label)) for label in labelset}
        labeldict: Dict[KT, Set[LT]]= {}
        for label, key_list in labeldict_inv.items():
            for key in key_list:
                labeldict.setdefault(key, set()).add(label)
        return cls(labelset, labeldict, labeldict_inv)

    @classmethod
    def from_tuples(cls, predictions: Sequence[Tuple[KT, FrozenSet[LT]]]) -> MemoryLabelProvider[KT, LT]:
        _, labels = list_unzip(predictions)
        labelset = union(*labels)
        labeldict = {key: set(labeling) for (key, labeling) in predictions}
        provider = cls(labelset, labeldict, None)
        return  provider

    @property
    def labelset(self) -> FrozenSet[LT]:
        return self._labelset

    def remove_labels(self, instance: Union[KT, Instance[KT, Any, Any, Any]], *labels: LT):
        key = to_key(instance)
        if key not in self._labeldict:
            raise KeyError("Key {} is not found".format(key))
        for label in labels:
            self._labeldict[key].discard(label)
            self._labeldict_inv[label].discard(key)

    def set_labels(self, instance: Union[KT, Instance[KT, Any, Any, Any]], *labels: LT):
        key = to_key(instance)
        for label in labels:
            self._labeldict.setdefault(key, set()).add(label)
            self._labeldict_inv.setdefault(label, set()).add(key)

    def get_labels(self, instance: Union[KT, Instance[KT, Any, Any, Any]]) -> FrozenSet[LT]:
        key = to_key(instance)
        return frozenset(self._labeldict.setdefault(key, set()))

    def get_instances_by_label(self, label: LT) -> FrozenSet[KT]:
        return frozenset(self._labeldict_inv.setdefault(label, set()))

    def document_count(self, label: LT) -> int:
        return len(self.get_instances_by_label(label))
            
