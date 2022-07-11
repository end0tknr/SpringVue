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

    public  List<String> getNearCityProfiles(
    		String prefName, String cityName) {
        return cityProfileRepository.getNearCityProfiles(prefName, cityName);
    }

    public  List<String> getTownProfiles(
    		String prefName, String cityName) {
        return townProfileRepository.getTownProfiles(prefName, cityName);
    }

}
