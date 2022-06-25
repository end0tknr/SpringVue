package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisJinkoSuikei500mRepository;

@Service
public class GisJinkoSuikei500mService extends GisServiceFactory {

    @Autowired
    GisJinkoSuikei500mRepository gisJinkoSuikei500mRepository;

	@Override
	public String tblName() {
    	return "gis_jinko_suikei_500m";
	}

    @Override
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

    @Override
	public  List<GisEntityAbstract> findByCoordFromRepo(List coord) {
    	return gisJinkoSuikei500mRepository.findByCoord(coord);
    }

}
