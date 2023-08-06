from typing import Any, Dict, Set

from pydantic import BaseModel, root_validator

from tdm.abstract.json_schema import DocumentMetadataFields, FactMetadataFields


class MetadataModel(BaseModel):

    @root_validator(pre=True)  # works like a charm though (no warnings with different order, but root_validator breaks)
    @classmethod
    def add_other_field(cls, fields: dict) -> dict:
        other = fields.get('other') or {}
        cls._validate_other_field(set(fields.keys()), other)
        known_fields = set(cls.__fields__.keys())

        def pull_other_fields(flds: dict) -> dict:
            return {field: value for field, value in flds.items() if field not in known_fields}

        def pull_known_fields(flds: dict) -> dict:
            return {field: value for field, value in flds.items() if field in known_fields.difference({'other'})}

        fields_to_add = {**pull_known_fields(other), **pull_known_fields(fields)}
        other_to_add = {**pull_other_fields(other), **pull_other_fields(fields)}
        if other_to_add != {}:
            fields_to_add['other'] = other_to_add
        return fields_to_add

    def to_metadata(self) -> Dict[str, Any]:
        dict_view = self.dict(exclude_none=True)
        if 'other' in dict_view:
            other = dict_view['other']
            self._validate_other_field(self.__fields_set__, other)
            del dict_view['other']
            return {**dict_view, **other}
        else:
            return dict_view

    @staticmethod
    def _validate_other_field(set_fields: Set[str], other: dict) -> None:
        if any(field in set_fields for field in other):
            raise ValueError('Field conflict!')


class DocumentMetadataModel(DocumentMetadataFields, MetadataModel):
    pass


class FactMetadataModel(FactMetadataFields, MetadataModel):
    pass
