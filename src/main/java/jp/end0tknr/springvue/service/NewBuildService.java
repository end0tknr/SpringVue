package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShop;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTown;
import jp.end0tknr.springvue.repository.NewBuildRepository;

@Service
public class NewBuildService {

    @Autowired
    NewBuildRepository newBuildRepository;

    public  List<NewBuildSalesCountByShop>
    getSalesCountByShop(
    		String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShop(prefName, dateFrom, dateTo );
    }
    public  List<NewBuildSalesCountByShopCity>
    getSalesCountByShopCity(
    		String prefName, String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByShopCity(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByCity>
    getSalesCountByCity(String prefName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByCity(prefName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByTown>
    getSalesCountByTown(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByTown(
    			prefName,cityName, dateFrom, dateTo );
    }

    public  List<NewBuildSalesCountByCity>
    getSalesCountByNearCity(
    		String prefName,String cityName, String dateFrom, String dateTo) {
    	return newBuildRepository.getSalesCountByNearCity(
    			prefName,cityName, dateFrom, dateTo );
    }


}
