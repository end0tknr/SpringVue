package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisChikaRepository;

@Service
public class GisChikaService extends GisServiceFactory {

    @Autowired
    GisChikaRepository gisChikaRepository;

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisChikaRepository.findByCoord(coord);
    }

    public String[] descsForDisp(){
    	String[] retStrs = {"調査価格","周辺の土地利用の状況","建ぺい率","容積率"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

}
