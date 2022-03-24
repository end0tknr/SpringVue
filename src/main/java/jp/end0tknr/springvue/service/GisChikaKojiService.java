package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisChikaKojiRepository;

@Service
public class GisChikaKojiService extends GisServiceFactory {

    @Autowired
    GisChikaKojiRepository gisChikaKojiRepository;

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisChikaKojiRepository.findByCoord(coord);
    }

    public String[] descsForDisp(){
    	String[] retStrs = {"公示価格","周辺の土地利用の状況","建ぺい率","容積率"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
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
//    	for( GisChikaKojiEntity tmpEntity :
//    		(List<GisChikaKojiEntity>) gisChikaKojiRepository.findByCoord(coord) ) {
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
