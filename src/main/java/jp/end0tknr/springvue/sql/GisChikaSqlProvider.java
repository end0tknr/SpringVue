package jp.end0tknr.springvue.sql;

import java.util.List;

public class GisChikaSqlProvider extends GisSqlProviderAbstract {

    public String findByCoord(List<Double> coord ) {
    	return findByCoord(coord, "gis_chika");
    }
}