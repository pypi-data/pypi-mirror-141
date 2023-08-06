from hdsr_wis_config_reader.idmappings.columns import IdMapCols
from hdsr_wis_config_reader.idmappings.columns import StartEndDateCols
from hdsr_wis_config_reader.location_sets.columns import LocSetSharedCols
from hdsr_wis_config_reader.tests.fixtures import loc_sets


# silence flake8
loc_sets = loc_sets


def test_loc_set_columns(loc_sets):
    expected_hoofd_cols = [
        "ALLE_TYPES",
        "FOTO_ID",
        "GAFCODE",
        "GPGIDENT",
        "KOMPAS",
        "LOC_NAME",
        "RAYON",
        "RBGID",
        "SYSTEEM",
        "X",
        "Y",
        "Z",
        "end",
        "geometry",
        "internalLocation",
        "schema",
        "start",
    ]
    for col_name in expected_hoofd_cols:
        if LocSetSharedCols.must_exist(col_name=col_name):
            assert col_name in loc_sets.hoofdloc.geo_df.columns
    assert sorted(LocSetSharedCols.get_simple_col_name(col_name=x) for x in expected_hoofd_cols) == [
        "ALLE_TYPES",
        "FOTO_ID",
        "GAFCODE",
        "GPGIDENT",
        "KOMPAS",
        "LOC_NAME",
        "RAYON",
        "RBGID",
        "SYSTEEM",
        "X",
        "Y",
        "Z",
        "end",
        "geometry",
        "internalLocation",
        "schema",
        "start",
    ]

    expected_sub_cols = [
        "LOC_ID",
        "QNORM",
        "LOC_NAME",
        "X",
        "Y",
        "TYPE",
        "ALLE_TYPES",
        "START",
        "EIND",
        "PAR_ID",
        "FUNCTIE",
        "AKKOORD",
        "BALANS",
        "SYSTEEM",
        "RAYON",
        "KOMPAS",
        "HBOV",
        "HBEN",
        "HBOVPS",
        "HBENPS",
        "IRIS_ID",
        "GPGIDENT",
        "GAFCODE",
        "RBGID",
        "B_NAAR",
        "B_VAN",
        "AFGB_NAAR",
        "AFGB_VAN",
        "SWM",
        "NWW-MDV",
        "geometry",
    ]
    for col_name in expected_sub_cols:
        if LocSetSharedCols.must_exist(col_name=col_name):
            assert col_name in loc_sets.subloc.geo_df.columns

    orig_list = [LocSetSharedCols.start, LocSetSharedCols.eind, LocSetSharedCols.loc_id]
    simple_list = [StartEndDateCols.start, StartEndDateCols.end, IdMapCols.int_loc]
    for orig, simple in zip(orig_list, simple_list):
        assert LocSetSharedCols.get_simple_col_name(col_name=orig) == simple
        assert LocSetSharedCols.get_orig_col_name(col_name=simple) == orig

    # test string not in mapper
    assert LocSetSharedCols.get_simple_col_name(col_name="xxx") == "xxx"
