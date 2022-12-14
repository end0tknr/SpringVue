package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.repository.CityProfileRepository;
import jp.end0tknr.springvue.repository.TownProfileRepository;

@Service
public class CityProfileService {

    @Autowired
    CityProfileRepository cityProfileRepository;
    @Autowired
    TownProfileRepository townProfileRepository;

    public  String getCityProfile(String prefName, String cityName) {
        return cityProfileRepository.getCityProfile(prefName, cityName);
    }

    public  String getBuildYearProfile(String prefName, String cityName) {
        return cityProfileRepository.getBuildYearProfile(prefName, cityName);
    }

    public  List<String> getNearCityProfiles(
    		String prefName, String cityName) {
        return cityProfileRepository.getNearCityProfiles(prefName, cityName);
    }

    public  List<String> getCityNewBuildRatings( String prefName) {
        return cityProfileRepository.getCityNewBuildRatings(prefName);
    }

    public  List<String> getTownNewbuildRatings( String prefName, String cityName) {
        return townProfileRepository.getTownNewbuildRatings(prefName, cityName);
    }

    public  List<String> getCitySumStockRatings( String prefName) {
        return cityProfileRepository.getCitySumStockRatings(prefName);
    }

    public  List<String> getTownSumStockRatings( String prefName, String cityName) {
        return townProfileRepository.getTownSumStockRatings(prefName, cityName);
    }

    public  List<String> getTownProfiles(
    		String prefName, String cityName) {
        return townProfileRepository.getTownProfiles(prefName, cityName);
    }

}
