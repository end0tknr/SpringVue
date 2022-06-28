package jp.end0tknr.springvue.controller;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.SumStockSalesCountByCity;
import jp.end0tknr.springvue.entity.SumStockSalesCountByPrice;
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

    List<String> convStr2CalcDate(String dateStr) {
        SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dateFrom = new Date();
		try {
	    	if(dateStr != null) {
	    		dateFrom = sdFormat.parse(dateStr);
	    	}
		} catch (ParseException e) {
			//e.printStackTrace();
		}

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(dateFrom);
        calendar.add(Calendar.DAY_OF_MONTH, 6);
        Date dateTo = calendar.getTime();

        return Arrays.asList(
        		sdFormat.format(dateFrom),
        		sdFormat.format(dateTo) );
    }

    @RequestMapping("/api/sumstock/SalesCountByShop/{prefName}")
    public List<SumStockSalesCountByShop> salesCountByShop(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);


    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return sumStockService.getSalesCountByShop(
    			prefName,calcDate.get(0),calcDate.get(1));
    }

    @RequestMapping("/api/sumstock/SalesCountByShopCity/{prefCityName}")
    public List<SumStockSalesCountByShopCity> salesCountByShopCity(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByShopCity(
    			names[0],names[1],calcDate.get(0),calcDate.get(1));
    }

    @RequestMapping("/api/sumstock/SalesCountByCity/{prefName}")
    public List<SumStockSalesCountByCity> salesCountByCity(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return sumStockService.getSalesCountByCity(
    			prefName,calcDate.get(0),calcDate.get(1));
    }

    @RequestMapping("/api/sumstock/SalesCountByNearCity/{prefCityName}")
    public List<SumStockSalesCountByCity> salesCountByNearCity(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByNearCity(
    			names[0],names[1],calcDate.get(0),calcDate.get(1));
    }

    @RequestMapping("/api/sumstock/SalesCountByTown/{prefCityName}")
    public List<SumStockSalesCountByTown> salesCountByTown(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByTown(
    			names[0],names[1],calcDate.get(0),calcDate.get(1));
    }

    @RequestMapping("/api/sumstock/SalesCountByPrice/{prefCityName}")
    public List<SumStockSalesCountByPrice> salesCountByPrice(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return sumStockService.getSalesCountByPrice(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
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
