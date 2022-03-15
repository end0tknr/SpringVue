package jp.end0tknr.springvue.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import jp.end0tknr.springvue.entity.GisChikaEntity;
import jp.end0tknr.springvue.entity.GisEntity;
import jp.end0tknr.springvue.service.GisChikaService;
import jp.end0tknr.springvue.service.GisService;

@RestController
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
	@RequestMapping("/api/gis/coldefs")
    public List<GisEntity> tblColDefs() {
        return gisService.getColumnDefs("gis_chika");
    }
}
