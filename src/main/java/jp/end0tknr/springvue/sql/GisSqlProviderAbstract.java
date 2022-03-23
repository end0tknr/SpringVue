package jp.end0tknr.springvue.sql;

import java.util.List;

import org.springframework.beans.factory.annotation.Value;

public abstract class GisSqlProviderAbstract {
	@Value("${repository.gis.select.limit}")
	private String selectLimit;

    public String findByCoord(List<Double> coord, String tblName ) {

        String[] coordTmp = {
    			coord.get(1).toString() +" "+ coord.get(0).toString(),
    			coord.get(1).toString() +" "+ coord.get(2).toString(),
    			coord.get(3).toString() +" "+ coord.get(2).toString(),
    			coord.get(3).toString() +" "+ coord.get(0).toString(),
    			coord.get(1).toString() +" "+ coord.get(0).toString() };

    	String sqlStr =
    			" SELECT *, ST_AsText(geom) as geom_text "+
    			" FROM " + tblName +
    			" WHERE "+
    			" ST_Intersects( "+
    			"  ST_GeographyFromText('POLYGON(("+
    			   String.join(",", coordTmp) +"))'),"+
    			"  geom) "+
    			" ORDER BY ST_AsText(geom) "+
    			//" ORDER BY l02_022 "+
    			" LIMIT "+selectLimit;
    	//System.out.println( sqlStr );

    	 return sqlStr;
    }


}
