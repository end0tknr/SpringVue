package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisChikaEntity;

@Mapper
public interface GisChikaRepository {

    @Select("SELECT * FROM gis_chika WHERE l02_022 like #{address} LIMIT 20")
    List<GisChikaEntity> findByAddress(@Param("address") String address);

    @SelectProvider(
            type=GisChikaRepositorySqlProvider.class,
            method="findByCoord" )
    List<GisChikaEntity> findByCoord(
    		@Param("coord") List<Double> coord);

    class GisChikaRepositorySqlProvider{

        public String findByCoord(List<Double> coord ) {

            String[] coordTmp = {
        			coord.get(1).toString() +" "+ coord.get(0).toString(),
        			coord.get(1).toString() +" "+ coord.get(2).toString(),
        			coord.get(3).toString() +" "+ coord.get(2).toString(),
        			coord.get(3).toString() +" "+ coord.get(0).toString(),
        			coord.get(1).toString() +" "+ coord.get(0).toString() };

        	String sqlStr =
        			" SELECT *, ST_AsText(geom) as geom_text "+
        			" FROM gis_chika "+
        			" WHERE "+
        			" ST_Intersects( "+
        			"  ST_GeographyFromText('POLYGON(("+
        			   String.join(",", coordTmp) +"))'),"+
        			"  geom) "+
        			" ORDER BY ST_AsText(geom) "+
        			//" ORDER BY l02_022 "+
        			" LIMIT 200";
        	//System.out.println( sqlStr );

        	 return sqlStr;
        }
    }
}
