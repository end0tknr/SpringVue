package jp.end0tknr.springvue.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.CityEntity;
import jp.end0tknr.springvue.repository.CityRepository;

@Service
public class CityService {

    @Autowired
    CityRepository cityRepository;

    public  CityEntity getByLatLng(float lat, float lng) {
        return cityRepository.getByLatLng(lat,lng);
    }


}
