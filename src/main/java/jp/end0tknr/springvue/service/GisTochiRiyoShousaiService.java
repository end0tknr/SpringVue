package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisTochiRiyoShousaiRepository;

@Service
public class GisTochiRiyoShousaiService extends GisServiceFactory {

    @Autowired
    GisTochiRiyoShousaiRepository gisTochiRiyoShousaiRepository;

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisTochiRiyoShousaiRepository.findByCoord(coord);
    }

    public String[] descsForDisp(){
    	String[] retStrs = {"土地利用種別"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

}
