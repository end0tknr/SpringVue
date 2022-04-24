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


}
