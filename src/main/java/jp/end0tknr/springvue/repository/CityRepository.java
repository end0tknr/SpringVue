package jp.end0tknr.springvue.repository;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.CityEntity;

@Mapper
public interface CityRepository {

    @Select("SELECT * FROM city "+
    		" ORDER BY (lat - ${lat})^2 +(lng - ${lng})^2 "+
    		" LIMIT 1")
    CityEntity getByLatLng(float lat,float lng);
}
