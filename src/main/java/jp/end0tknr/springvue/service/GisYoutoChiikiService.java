package jp.end0tknr.springvue.service;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisYoutoChiikiEntity;
import jp.end0tknr.springvue.repository.GisYoutoChiikiRepository;

@Service
public class GisYoutoChiikiService extends GisServiceFactory {

    @Autowired
    GisYoutoChiikiRepository gisYoutoChiikiRepository;

    public  List<HashMap> findByCoord(List coord) {

    	List<HashMap> retEntities = new ArrayList<HashMap>();
    	if( coord.size() != 4) {
    		return retEntities;
    	}

    	HashMap<String,String> colDefs	= getDescedColumnDefs();

    	for( GisYoutoChiikiEntity tmpEntity :
    		(List<GisYoutoChiikiEntity>) gisYoutoChiikiRepository.findByCoord(coord) ) {

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
