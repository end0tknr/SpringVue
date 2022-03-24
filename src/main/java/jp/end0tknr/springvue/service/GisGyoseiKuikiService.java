package jp.end0tknr.springvue.service;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.entity.GisGyoseiKuikiEntity;
import jp.end0tknr.springvue.repository.GisGyoseiKuikiRepository;

@Service
public class GisGyoseiKuikiService extends GisServiceFactory {

    @Autowired
    GisGyoseiKuikiRepository gisGyoseiKuikiRepository;

    public String[] descsForDisp(){
    	String[] retStrs = {"都道府県名","郡・政令都市名","市区町村名"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisGyoseiKuikiRepository.findByCoord(coord);
    }

    public  List<HashMap> findByCoord(List coord) {

    	List<HashMap> retEntities = new ArrayList<HashMap>();
    	if( coord.size() != 4) {
    		return retEntities;
    	}

    	HashMap<String,String> colDefs	= getDescedColumnDefs();

    	for( GisGyoseiKuikiEntity tmpEntity :
    		(List<GisGyoseiKuikiEntity>) gisGyoseiKuikiRepository.findByCoord(coord) ) {

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
