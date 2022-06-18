package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShop;

@Mapper
public interface NewBuildRepository {

    @Select("SELECT * FROM newbuild_sales_count_by_shop WHERE pref='${prefName}' LIMIT 30")
    List<NewBuildSalesCountByShop> getSalesCountByShop(String prefName);

    @Select("SELECT * FROM newbuild_sales_count_by_city WHERE pref='${prefName}' LIMIT 30")
    List<NewBuildSalesCountByCity> getSalesCountByCity(String prefName);

}
