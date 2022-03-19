package jp.end0tknr.springvue.controller;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.GisChikaEntity;
import jp.end0tknr.springvue.entity.GisEntity;
import jp.end0tknr.springvue.service.GisChikaService;
import jp.end0tknr.springvue.service.GisService;

@RestController
@CrossOrigin
public class GisRestController {

    @Autowired
    GisChikaService gisChikaService;
    @Autowired
    GisService gisService;

	@RequestMapping("/api/gis/chika")
    public List<GisChikaEntity> index() {
        return gisChikaService.findByAddress("東京都　国分寺市%");
    }

	@RequestMapping("/api/gis/datanames")
    public List<GisEntity> getDataNames() {
        return gisService.getDataNames();
    }
	@RequestMapping("/api/gis/coldefs/{dataName}")
    public List<GisEntity> tblColDefs
    ( @PathVariable("dataName") String dataName ) {
        return gisService.getColumnDefs(dataName);
    }

	@RequestMapping("/api/gis/find/{dataName}")
    public List findGisDatas(
    		@PathVariable("dataName") String dataName,
    		@RequestParam("co") String coordStr) {

		List<Double> coords = new ArrayList<Double>();

		for(String tmpStr : Arrays.asList(coordStr.split(",")) ){
			coords.add(Double.valueOf(tmpStr));
		}

		return gisChikaService.findByCoord(coords);
    }
}
