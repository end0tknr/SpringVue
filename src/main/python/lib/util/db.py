#!python
# -*- coding: utf-8 -*-

from psycopg2  import extras # for bulk insert
import appbase

logger = appbase.AppBase().get_logger()

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
            logger.error(" ".join([sql]))
            logger.error(e)
            return False
            
        return True
    
    def save_tbl_comment(self,tbl_name,comment):
        logger.info( " ".join([tbl_name,comment]) )

        conf = self.get_conf()
        db_conn = self.db_connect()
        cur = self.db_cursor(db_conn)
        sql = "COMMENT ON TABLE %s IS '%s'"%(tbl_name,comment)
        try:

            cur.execute(sql)
            db_conn.commit()
        except Exception as e:
            logger.error(" ".join([sql]))
            logger.error(e)
            return False
            
        return True


    def save_tbl_rows(self, tbl_name, atri_keys, rows):
        logger.info("start")
        logger.info(rows[0])

        bulk_insert_size = self.get_conf()["common"]["bulk_insert_size"]
        row_groups = self.divide_rows(rows, bulk_insert_size, atri_keys )
        
        sql = "INSERT INTO %s (%s) VALUES %s" % (tbl_name, ",".join(atri_keys),"%s")
        
        with self.db_connect() as db_conn:
            with self.db_cursor(db_conn) as db_cur:

                for row_group in row_groups:
                    try:
                        # bulk insert
                        extras.execute_values(db_cur,sql,row_group)
                    except Exception as e:
                        logger.error(e)
                        logger.error(sql)
                        logger.error(row_group)
                        return False
                    
            db_conn.commit()
        return True

    # for bulk insert
    def divide_rows(self, org_rows, chunk_size, atri_keys):
        i = 0
        chunk = []
        ret_rows = []
        for org_row in org_rows:
            new_tuple = ()
            for atri_key in atri_keys:
                new_tuple += (org_row[atri_key],)
            chunk.append( new_tuple )
            
            if len(chunk) >= chunk_size:
                ret_rows.append(chunk)
                chunk = []
            i += 1

        if len(chunk) > 0:
            ret_rows.append(chunk)

        return ret_rows

