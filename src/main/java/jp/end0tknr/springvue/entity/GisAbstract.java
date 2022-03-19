package jp.end0tknr.springvue.entity;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.beans.factory.annotation.Value;

abstract class GisAbstract {

	@Value("${spring.datasource.dbname}")
	private String dbName;
	public String getDbName() {
		return dbName;
	}

	public List<Double> convGeomText2Coords(String geom_text) {
        Pattern re = Pattern.compile( "[\\d\\.]+" );
        Matcher m = re.matcher(geom_text);

        System.out.println(geom_text);
        System.out.println(m.groupCount());

        List<Double> coords = new ArrayList<Double>();
        while( m.find()) {
        	coords.add( Double.parseDouble(m.group()) );
        }

        return coords;
	}


}
