package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCityEntity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByPriceEntity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopCityEntity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopEntity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByTownEntity;
import jp.end0tknr.springvue.repository.SumStockRepository;

@Service
public class SumStockService {

    @Autowired
    SumStockRepository sumStockRepository;

    public String getDispDateMin() {
    	return sumStockRepository.getDispDateMin();
    }
    public String getDispDateMax() {
    	return sumStockRepository.getDispDateMax();
    }

    public  List<SumStockSalesCountByShopEntity>
    getSalesCountByShop(String prefName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByShop(
    			prefName, dateFrom, dateTo);
    }
    public  List<SumStockSalesCountByShopCityEntity>
    getSalesCountByShopCity(
    		String prefName, String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByShopCity(
    			prefName,cityName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByCityEntity>
    getSalesCountByCity(
    		String prefName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByCity(
    			prefName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByTownEntity>
    getSalesCountByTown(
    		String prefName,String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByTown(
    			prefName,cityName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByPriceEntity>
    getSalesCountByPrice(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByPrice(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<SumStockSalesCountByCityEntity>
    getSalesCountByNearCity(
    		String prefName,String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByNearCity(
    			prefName,cityName, dateFrom, dateTo);
    }


}
