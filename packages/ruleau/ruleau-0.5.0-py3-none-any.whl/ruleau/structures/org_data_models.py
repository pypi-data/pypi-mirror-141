from typing import List, Literal, TypedDict, Union

SchemeTypes = Literal["string", "integer", "float", "date"]


class OrganisationalData(TypedDict):
    key: str
    value: Union[str, int, float]


class OrganisationalSchemeID(TypedDict):
    id: str


class OrganisationalScheme(OrganisationalSchemeID):
    display_name: str
    display_default: bool
    type: SchemeTypes


class UiLayoutMetadata(TypedDict):
    case_org_data_order: List[OrganisationalSchemeID]
    override_org_data_order: List[OrganisationalSchemeID]
