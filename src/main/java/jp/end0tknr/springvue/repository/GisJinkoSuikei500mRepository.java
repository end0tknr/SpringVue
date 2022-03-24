package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisJinkoSuikei500mEntity;
import jp.end0tknr.springvue.sql.GisJinkoSuikei500mSqlProvider;

@Mapper
public interface GisJinkoSuikei500mRepository {

    @SelectProvider(
            type=GisJinkoSuikei500mSqlProvider.class,
            method="sqlFindByCoord" )
    List<GisJinkoSuikei500mEntity> findByCoord(
    		@Param("coord") List<Double> coord);

}
