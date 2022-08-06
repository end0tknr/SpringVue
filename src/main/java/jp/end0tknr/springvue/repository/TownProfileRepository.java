package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface TownProfileRepository {

    @Select("SELECT summary FROM town_profile"+
  		   " WHERE pref='${prefName}' AND city='${cityName}' "+
  		   " ORDER BY town ")
    List<String> getTownProfiles(String prefName,String cityName);

    @Select("SELECT newbuild_rating FROM town_profile"+
 		   " WHERE pref='${prefName}' AND city='${cityName}' "+
 		   " ORDER BY town ")
    List<String> getTownNewbuildRatings(String prefName,String cityName);
}
