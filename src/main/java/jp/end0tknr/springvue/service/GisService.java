package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntity;
import jp.end0tknr.springvue.repository.GisRepository;

@Service
public class GisService {

    @Autowired
    GisRepository gisRepository;

	@Value("${spring.datasource.dbname}")
	private String dbName;

//    public  List<GisEntity> getColumnDefs(String tblName) {
//        return gisRepository.getColumnDefs(dbName, tblName);
//    }
//
//    public  HashMap<String,String> getDescedColumnDefs(String tblName) {
//    	System.out.println("HGOE 2-1");
//    	HashMap<String,String> retMap = new HashMap<>();
//    	for (GisEntity entity : gisRepository.getDescedColumnDefs(dbName, tblName) ) {
//        	System.out.println("HGOE 2-2");
//    		retMap.put(entity.getColumn_name(),entity.getDescription());
//        	System.out.println("HGOE 2-3");
//    	}
//    	System.out.println("HGOE 2-4");
//        return retMap;
//    }

    public  List<GisEntity> getDataNames() {
        return gisRepository.getDataNames(dbName, "gis_%");
    }

}
