package jp.end0tknr.springvue.entity;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;

public abstract class GisEntityAbstract {

	@Value("${spring.datasource.dbname}")
	private String dbName;
	public String getDbName() {
		return dbName;
	}

//	public List<Double> convGeomText2Coords(String geom_text) {
//        Pattern re = Pattern.compile( "[\\d\\.]+" );
//        Matcher m = re.matcher(geom_text);
//
//        List<Double> coords = new ArrayList<Double>();
//        while( m.find()) {
//        	coords.add( Double.parseDouble(m.group()) );
//        }
//
//        return coords;
//	}

	public List<Double> getGeom() {
		List<Double> lng_lat = new ArrayList<Double>();
		lng_lat.add(getLng());
		lng_lat.add(getLat());
		return lng_lat;
	}

	public abstract Double getLng();
	public abstract Double getLat();

}
