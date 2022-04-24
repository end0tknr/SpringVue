package jp.end0tknr.springvue.controller;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.GisEntity;
import jp.end0tknr.springvue.service.GisService;
import jp.end0tknr.springvue.service.GisServiceFactory;

@RestController
@CrossOrigin
public class GisRestController {

    @Autowired
    GisService gisService;
    @Autowired
    ApplicationContext context;

	@RequestMapping("/api/gis/datanames")
    public List<GisEntity> getDataNames() {
        return gisService.getDataNames();
    }
	@RequestMapping("/api/gis/coldefs/{dataName}")
    public HashMap<String,String> tblColDefs
    ( @PathVariable("dataName") String dataName ) {
		String gisBeanName = GisServiceFactory.toBeanName(dataName);
		GisServiceFactory gisFactory
		= (GisServiceFactory)context.getBean(gisBeanName);

		return gisFactory.getDescedColumnDefs4Disp();

    }

	@RequestMapping("/api/gis/find/{dataName}")
    public List findGisDatas(
    		@PathVariable("dataName") String dataName,
    		@RequestParam("co") String coordStr) {

		List<Double> coords = new ArrayList<Double>();

		for(String tmpStr : Arrays.asList(coordStr.split(",")) ){
			coords.add(Double.valueOf(tmpStr));
		}

		String gisBeanName = GisServiceFactory.toBeanName(dataName);
		GisServiceFactory gisFactory
		= (GisServiceFactory)context.getBean(gisBeanName);

		return gisFactory.findByCoord(coords);
    }
}
