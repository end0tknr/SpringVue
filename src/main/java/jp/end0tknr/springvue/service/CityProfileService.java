package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.repository.CityProfileRepository;

@Service
public class CityProfileService {

    @Autowired
    CityProfileRepository cityProfileRepository;

    public  String getCityProfile(String prefName, String cityName) {
        return cityProfileRepository.getCityProfile(prefName, cityName);
    }

    public  String getCityProfileByYear(String prefName, String cityName) {
        return cityProfileRepository.getCityProfileByYear(prefName, cityName);
    }

    public  List<String> getNearCityProfiles(
    		String prefName, String cityName) {
        return cityProfileRepository.getNearCityProfiles(prefName, cityName);
    }

}
