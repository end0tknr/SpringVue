package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisJinkoSuikei1kmEntity;
import jp.end0tknr.springvue.sql.GisJinkoSuikei1kmSqlProvider;

@Mapper
public interface GisJinkoSuikei1kmRepository {

    @SelectProvider(
            type=GisJinkoSuikei1kmSqlProvider.class,
            method="sqlFindByCoord" )
    List<GisJinkoSuikei1kmEntity> findByCoord(
    		@Param("coord") List<Double> coord);

}
