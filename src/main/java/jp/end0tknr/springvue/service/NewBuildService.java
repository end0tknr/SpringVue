package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByPriceEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTownEntity;
import jp.end0tknr.springvue.repository.NewBuildRepository;

@Service
public class NewBuildService {

    @Autowired
    NewBuildRepository newBuildRepository;

    public String getDispDateMin() {
    	return newBuildRepository.getDispDateMin();
    }
    public String getDispDateMax() {
    	return newBuildRepository.getDispDateMax();
    }

    public  List<NewBuildSalesCountByShopEntity>
    getSalesCountByShop(
    		String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShop(prefName, dateFrom, dateTo );
    }

    public  List<String> getSalesCountByShopScale(
    		String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShopScale(prefName, dateFrom, dateTo );
    }

    public  List<String> getSalesCountByShopCityScale(
    		String prefName, String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShopCityScale(prefName, cityName, dateFrom, dateTo );
    }

    public  List<String> getSalesCountByTownScale(
    		String prefName, String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByTownScale(prefName, cityName, dateFrom, dateTo );
    }

    public  List<String> getSalesCountByCityScale(
    		String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByCityScale(prefName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByShopCityEntity>
    getSalesCountByShopCity(
    		String prefName, String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShopCity(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByCityEntity>
    getSalesCountByCity(String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByCity(prefName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByTownEntity>
    getSalesCountByTown(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByTown(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByPriceEntity>
    getSalesCountByPrice(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByPrice(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByCityEntity>
    getSalesCountByNearCity(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByNearCity(
    			prefName,cityName, dateFrom, dateTo );
    }


}
