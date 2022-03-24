package jp.end0tknr.springvue.service;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.entity.GisJinkoSuikei500mEntity;
import jp.end0tknr.springvue.repository.GisJinkoSuikei500mRepository;

@Service
public class GisJinkoSuikei500mService extends GisServiceFactory {

    @Autowired
    GisJinkoSuikei500mRepository gisJinkoSuikei500mRepository;

	public String tblName() {
    	return "gis_jinko_suikei_500m";
	}

    public String[] descsForDisp(){
    	String[] retStrs = {
    			"2030年男女計0～14歳人口",
    			"2030年男女計15～64歳人口",
    			"2030年男女計65歳以上人口",
    			"2040年男女計0～14歳人口",
    			"2040年男女計15～64歳人口",
    			"2040年男女計65歳以上人口",
    			"2050年男女計0～14歳人口",
    			"2050年男女計15～64歳人口",
    			"2050年男女計65歳以上人口"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisJinkoSuikei500mRepository.findByCoord(coord);
    }


    public  List<HashMap> findByCoord(List coord) {

    	List<HashMap> retEntities = new ArrayList<HashMap>();
    	if( coord.size() != 4) {
    		return retEntities;
    	}

    	HashMap<String,String> colDefs	= getDescedColumnDefs();

    	for( GisJinkoSuikei500mEntity tmpEntity :
    		(List<GisJinkoSuikei500mEntity>) gisJinkoSuikei500mRepository.findByCoord(coord) ) {

    		HashMap<String,Object> retEntity = new HashMap();

    	    for (Field field : tmpEntity.getClass().getDeclaredFields() ){
    	    	field.setAccessible(true);
    	    	String fieldName = field.getName();
    	    	if (! colDefs.containsKey(fieldName) ) {
    	    		continue;
    	    	}

    	    	try {
					retEntity.put( colDefs.get(fieldName), field.get(tmpEntity));
				} catch (IllegalArgumentException | IllegalAccessException e) {
					e.printStackTrace();
				}
    	    }
    	    retEntity.put( "geom", tmpEntity.getGeom() );
    	    //System.out.println(retEntity);
    	    retEntities.add(retEntity);
    	}

    	return retEntities;
    }


}
