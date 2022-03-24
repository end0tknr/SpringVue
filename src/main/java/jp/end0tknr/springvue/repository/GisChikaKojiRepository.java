package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisChikaKojiEntity;
import jp.end0tknr.springvue.sql.GisChikaKojiSqlProvider;

@Mapper
public interface GisChikaKojiRepository {

    @SelectProvider(
            type=GisChikaKojiSqlProvider.class,
            method="sqlFindByCoord" )
    List<GisChikaKojiEntity> findByCoord(
    		@Param("coord") List<Double> coord);

}
