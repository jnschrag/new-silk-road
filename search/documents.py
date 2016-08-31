from elasticsearch_dsl import (
    DocType, field,
)


class CategoryDoc(field.InnerObjectWrapper):
    name = field.String()


class CountryDoc(field.InnerObjectWrapper):
    name = field.String()


class InfrastructureTypeDoc(field.InnerObjectWrapper):
    name = field.String()


class OrganizationDoc(DocType):
    identifier = field.String()
    name = field.String()
    countries = field.Nested(doc_class=CountryDoc, properties={'name': field.String()})


class PositionDoc(field.InnerObjectWrapper):
    title = field.String()
    organization = field.Object(
        doc_class=OrganizationDoc,
        properties={
            'name': field.String(),
        }
    )


class PersonDoc(DocType):
    given_name = field.String()
    additional_name = field.String()
    family_name = field.String()
    description = field.String()
    citizenships = field.Nested(doc_class=CountryDoc, properties={'name': field.String()})
    position_set = field.Nested(
        doc_class=PositionDoc,
        properties={
            'title': field.String(),
            'organization': field.Object(properties={'name': field.String()})
        }
    )


class ProjectDoc(DocType):
    identifier = field.String()
    name = field.String()
    alternate_name = field.String()
    description = field.String()
    countries = field.Nested(doc_class=CountryDoc, properties={'name': field.String()})
    infrastructure_type = field.Nested(doc_class=InfrastructureTypeDoc, properties={'name': field.String()})


class EntryDoc(DocType):
    title = field.String()
    author = field.String()
    content = field.String()
    description = field.String()
    publication_date = field.Date()
    categories = field.Nested(doc_class=CategoryDoc, properties={'name': field.String()})
