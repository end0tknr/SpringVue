#!python
# -*- coding: utf-8 -*-

import appbase

logger = appbase.AppBase.get_logger()

class Db(appbase.AppBase):
    
    def __init__(self):
        pass

    def col_defs(self,tbl_name):
        conf = self.get_conf()
        db_conn = self.db_connect()
        cur = self.db_cursor(db_conn)
        sql = """
select
  isc.column_name, isc.data_type, pd.description
from information_schema.columns as isc
left join pg_description as pd
  on ( pd.objsubid=isc.ordinal_position )
left join pg_stat_user_tables as psut
  on (pd.objoid=psut.relid and psut.relname=isc.table_name)
where isc.table_catalog=%s and isc.table_name=%s
ORDER BY isc.ORDINAL_POSITION
"""
        try:
            cur.execute(sql, [conf["db"]["db_name"],tbl_name])
        except Exception as e:
            logger.error(e)
            return []
        
        ret_rows = []
        for row in cur.fetchall():
            ret_rows.append( dict(row) )
            
        return ret_rows

    def save_col_comment(self,tbl_name,col_name,comment):
        logger.info( " ".join([tbl_name,col_name,comment]) )

        conf = self.get_conf()
        db_conn = self.db_connect()
        cur = self.db_cursor(db_conn)
        sql = "COMMENT ON COLUMN %s.%s IS '%s'"%(tbl_name,col_name,comment)
        try:
            cur.execute(sql)
            db_conn.commit()
        except Exception as e:
            logger.error(" ".join([sql,tbl_name,col_name,comment]))
            logger.error(e)
            return False
            
        return True
