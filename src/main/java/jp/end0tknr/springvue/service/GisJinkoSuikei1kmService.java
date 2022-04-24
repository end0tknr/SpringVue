package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisJinkoSuikei1kmRepository;

@Service
public class GisJinkoSuikei1kmService extends GisServiceFactory {

    @Autowired
    GisJinkoSuikei1kmRepository gisJinkoSuikei1kmRepository;

	public String tblName() {
    	return "gis_jinko_suikei_1km";
	}

	public String[] descsForDisp(){
    	String[] retStrs = {
    			"2030年男女計0～14歳人口",
    			"2030年男女計15～64歳人口",
    			"2030年男女計65歳以上人口",
    			"2040年男女計0～14歳人口",
    			"2040年男女計15～64歳人口",
    			"2040年男女計65歳以上人口",
    			"2050年男女計0～14歳人口",
    			"2050年男女計15～64歳人口",
    			"2050年男女計65歳以上人口"};
    	//Arrays.asList(retStrs).contains("Apple");
    	return retStrs;
    }

    public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisJinkoSuikei1kmRepository.findByCoord(coord);
    }

}
