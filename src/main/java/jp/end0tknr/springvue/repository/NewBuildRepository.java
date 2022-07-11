package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByPriceEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTownEntity;

@Mapper
public interface NewBuildRepository {
	String limit = "LIMIT 5000";

    @Select("SELECT min(calc_date) FROM newbuild_sales_count_by_city")
    String getDispDateMin();

    @Select("SELECT max(calc_date) FROM newbuild_sales_count_by_city")
    String getDispDateMax();

    @Select("SELECT * FROM newbuild_sales_count_by_shop "+
    		"WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit )
    List<NewBuildSalesCountByShopEntity> getSalesCountByShop(
    		String prefName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_shop_city "+
    		" WHERE pref='${prefName}' AND city='${cityName}' "+
    		 "AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		 limit )
    List<NewBuildSalesCountByShopCityEntity> getSalesCountByShopCity(
    		String prefName,String cityName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_city "+
    "WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    limit)
    List<NewBuildSalesCountByCityEntity> getSalesCountByCity(
    		String prefName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_town "+
    		"WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit)
    List<NewBuildSalesCountByTownEntity> getSalesCountByTown(
    		String prefName,String cityName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_city_price "+
    		"WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit)
    List<NewBuildSalesCountByPriceEntity> getSalesCountByPrice(
    		String prefName,String cityName,String dateFrom,String dateTo);

   @Select(" SELECT tbl1.* FROM newbuild_sales_count_by_city tbl1 "+
		   " JOIN near_city tbl2 "+
		   "  ON ( tbl1.pref=tbl2.near_pref AND tbl1.city=tbl2.near_city ) "+
		   " WHERE tbl2.pref='${prefName}' AND tbl2.city='${cityName}' "+
		   " AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
		   limit)
    List<NewBuildSalesCountByCityEntity> getSalesCountByNearCity(
    		String prefName,String cityName,String dateFrom,String dateTo);

}
