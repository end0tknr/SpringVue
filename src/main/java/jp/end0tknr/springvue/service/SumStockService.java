package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShop;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByTown;
import jp.end0tknr.springvue.repository.SumStockRepository;

@Service
public class SumStockService {

    @Autowired
    SumStockRepository sumStockRepository;

    public  List<SumStockSalesCountByShop>
    getSalesCountByShop(String prefName) {
    	return sumStockRepository.getSalesCountByShop(prefName);
    }
    public  List<SumStockSalesCountByShopCity>
    getSalesCountByShopCity(String prefName, String cityName) {
    	return sumStockRepository.getSalesCountByShopCity(prefName,cityName);
    }

    public  List<SumStockSalesCountByCity>
    getSalesCountByCity(String prefName) {
    	return sumStockRepository.getSalesCountByCity(prefName);
    }

    public  List<SumStockSalesCountByTown>
    getSalesCountByTown(String prefName,String cityName) {
    	return sumStockRepository.getSalesCountByTown(prefName,cityName);
    }

    public  List<SumStockSalesCountByCity>
    getSalesCountByNearCity(String prefName,String cityName) {
    	return sumStockRepository.getSalesCountByNearCity(prefName,cityName);
    }


}
