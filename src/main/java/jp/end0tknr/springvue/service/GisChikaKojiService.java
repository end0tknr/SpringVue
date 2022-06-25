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

    @Override
	public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisChikaKojiRepository.findByCoord(coord);
    }

    @Override
	public String[] descsForDisp(){
    	String[] retStrs = {"公示価格","周辺の土地利用の状況","建ぺい率","容積率"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

}
