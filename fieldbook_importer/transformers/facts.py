from fieldbook_importer.utils import (
    clean_string,
)
from nameparser import HumanName


def make_person_transformer(name_field):
    def transform_person(item):
        name_string = item.get(name_field)
        if not name_string:
            return None
        name = HumanName(name_string)
        return {
            "given_name": name.first,
            "additional_name": name.middle,
            "family_name": name.last
        }
    return transform_person

transform_person_poc = make_person_transformer("points_of_contact_name")


def make_organization_transformer(name_field):
    def transform_organization(item):
        return {
            'name': clean_string(item.get(name_field)),
        }
    return transform_organization

transform_organization = make_organization_transformer("organization_name")
