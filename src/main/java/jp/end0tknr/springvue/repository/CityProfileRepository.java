package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface CityProfileRepository {

	@Select("SELECT summary FROM city_profile "+
			" WHERE pref='${prefName}' AND city='${cityName}'")
	String getCityProfile(String prefName,String cityName);

	@Select("SELECT build_year_summary FROM city_profile "+
			" WHERE pref='${prefName}' AND city='${cityName}'")
	String getBuildYearProfile(String prefName,String cityName);

    @Select("SELECT summary FROM city_profile tbl1"+
  		   " JOIN near_city tbl2 "+
  		   "  ON ( tbl1.pref=tbl2.near_pref AND tbl1.city=tbl2.near_city ) "+
  		   " WHERE tbl2.pref='${prefName}' AND tbl2.city='${cityName}' ")
     List<String> getNearCityProfiles(String prefName,String cityName);

    @Select("SELECT rating FROM city_profile "+
    		" WHERE pref='${prefName}' ")
    List<String> getCityRatings(String prefName);
}
