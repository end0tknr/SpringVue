package jp.end0tknr.springvue.repository;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByPrice;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShop;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByTown;

@Mapper
public interface SumStockRepository {
	String limit = "LIMIT 5000";

    @Select("SELECT * FROM sumstock_sales_count_by_shop "+
    		"WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit )
    List<SumStockSalesCountByShop> getSalesCountByShop(
    		String prefName, String dateFrom, String dateTo);

    @Select("SELECT * FROM sumstock_sales_count_by_shop_city "+
    		" WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit )
    List<SumStockSalesCountByShopCity> getSalesCountByShopCity(
    		String prefName,String cityName, String dateFrom, String dateTo);

    @Select("SELECT * FROM sumstock_sales_count_by_city "+
    	    "WHERE pref='${prefName}' AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    	    limit)
    List<SumStockSalesCountByCity> getSalesCountByCity(
    		String prefName, String dateFrom, String dateTo);

    @Select("SELECT * FROM sumstock_sales_count_by_town "+
    		"WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit)
    List<SumStockSalesCountByTown> getSalesCountByTown(
    		String prefName,String cityName, String dateFrom, String dateTo);

    @Select("SELECT * FROM sumstock_sales_count_by_city_price "+
    		"WHERE pref='${prefName}' AND city='${cityName}' "+
    		"AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
    		limit)
    List<SumStockSalesCountByPrice> getSalesCountByPrice(
    		String prefName,String cityName,String dateFrom,String dateTo);

   @Select(" SELECT tbl1.* FROM sumstock_sales_count_by_city tbl1 "+
		   " JOIN near_city tbl2 "+
		   "  ON ( tbl1.pref=tbl2.near_pref AND tbl1.city=tbl2.near_city ) "+
		   " WHERE tbl2.pref='${prefName}' AND tbl2.city='${cityName}' "+
		   " AND calc_date BETWEEN '${dateFrom}' AND '${dateTo}' "+
		   limit)
    List<SumStockSalesCountByCity> getSalesCountByNearCity(
    		String prefName,String cityName, String dateFrom, String dateTo);

}
