package jp.end0tknr.springvue.controller;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShop;
import jp.end0tknr.springvue.entity.SumStockSalesCountByShopCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByTown;
import jp.end0tknr.springvue.service.CityProfileService;
import jp.end0tknr.springvue.service.SumStockService;

@RestController
@CrossOrigin
public class SumStockRestController {

    @Autowired
    SumStockService sumStockService;
    @Autowired
    CityProfileService cityProfileService;

    @RequestMapping("/api/sumstock/SalesCountByShop/{prefName}")
    public List<SumStockSalesCountByShop> salesCountByShop(
    		@PathVariable("prefName") String prefName ){

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return sumStockService.getSalesCountByShop(prefName);
    }

    @RequestMapping("/api/sumstock/SalesCountByShopCity/{prefCityName}")
    public List<SumStockSalesCountByShopCity> salesCountByShopCity(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByShopCity(names[0],names[1]);
    }

    @RequestMapping("/api/sumstock/SalesCountByCity/{prefName}")
    public List<SumStockSalesCountByCity> salesCountByCity(
    		@PathVariable("prefName") String prefName ){

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return sumStockService.getSalesCountByCity(prefName);
    }

    @RequestMapping("/api/sumstock/SalesCountByNearCity/{prefCityName}")
    public List<SumStockSalesCountByCity> salesCountByNearCity(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByNearCity(names[0],names[1]);
    }

    @RequestMapping("/api/sumstock/SalesCountByTown/{prefCityName}")
    public List<SumStockSalesCountByTown> salesCountByTown(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByTown(names[0],names[1]);
    }


    @RequestMapping("/api/sumstock/CityProfile/{prefCityName}")
    public String cityProfile(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");

    	String cityProfile = cityProfileService.getCityProfile(names[0],names[1]);

    	return cityProfile;
    }

    @RequestMapping("/api/sumstock/NearCityProfiles/{prefCityName}")
    public List<String> nearCityProfiles (
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");

    	List<String> cityProfile =
    			cityProfileService.getNearCityProfiles(names[0],names[1]);
    	return cityProfile;
    }


}
