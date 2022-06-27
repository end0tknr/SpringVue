package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShop;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTown;

@Mapper
public interface NewBuildRepository {
	String limit = "LIMIT 5000";

    @Select("SELECT * FROM newbuild_sales_count_by_shop "+
    		"WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit )
    List<NewBuildSalesCountByShop> getSalesCountByShop(
    		String prefName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_shop_city "+
    		" WHERE pref='${prefName}' AND city='${cityName}' "+
    		 "AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		 limit )
    List<NewBuildSalesCountByShopCity> getSalesCountByShopCity(
    		String prefName,String cityName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_city "+
    "WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    limit)
    List<NewBuildSalesCountByCity> getSalesCountByCity(
    		String prefName,String dateFrom,String dateTo);

    @Select("SELECT * FROM newbuild_sales_count_by_town "+
    		"WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit)
    List<NewBuildSalesCountByTown> getSalesCountByTown(
    		String prefName,String cityName,String dateFrom,String dateTo);

   @Select(" SELECT tbl1.* FROM newbuild_sales_count_by_city tbl1 "+
		   " JOIN near_city tbl2 "+
		   "  ON ( tbl1.pref=tbl2.near_pref AND tbl1.city=tbl2.near_city ) "+
		   " WHERE tbl2.pref='${prefName}' AND tbl2.city='${cityName}' "+
		   " AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
		   limit)
    List<NewBuildSalesCountByCity> getSalesCountByNearCity(
    		String prefName,String cityName,String dateFrom,String dateTo);

}
