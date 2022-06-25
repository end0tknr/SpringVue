package jp.end0tknr.springvue.repository;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface CityProfileRepository {

    @Select("SELECT summary FROM city_profile "+
    		" WHERE pref='${prefName}' AND city='${cityName}'")
    String getCityProfile(String prefName,String cityName);
}
