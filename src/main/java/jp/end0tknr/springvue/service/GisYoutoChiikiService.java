package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisYoutoChiikiRepository;

@Service
public class GisYoutoChiikiService extends GisServiceFactory {

    @Autowired
    GisYoutoChiikiRepository gisYoutoChiikiRepository;

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisYoutoChiikiRepository.findByCoord(coord);
    }


    public String[] descsForDisp(){
    	String[] retStrs = {"用途地域名","建蔽率","容積率"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

}
