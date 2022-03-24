package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.SelectProvider;

import jp.end0tknr.springvue.entity.GisGyoseiKuikiEntity;
import jp.end0tknr.springvue.sql.GisGyoseiKuikiSqlProvider;

@Mapper
public interface GisGyoseiKuikiRepository {

    @SelectProvider(
            type=GisGyoseiKuikiSqlProvider.class,
            method="sqlFindByCoord" )
    List<GisGyoseiKuikiEntity> findByCoord(
    		@Param("coord") List<Double> coord);

}
