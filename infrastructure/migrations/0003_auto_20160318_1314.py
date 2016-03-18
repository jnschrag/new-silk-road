# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-18 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0002_auto_20160317_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectfunding',
            options={'verbose_name_plural': 'Project Funders'},
        ),
        migrations.RemoveField(
            model_name='projectfunding',
            name='amount_description',
        ),
        migrations.AddField(
            model_name='projectfunding',
            name='amount',
            field=models.IntegerField(blank=True, help_text='Values in whole units (dollars, etc.)', null=True),
        ),
        migrations.AddField(
            model_name='projectfunding',
            name='currency',
            field=models.CharField(blank=True, choices=[('TMT', 'Turkmenistan New Manat'), ('BWP', 'Pula'), ('STD', 'Dobra'), ('NAD', 'Namibia Dollar'), ('BND', 'Brunei Dollar'), ('XAF', 'CFA Franc BEAC'), ('ETB', 'Ethiopian Birr'), ('LYD', 'Libyan Dinar'), ('GMD', 'Dalasi'), ('OMR', 'Rial Omani'), ('CHE', 'WIR Euro'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MXN', 'Mexican Peso'), ('TOP', 'Pa’anga'), ('CUC', 'Peso Convertible'), ('JOD', 'Jordanian Dinar'), ('MNT', 'Tugrik'), ('HTG', 'Gourde'), ('FKP', 'Falkland Islands Pound'), ('LAK', 'Kip'), ('SDG', 'Sudanese Pound'), ('UGX', 'Uganda Shilling'), ('MAD', 'Moroccan Dirham'), ('CZK', 'Czech Koruna'), ('BBD', 'Barbados Dollar'), ('CLF', 'Unidad de Fomento'), ('HNL', 'Lempira'), ('BAM', 'Convertible Mark'), ('SGD', 'Singapore Dollar'), ('ERN', 'Nakfa'), ('DJF', 'Djibouti Franc'), ('HKD', 'Hong Kong Dollar'), ('JMD', 'Jamaican Dollar'), ('CRC', 'Costa Rican Colon'), ('UZS', 'Uzbekistan Sum'), ('NPR', 'Nepalese Rupee'), ('GTQ', 'Quetzal'), ('KYD', 'Cayman Islands Dollar'), ('HUF', 'Forint'), ('LKR', 'Sri Lanka Rupee'), ('YER', 'Yemeni Rial'), ('AZN', 'Azerbaijanian Manat'), ('SBD', 'Solomon Islands Dollar'), ('TRY', 'Turkish Lira'), ('SEK', 'Swedish Krona'), ('BIF', 'Burundi Franc'), ('NOK', 'Norwegian Krone'), ('NGN', 'Naira'), ('GBP', 'Pound Sterling'), ('SAR', 'Saudi Riyal'), ('LSL', 'Loti'), ('NZD', 'New Zealand Dollar'), ('UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'), ('BMD', 'Bermudian Dollar'), ('AMD', 'Armenian Dram'), ('TTD', 'Trinidad and Tobago Dollar'), ('MDL', 'Moldovan Leu'), ('AWG', 'Aruban Florin'), ('BRL', 'Brazilian Real'), ('TND', 'Tunisian Dinar'), ('PAB', 'Balboa'), ('AOA', 'Kwanza'), ('BOB', 'Boliviano'), ('ZMW', 'Zambian Kwacha'), ('DOP', 'Dominican Peso'), ('RUB', 'Russian Ruble'), ('DKK', 'Danish Krone'), ('CLP', 'Chilean Peso'), ('IRR', 'Iranian Rial'), ('USD', 'US Dollar'), ('TWD', 'New Taiwan Dollar'), ('RON', 'Romanian Leu'), ('NIO', 'Cordoba Oro'), ('MVR', 'Rufiyaa'), ('KHR', 'Riel'), ('AUD', 'Australian Dollar'), ('SLL', 'Leone'), ('BHD', 'Bahraini Dinar'), ('KES', 'Kenyan Shilling'), ('BYR', 'Belarusian Ruble'), ('KPW', 'North Korean Won'), ('ZWL', 'Zimbabwe Dollar'), ('MZN', 'Mozambique Metical'), ('VND', 'Dong'), ('THB', 'Baht'), ('IDR', 'Rupiah'), ('CDF', 'Congolese Franc'), ('COP', 'Colombian Peso'), ('PKR', 'Pakistan Rupee'), ('BDT', 'Taka'), ('UAH', 'Hryvnia'), ('UYU', 'Peso Uruguayo'), ('ARS', 'Argentine Peso'), ('BSD', 'Bahamian Dollar'), ('VEF', 'Bolívar'), ('LBP', 'Lebanese Pound'), ('PGK', 'Kina'), ('BZD', 'Belize Dollar'), ('MGA', 'Malagasy Ariary'), ('GYD', 'Guyana Dollar'), ('SHP', 'Saint Helena Pound'), ('KWD', 'Kuwaiti Dinar'), ('SCR', 'Seychelles Rupee'), ('ILS', 'New Israeli Sheqel'), ('SZL', 'Lilangeni'), ('ANG', 'Netherlands Antillean Guilder'), ('BTN', 'Ngultrum'), ('MOP', 'Pataca'), ('CAD', 'Canadian Dollar'), ('INR', 'Indian Rupee'), ('KGS', 'Som'), ('ALL', 'Lek'), ('QAR', 'Qatari Rial'), ('BGN', 'Bulgarian Lev'), ('AFN', 'Afghani'), ('PLN', 'Zloty'), ('EGP', 'Egyptian Pound'), ('TJS', 'Somoni'), ('PHP', 'Philippine Peso'), ('VUV', 'Vatu'), ('JPY', 'Yen'), ('ZAR', 'Rand'), ('MRO', 'Ouguiya'), ('CVE', 'Cabo Verde Escudo'), ('CUP', 'Cuban Peso'), ('SRD', 'Surinam Dollar'), ('RSD', 'Serbian Dinar'), ('ISK', 'Iceland Krona'), ('TZS', 'Tanzanian Shilling'), ('MYR', 'Malaysian Ringgit'), ('MWK', 'Malawi Kwacha'), ('MKD', 'Denar'), ('BOV', 'Mvdol'), ('LRD', 'Liberian Dollar'), ('HRK', 'Kuna'), ('XCD', 'East Caribbean Dollar'), ('USN', 'US Dollar (Next day)'), ('SVC', 'El Salvador Colon'), ('WST', 'Tala'), ('AED', 'UAE Dirham'), ('KRW', 'Won'), ('MMK', 'Kyat'), ('SSP', 'South Sudanese Pound'), ('GEL', 'Lari'), ('EUR', 'Euro'), ('IQD', 'Iraqi Dinar'), ('CNY', 'Yuan Renminbi'), ('PEN', 'Sol'), ('RWF', 'Rwanda Franc'), ('KMF', 'Comoro Franc'), ('MUR', 'Mauritius Rupee'), ('PYG', 'Guarani'), ('XOF', 'CFA Franc BCEAO'), ('FJD', 'Fiji Dollar'), ('GHS', 'Ghana Cedi'), ('CHW', 'WIR Franc'), ('XPF', 'CFP Franc'), ('DZD', 'Algerian Dinar'), ('GNF', 'Guinea Franc'), ('GIP', 'Gibraltar Pound'), ('CHF', 'Swiss Franc'), ('KZT', 'Tenge'), ('COU', 'Unidad de Valor Real'), ('SOS', 'Somali Shilling'), ('SYP', 'Syrian Pound')], default='USD', max_length=3, null=True),
        ),
    ]
