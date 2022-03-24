package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisJinkoShuchuRepository;

@Service
public class GisJinkoShuchuService extends GisServiceFactory {

    @Autowired
    GisJinkoShuchuRepository gisJinkoShuchuRepository;

    public String[] descsForDisp(){
    	String[] retStrs = {"人口","面積"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisJinkoShuchuRepository.findByCoord(coord);
    }

//    public  List<HashMap> findByCoord(List coord) {
//
//    	List<HashMap> retEntities = new ArrayList<HashMap>();
//    	if( coord.size() != 4) {
//    		return retEntities;
//    	}
//
//    	HashMap<String,String> colDefs	= getDescedColumnDefs();
//
//    	for( GisJinkoShuchuEntity tmpEntity :
//    		(List<GisJinkoShuchuEntity>) gisJinkoShuchuRepository.findByCoord(coord) ) {
//
//    		HashMap<String,Object> retEntity = new HashMap();
//
//    	    for (Field field : tmpEntity.getClass().getDeclaredFields() ){
//    	    	field.setAccessible(true);
//    	    	String fieldName = field.getName();
//    	    	if (! colDefs.containsKey(fieldName) ) {
//    	    		continue;
//    	    	}
//
//    	    	try {
//					retEntity.put( colDefs.get(fieldName), field.get(tmpEntity));
//				} catch (IllegalArgumentException | IllegalAccessException e) {
//					e.printStackTrace();
//				}
//    	    }
//    	    retEntity.put( "geom", tmpEntity.getGeom() );
//    	    //System.out.println(retEntity);
//    	    retEntities.add(retEntity);
//    	}
//
//    	return retEntities;
//    }


}
