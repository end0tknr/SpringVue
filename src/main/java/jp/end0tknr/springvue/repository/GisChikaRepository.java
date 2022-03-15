package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.GisChikaEntity;

@Mapper
public interface GisChikaRepository {

    @Select("SELECT * FROM gis_chika WHERE l02_022 like #{address} LIMIT 20")
    List<GisChikaEntity> findByAddress(@Param("address") String address);


}
