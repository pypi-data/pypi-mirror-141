from hdsr_wis_config_reader.idmappings.columns import IdMapCols
from hdsr_wis_config_reader.idmappings.columns import StartEndDateCols
from hdsr_wis_config_reader.idmappings.utils import get_class_attributes
from typing import Dict


class LocSetSharedCols:
    """Each location set (e.g hoofdlacations, sublocations, etc) csv has it own columns.
     However, some columns are shared by all csvs."""

    loc_id = "LOC_ID"
    loc_name = "LOC_NAME"
    x = "X"
    y = "Y"
    z = "Z"  # only in hoof- and waterstand loc_set
    gpgident = "GPGIDENT"
    gafcode = "GAFCODE"
    rbgid = "RBGID"
    start = "START"  # in all loc_set except for mswloc
    eind = "EIND"  # in all loc_set except for mswloc

    @classmethod
    def must_exist(cls, col_name: str) -> bool:
        """columns start and eind are in all loc_sets except for mswloc.
        column Z is only in hoofdloc and waterstand loc."""
        return col_name in {cls.loc_id, cls.loc_name, cls.x, cls.y, cls.gpgident, cls.gafcode, cls.rbgid}

    @classmethod
    def _get_all(cls) -> Dict:
        return get_class_attributes(the_class=cls)

    @classmethod
    def _mapper_orig_to_simple_col_name(cls) -> Dict:
        """column 'LOC_ID' is the same as id-mapping column 'InternalLocation' (e.g. 'KW760301'). To avoid using
        two different names for the same thing you can use loc_id_new when reading a location set to dataframe."""
        return {cls.loc_id: IdMapCols.int_loc, cls.start: StartEndDateCols.start, cls.eind: StartEndDateCols.end}

    @classmethod
    def get_simple_col_name(cls, col_name: str):
        return cls._mapper_orig_to_simple_col_name().get(col_name, col_name)

    @classmethod
    def get_orig_col_name(cls, col_name: str):
        mapper_simple_to_orig = {v: k for k, v in cls._mapper_orig_to_simple_col_name().items()}
        return mapper_simple_to_orig.get(col_name, col_name)
