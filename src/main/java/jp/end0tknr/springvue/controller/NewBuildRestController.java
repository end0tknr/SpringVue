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
}
