package jp.end0tknr.springvue.controller;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.CityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByPriceEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopCityEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShopEntity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTownEntity;
import jp.end0tknr.springvue.service.CityProfileService;
import jp.end0tknr.springvue.service.CityService;
import jp.end0tknr.springvue.service.ClientIpPosService;
import jp.end0tknr.springvue.service.NewBuildService;

@RestController
@CrossOrigin
public class NewBuildRestController {

	 Logger logger = LoggerFactory.getLogger( NewBuildRestController.class );

    @Autowired
    NewBuildService newBuildService;
    @Autowired
    CityService cityService;
    @Autowired
    CityProfileService cityProfileService;
    @Autowired
    ClientIpPosService clientIpPosService;

    List<String> convStr2CalcDate(String dateStr) {
        SimpleDateFormat sdFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dateTo = new Date();
		try {
	    	if(dateStr != null) {
	    		dateTo= sdFormat.parse(dateStr);
	    	}
		} catch (ParseException e) {
			//e.printStackTrace();
		}

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(dateTo);
        calendar.add(Calendar.DAY_OF_MONTH, -6);
        Date dateFrom = calendar.getTime();

        return Arrays.asList(
        		sdFormat.format(dateFrom),
        		sdFormat.format(dateTo) );
    }

    @RequestMapping("/api/newbuild/CityByLatLng/{latLng}")
    public CityEntity cityByLatLng(
    		@PathVariable("latLng") String latLng ){
    	String coordStr[] = latLng.split(",");

    	float lat = Float.parseFloat( coordStr[0] );
    	float lng = Float.parseFloat( coordStr[1] );

    	return cityService.getByLatLng(lat,lng);
    }

    @RequestMapping("/api/newbuild/ClientIp")
    public Map<String, String> clientIp(HttpServletRequest request){
    	Map<String, String> ipInfo = clientIpPosService.getClientIp(request);
    	return ipInfo;
    }

    @RequestMapping("/api/newbuild/DispDateRange")
    public String[] dispDateRange(){
    	String dateRange[] = new String[2];
    	dateRange[0] = newBuildService.getDispDateMin();
    	dateRange[1] = newBuildService.getDispDateMax();
    	return dateRange;
    }

    @RequestMapping("/api/newbuild/SalesCountByShop/{prefName}")
    public List<NewBuildSalesCountByShopEntity> salesCountByShop(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByShop(
    			prefName,calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByShopScale/{prefName}")
    public List<String> salesCountByShopScale(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByShopScale(
    			prefName,calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByShopCityScale/{prefCityName}")
    public List<String> salesCountByShopCityScale(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByShopCityScale(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByTownScale/{prefCityName}")
    public List<String> salesCountByTownScale(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByTownScale(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByCityScale/{prefName}")
    public List<String> salesCountByCityScale(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByCityScale(
    			prefName,calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByShopCity/{prefCityName}")
    public List<NewBuildSalesCountByShopCityEntity> salesCountByShopCity(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByShopCity(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByCity/{prefName}")
    public List<NewBuildSalesCountByCityEntity> salesCountByCity(
    		@PathVariable("prefName") String prefName,
    		@RequestParam(value="date", required=false) String calcDateStr  ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByCity(
    			prefName,calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByNearCity/{prefCityName}")
    public List<NewBuildSalesCountByCityEntity> salesCountByNearCity(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByNearCity(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByTown/{prefCityName}")
    public List<NewBuildSalesCountByTownEntity> salesCountByTown(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByTown(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/SalesCountByPrice/{prefCityName}")
    public List<NewBuildSalesCountByPriceEntity> salesCountByPrice(
    		@PathVariable("prefCityName") String prefCityName,
    		@RequestParam(value="date", required=false) String calcDateStr ){

    	List<String> calcDate = convStr2CalcDate(calcDateStr);

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByPrice(
    			names[0],names[1],calcDate.get(0),calcDate.get(1) );
    }

    @RequestMapping("/api/newbuild/CityProfile/{prefCityName}")
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

    @RequestMapping("/api/newbuild/CityProfileByBuildYear/{prefCityName}")
    public String buildYearCityProfile(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");

    	String cityProfile =
    			cityProfileService.getBuildYearProfile(names[0],names[1]);

    	return cityProfile;
    }

    @RequestMapping("/api/newbuild/NearCityProfiles/{prefCityName}")
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


    @RequestMapping("/api/newbuild/TownProfiles/{prefCityName}")
    public List<String> townProfiles (
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
			prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	String[] names = prefCityName.split("_");

    	List<String> townProfile =
    			cityProfileService.getTownProfiles(names[0],names[1] );
    	return townProfile;
    }

}
