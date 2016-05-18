# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 20:33
from __future__ import unicode_literals

import utilities.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import markymark.fields
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sources', '0004_auto_20160425_1251'),
        ('facts', '0001_initial'),
        ('locations', '0004_geometrystore_centroid'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfrastructureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=140)),
                ('slug', models.SlugField(allow_unicode=True, max_length=150)),
                ('notes', markymark.fields.MarkdownField(blank=True)),
                ('founding_date', models.DateField(blank=True, null=True, verbose_name='Founding/Signing Date')),
                ('appeared_year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='First Apperance Year')),
                ('appeared_month', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='First Apperance Month')),
                ('appeared_day', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='First Apperance Day')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('affiliated_events', models.ManyToManyField(blank=True, to='facts.Event')),
                ('affiliated_organizations', models.ManyToManyField(blank=True, to='facts.Organization')),
                ('affiliated_people', models.ManyToManyField(blank=True, to='facts.Person')),
                ('geographic_scope', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Region')),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='InitiativeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=300, verbose_name='Project name/title')),
                ('slug', models.SlugField(allow_unicode=True, max_length=310)),
                ('total_cost', models.BigIntegerField(blank=True, help_text='Values in whole units (dollars, etc.)', null=True)),
                ('total_cost_currency', models.CharField(blank=True, choices=[('AFN', 'Afghani'), ('DZD', 'Algerian Dinar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijanian Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('THB', 'Baht'), ('PAB', 'Balboa'), ('BBD', 'Barbados Dollar'), ('BYR', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudian Dollar'), ('BOB', 'Boliviano'), ('VEF', 'Bolívar'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('XOF', 'CFA Franc BCEAO'), ('XAF', 'CFA Franc BEAC'), ('XPF', 'CFP Franc'), ('CVE', 'Cabo Verde Escudo'), ('CAD', 'Canadian Dollar'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean Peso'), ('COP', 'Colombian Peso'), ('KMF', 'Comoro Franc'), ('CDF', 'Congolese Franc'), ('BAM', 'Convertible Mark'), ('NIO', 'Cordoba Oro'), ('CRC', 'Costa Rican Colon'), ('CUP', 'Cuban Peso'), ('CZK', 'Czech Koruna'), ('GMD', 'Dalasi'), ('DKK', 'Danish Krone'), ('MKD', 'Denar'), ('DJF', 'Djibouti Franc'), ('STD', 'Dobra'), ('DOP', 'Dominican Peso'), ('VND', 'Dong'), ('XCD', 'East Caribbean Dollar'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('HUF', 'Forint'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('HTG', 'Gourde'), ('PYG', 'Guarani'), ('GNF', 'Guinea Franc'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('UAH', 'Hryvnia'), ('ISK', 'Iceland Krona'), ('INR', 'Indian Rupee'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('KES', 'Kenyan Shilling'), ('PGK', 'Kina'), ('LAK', 'Kip'), ('HRK', 'Kuna'), ('KWD', 'Kuwaiti Dinar'), ('AOA', 'Kwanza'), ('MMK', 'Kyat'), ('GEL', 'Lari'), ('LBP', 'Lebanese Pound'), ('ALL', 'Lek'), ('HNL', 'Lempira'), ('SLL', 'Leone'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('SZL', 'Lilangeni'), ('LSL', 'Loti'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawi Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MUR', 'Mauritius Rupee'), ('MXN', 'Mexican Peso'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MDL', 'Moldovan Leu'), ('MAD', 'Moroccan Dirham'), ('MZN', 'Mozambique Metical'), ('BOV', 'Mvdol'), ('NGN', 'Naira'), ('ERN', 'Nakfa'), ('NAD', 'Namibia Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillean Guilder'), ('ILS', 'New Israeli Sheqel'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('BTN', 'Ngultrum'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('MRO', 'Ouguiya'), ('PKR', 'Pakistan Rupee'), ('MOP', 'Pataca'), ('TOP', 'Pa’anga'), ('CUC', 'Peso Convertible'), ('UYU', 'Peso Uruguayo'), ('PHP', 'Philippine Peso'), ('GBP', 'Pound Sterling'), ('BWP', 'Pula'), ('QAR', 'Qatari Rial'), ('GTQ', 'Quetzal'), ('ZAR', 'Rand'), ('OMR', 'Rial Omani'), ('KHR', 'Riel'), ('RON', 'Romanian Leu'), ('MVR', 'Rufiyaa'), ('IDR', 'Rupiah'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SHP', 'Saint Helena Pound'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('SGD', 'Singapore Dollar'), ('PEN', 'Sol'), ('SBD', 'Solomon Islands Dollar'), ('KGS', 'Som'), ('SOS', 'Somali Shilling'), ('TJS', 'Somoni'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('BDT', 'Taka'), ('WST', 'Tala'), ('TZS', 'Tanzanian Shilling'), ('KZT', 'Tenge'), ('TTD', 'Trinidad and Tobago Dollar'), ('MNT', 'Tugrik'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('AED', 'UAE Dirham'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UGX', 'Uganda Shilling'), ('CLF', 'Unidad de Fomento'), ('COU', 'Unidad de Valor Real'), ('UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('KRW', 'Won'), ('YER', 'Yemeni Rial'), ('JPY', 'Yen'), ('CNY', 'Yuan Renminbi'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar'), ('PLN', 'Zloty')], default='USD', max_length=3, null=True)),
                ('start_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('start_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('commencement_year', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Year of commencement of works')),
                ('commencement_month', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Month of commencement of works')),
                ('commencement_day', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Day of commencement of works')),
                ('planned_completion_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('planned_completion_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('planned_completion_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Announced/Under Negotiation'), (2, 'Preparatory Works'), (3, 'Started'), (4, 'Under Construction'), (5, 'Completed'), (6, 'Cancelled')], default=1, null=True)),
                ('new', models.NullBooleanField(verbose_name='New Construction?')),
                ('sources', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000, validators=[utilities.validators.URLLikeValidator]), blank=True, default=list, help_text='Enter URLs separated by commas.', null=True, size=None, verbose_name='Sources URLs')),
                ('notes', markymark.fields.MarkdownField(blank=True)),
                ('verified_path', models.NullBooleanField()),
                ('collection_stage', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Identified'), (2, 'Collected')], default=1, null=True)),
                ('consultants', models.ManyToManyField(blank=True, related_name='projects_consulted', to='facts.Organization', verbose_name='Consultants')),
                ('contacts', models.ManyToManyField(blank=True, related_name='projects_contacts', to='facts.Person', verbose_name='Points of contact')),
                ('contractors', models.ManyToManyField(blank=True, related_name='projects_contracted', to='facts.Organization', verbose_name='Contractors')),
                ('countries', models.ManyToManyField(blank=True, to='locations.Country')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProjectDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('source_url', models.CharField(blank=True, max_length=1000, validators=[utilities.validators.URLLikeValidator])),
                ('document_type', models.PositiveSmallIntegerField(blank=True, choices=[('Public Materials', ((1, 'Press Releases'), (2, 'Presentations & Brochures'), (3, 'National Development Plans'))), ('Agreements/Contracts', ((4, 'MoU'), (5, 'Financing Agreements'), (6, 'Procurement Contracts'), (7, 'Other Agreements'))), ('Operational Documents', ((8, 'Concept Notes'), (9, 'Review and Approval Documents'), (10, 'Procurement Documents'), (11, 'Appraisal Documents'), (12, 'Administration Manuals'), (13, 'Aide-Memoires'), (14, 'Financial Audits'))), ('Impact Assessment and Monitoring Reports', ((15, 'Environmental and Social Assessment'), (16, 'Resettlement Frameworks'), (17, 'Safeguards Monitoring Reports'), (18, 'Consultation Minutes'))), ('Implementation Progress Reports', ((19, 'Progress Reports'), (20, 'Completion Reports'))), ('Miscellaneous Reports', ((21, 'Miscellaneous Reports'),))], null=True, verbose_name='type')),
                ('notes', markymark.fields.MarkdownField(blank=True)),
                ('status_indicator', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Announced/Under Negotiation'), (2, 'Preparatory Works'), (3, 'Started'), (4, 'Under Construction'), (5, 'Completed'), (6, 'Cancelled')], null=True)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sources.Document')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFunding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField(blank=True, help_text='Values in whole units (dollars, etc.)', null=True)),
                ('currency', models.CharField(blank=True, choices=[('AFN', 'Afghani'), ('DZD', 'Algerian Dinar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Florin'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijanian Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('THB', 'Baht'), ('PAB', 'Balboa'), ('BBD', 'Barbados Dollar'), ('BYR', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudian Dollar'), ('BOB', 'Boliviano'), ('VEF', 'Bolívar'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('XOF', 'CFA Franc BCEAO'), ('XAF', 'CFA Franc BEAC'), ('XPF', 'CFP Franc'), ('CVE', 'Cabo Verde Escudo'), ('CAD', 'Canadian Dollar'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean Peso'), ('COP', 'Colombian Peso'), ('KMF', 'Comoro Franc'), ('CDF', 'Congolese Franc'), ('BAM', 'Convertible Mark'), ('NIO', 'Cordoba Oro'), ('CRC', 'Costa Rican Colon'), ('CUP', 'Cuban Peso'), ('CZK', 'Czech Koruna'), ('GMD', 'Dalasi'), ('DKK', 'Danish Krone'), ('MKD', 'Denar'), ('DJF', 'Djibouti Franc'), ('STD', 'Dobra'), ('DOP', 'Dominican Peso'), ('VND', 'Dong'), ('XCD', 'East Caribbean Dollar'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('HUF', 'Forint'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('HTG', 'Gourde'), ('PYG', 'Guarani'), ('GNF', 'Guinea Franc'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('UAH', 'Hryvnia'), ('ISK', 'Iceland Krona'), ('INR', 'Indian Rupee'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('KES', 'Kenyan Shilling'), ('PGK', 'Kina'), ('LAK', 'Kip'), ('HRK', 'Kuna'), ('KWD', 'Kuwaiti Dinar'), ('AOA', 'Kwanza'), ('MMK', 'Kyat'), ('GEL', 'Lari'), ('LBP', 'Lebanese Pound'), ('ALL', 'Lek'), ('HNL', 'Lempira'), ('SLL', 'Leone'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('SZL', 'Lilangeni'), ('LSL', 'Loti'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawi Kwacha'), ('MYR', 'Malaysian Ringgit'), ('MUR', 'Mauritius Rupee'), ('MXN', 'Mexican Peso'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MDL', 'Moldovan Leu'), ('MAD', 'Moroccan Dirham'), ('MZN', 'Mozambique Metical'), ('BOV', 'Mvdol'), ('NGN', 'Naira'), ('ERN', 'Nakfa'), ('NAD', 'Namibia Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillean Guilder'), ('ILS', 'New Israeli Sheqel'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('BTN', 'Ngultrum'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('MRO', 'Ouguiya'), ('PKR', 'Pakistan Rupee'), ('MOP', 'Pataca'), ('TOP', 'Pa’anga'), ('CUC', 'Peso Convertible'), ('UYU', 'Peso Uruguayo'), ('PHP', 'Philippine Peso'), ('GBP', 'Pound Sterling'), ('BWP', 'Pula'), ('QAR', 'Qatari Rial'), ('GTQ', 'Quetzal'), ('ZAR', 'Rand'), ('OMR', 'Rial Omani'), ('KHR', 'Riel'), ('RON', 'Romanian Leu'), ('MVR', 'Rufiyaa'), ('IDR', 'Rupiah'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SHP', 'Saint Helena Pound'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('SGD', 'Singapore Dollar'), ('PEN', 'Sol'), ('SBD', 'Solomon Islands Dollar'), ('KGS', 'Som'), ('SOS', 'Somali Shilling'), ('TJS', 'Somoni'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('BDT', 'Taka'), ('WST', 'Tala'), ('TZS', 'Tanzanian Shilling'), ('KZT', 'Tenge'), ('TTD', 'Trinidad and Tobago Dollar'), ('MNT', 'Tugrik'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('AED', 'UAE Dirham'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UGX', 'Uganda Shilling'), ('CLF', 'Unidad de Fomento'), ('COU', 'Unidad de Valor Real'), ('UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('KRW', 'Won'), ('YER', 'Yemeni Rial'), ('JPY', 'Yen'), ('CNY', 'Yuan Renminbi'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar'), ('PLN', 'Zloty')], default='USD', max_length=3, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infrastructure.Project')),
                ('sources', models.ManyToManyField(blank=True, to='facts.Organization')),
            ],
            options={
                'verbose_name_plural': 'project funders',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='documents',
            field=models.ManyToManyField(blank=True, to='infrastructure.ProjectDocument'),
        ),
        migrations.AddField(
            model_name='project',
            name='extra_data',
            field=models.ManyToManyField(blank=True, to='facts.Data'),
        ),
        migrations.AddField(
            model_name='project',
            name='geo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.GeometryStore'),
        ),
        migrations.AddField(
            model_name='project',
            name='implementers',
            field=models.ManyToManyField(blank=True, related_name='projects_implemented', to='facts.Organization', verbose_name='Client or implementing agency/ies'),
        ),
        migrations.AddField(
            model_name='project',
            name='infrastructure_type',
            field=models.ForeignKey(blank=True, help_text='Select or create named infrastructure types.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructure.InfrastructureType'),
        ),
        migrations.AddField(
            model_name='project',
            name='initiative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructure.Initiative'),
        ),
        migrations.AddField(
            model_name='project',
            name='operators',
            field=models.ManyToManyField(blank=True, related_name='projects_operated', to='facts.Organization'),
        ),
        migrations.AddField(
            model_name='project',
            name='regions',
            field=models.ManyToManyField(blank=True, help_text='Select or create geographic region names.', to='locations.Region'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='initiative_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructure.InitiativeType'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='member_countries',
            field=models.ManyToManyField(blank=True, to='locations.Country'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='infrastructure.Initiative', verbose_name='parent initiative'),
        ),
        migrations.AddField(
            model_name='initiative',
            name='principal_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='principal_initiatives', to='facts.Person'),
        ),
    ]
