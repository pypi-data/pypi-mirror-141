import functools

from enginelib.rds.client import db_client, db_name
from enginelib.errors import Error

from enginelib.rds.utils import sql_sanitize

from typing import List, Dict


class NCCIMueMedicare:
    @staticmethod
    @functools.lru_cache(None)
    def get_row(tx_id: str, proc_code: str) -> Dict:
        """return single row from ncci_mue_mcr table, matching proc_code"""
        query = f'''
            SELECT * FROM "{db_name}".ncci_mue_mcr
            WHERE hcpcs = '{sql_sanitize(proc_code)}'
        '''
        rows = NCCIMueMedicare._run_query(tx_id, query)
        if rows:
            return rows[0]
        else:
            return {}

    @staticmethod
    def _run_query(tx_id: str, query: str) -> List:
        rows, error = db_client.GetReferenceData(tx_id or "<no_tx_id>", query)
        if not error:
            return rows
        elif 'does not exist' in error:
            return []
        raise Error(f"Unable to query {db_name}, error: {str(error)}")

