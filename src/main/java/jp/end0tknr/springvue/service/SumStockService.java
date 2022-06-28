package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByPrice;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShop;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByTown;
import jp.end0tknr.springvue.repository.SumStockRepository;

@Service
public class SumStockService {

    @Autowired
    SumStockRepository sumStockRepository;

    public  List<SumStockSalesCountByShop>
    getSalesCountByShop(String prefName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByShop(
    			prefName, dateFrom, dateTo);
    }
    public  List<SumStockSalesCountByShopCity>
    getSalesCountByShopCity(
    		String prefName, String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByShopCity(
    			prefName,cityName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByCity>
    getSalesCountByCity(
    		String prefName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByCity(
    			prefName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByTown>
    getSalesCountByTown(
    		String prefName,String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByTown(
    			prefName,cityName, dateFrom, dateTo);
    }

    public  List<SumStockSalesCountByPrice>
    getSalesCountByPrice(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByPrice(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<SumStockSalesCountByCity>
    getSalesCountByNearCity(
    		String prefName,String cityName,String dateFrom, String dateTo) {
    	return sumStockRepository.getSalesCountByNearCity(
    			prefName,cityName, dateFrom, dateTo);
    }


}
