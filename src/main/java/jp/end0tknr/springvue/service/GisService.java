package jp.end0tknr.springvue.service;

import java.util.HashMap;
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

    public  List<GisEntity> getColumnDefs(String tblName) {
        return gisRepository.getColumnDefs(dbName, tblName);
    }

    public  HashMap<String,String> getDescedColumnDefs(String tblName) {
    	HashMap<String,String> retMap = new HashMap<>();
    	for (GisEntity entity : gisRepository.getDescedColumnDefs(dbName, tblName) ) {
    		retMap.put(entity.getColumn_name(),entity.getDescription());
    	}
        return retMap;
    }

    public  List<GisEntity> getDataNames() {
        return gisRepository.getDataNames(dbName, "gis_%");
    }

}
