package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisJinkoShuchuEntity;
import jp.end0tknr.springvue.sql.GisJinkoShuchuSqlProvider;

@Mapper
public interface GisJinkoShuchuRepository {

    @SelectProvider(
            type=GisJinkoShuchuSqlProvider.class,
            method="sqlFindByCoord" )
    List<GisJinkoShuchuEntity> findByCoord(
    		@Param("coord") List<Double> coord);

}
