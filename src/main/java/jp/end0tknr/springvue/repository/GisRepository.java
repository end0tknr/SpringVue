package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisEntity;

@Mapper
public interface GisRepository {


    @SelectProvider(
            type=GisRepositorySqlProvider.class,
            method="getColumnDefs" )
    List<GisEntity> getColumnDefs(
    		@Param("dbName") String dbName,
    		@Param("tblName") String tblName);

    @SelectProvider(
            type=GisRepositorySqlProvider.class,
            method="getDataNames" )
    List<GisEntity> getDataNames(
    		@Param("dbName") String dbName,
    		@Param("tblName") String tblName);


    class GisRepositorySqlProvider{

        public String getDataNames(String dbName, String tblName ) {

        	String sqlStr =
        			" SELECT "+
        			"   pc.relname as data_name,"+
        			"   pc.relpages/8 as kbyte,"+
        			"   pd.description "+
        			" FROM pg_class pc "+
        			" JOIN pg_stat_user_tables psut "+
        			"   ON pc.relname=psut.relname "+
        			" LEFT JOIN pg_description pd "+
        			"   ON psut.relid=pd.objoid and pd.objsubid=0 "+
        			" WHERE pc.relname like #{tblName} "+
        			" ORDER BY pc.relname";

        	 return sqlStr;
        }

        public String getColumnDefs(String dbName, String tblName ) {

        	String sqlStr =
        			" select isc.column_name, isc.data_type, pd.description "+
        			" from pg_stat_user_tables as psut "+
        			" join information_schema.columns as isc "+
        			" on (psut.relname=isc.table_name) "+
        			" left join pg_description as pd " +
        			" on (pd.objoid=psut.relid and pd.objsubid=isc.ordinal_position) ";
        	sqlStr += " WHERE isc.table_catalog=#{dbName} ";
        	sqlStr += "  AND isc.table_name =#{tblName} ";
        	sqlStr += " ORDER BY isc.ORDINAL_POSITION ";

        	 return sqlStr;
        }
    }
}
