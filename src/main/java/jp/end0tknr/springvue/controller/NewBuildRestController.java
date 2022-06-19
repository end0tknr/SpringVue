package jp.end0tknr.springvue.controller;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShop;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByTown;
import jp.end0tknr.springvue.service.NewBuildService;

@RestController
@CrossOrigin
public class NewBuildRestController {

    @Autowired
    NewBuildService newBuildService;

    @RequestMapping("/api/newbuild/SalesCountByShop/{prefName}")
    public List<NewBuildSalesCountByShop> salesCountByShop(
    		@PathVariable("prefName") String prefName ){

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByShop(prefName);
    }

    @RequestMapping("/api/newbuild/SalesCountByCity/{prefName}")
    public List<NewBuildSalesCountByCity> salesCountByCity(
    		@PathVariable("prefName") String prefName ){

    	try {
			prefName = URLDecoder.decode(prefName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
    	return newBuildService.getSalesCountByCity(prefName);
    }

    @RequestMapping("/api/newbuild/SalesCountByTown/{prefCityName}")
    public List<NewBuildSalesCountByTown> salesCountByTown(
    		@PathVariable("prefCityName") String prefCityName ){

    	try {
    		prefCityName = URLDecoder.decode(prefCityName, "UTF-8");
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}

    	String[] names = prefCityName.split("_");
    	return newBuildService.getSalesCountByTown(names[0],names[1]);
    }
}
