package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
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


}
