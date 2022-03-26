package jp.end0tknr.springvue.service;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

import jp.end0tknr.springvue.entity.GisEntity;
import jp.end0tknr.springvue.entity.GisEntityAbstract;
import jp.end0tknr.springvue.repository.GisRepository;


public abstract class GisServiceFactory {

    @Autowired
    GisRepository gisRepository;

	@Value("${spring.datasource.dbname}")
	private String dbName;

	public String tblName() {
    	String tblName	= toSnakeStr( this.getClass().getSimpleName() );
    	tblName = tblName.replace("_service","");
    	return tblName;
	}

    public  HashMap<String,String> getDescedColumnDefs4Disp() {
    	HashMap<String,String> colDefs	= getDescedColumnDefs();
    	String[] descsForDisp = descsForDisp();

    	List<String> delColNames = new ArrayList<String>();

        for (String colName : colDefs.keySet()) {
            String description = colDefs.get(colName);
            if(Arrays.asList(descsForDisp).contains(description)){
            	continue;
            }
            delColNames.add(colName);
        }

        for (String colName : delColNames) {
            colDefs.remove(colName);
        }
        return colDefs;
    }

    public  HashMap<String,String> getDescedColumnDefs() {
    	String tblName	= tblName();

    	HashMap<String,String> retMap = new HashMap<>();
    	List<GisEntity> entries =
    			gisRepository.getDescedColumnDefs(dbName,tblName);

    	for (GisEntity entity : entries ) {
    		retMap.put(entity.getColumn_name(),entity.getDescription());
    	}
        return retMap;
    }

    public static String toBeanName(String dataName ) {
    	return toCamelStr(dataName) + "Service";
    }

    private static String toCamelStr(String snake) {
        if( StringUtils.isEmpty(snake) ) {
            return snake;
        }

        StringBuilder sb =
        		new StringBuilder(snake.length() + snake.length());

        for (int i = 0; i < snake.length(); i++) {
        	char c = snake.charAt(i);
            if (c == '_') {
            	if((i + 1) < snake.length()) {
            		sb.append( Character.toUpperCase(snake.charAt(++i)) );
            	} else {
            		sb.append( "" );
            	}
            	continue;
            }

            if(sb.length()==0 && i!=0) {
            	sb.append( Character.toUpperCase(c));
            	continue;
            }

            sb.append( Character.toLowerCase(c));
        }
        return sb.toString();
    }


    public String toSnakeStr(String camel) {
        String snake =
                StringUtils.join(
                        StringUtils.splitByCharacterTypeCamelCase(camel), "_")
                .toLowerCase();
        //数字の前には「_」不要
        snake = snake.replaceAll("(_)([0-9])", "$2");

        return snake;
    }


    //public abstract List<HashMap> findByCoord(List coord);
    public abstract List<GisEntityAbstract> findByCoordFromRepo(List coord);
    public abstract String[] descsForDisp();


    public  List<HashMap> findByCoord(List coord) {

    	List<HashMap> retEntities = new ArrayList<HashMap>();
    	if( coord.size() != 4) {
    		return retEntities;
    	}

    	HashMap<String,String> colDefs	= getDescedColumnDefs4Disp();

    	for( GisEntityAbstract tmpEntity :
    		(List<GisEntityAbstract>) findByCoordFromRepo(coord) ) {

    		HashMap<String,Object> retEntity = new HashMap();

    	    for (Field field : tmpEntity.getClass().getDeclaredFields() ){
    	    	field.setAccessible(true);

    	    	String fieldName = field.getName();

    	    	if (! colDefs.containsKey(fieldName) ) {
    	    		continue;
    	    	}

    	    	try {
					retEntity.put( colDefs.get(fieldName), field.get(tmpEntity));
				} catch (IllegalArgumentException | IllegalAccessException e) {
					e.printStackTrace();
				}
    	    }
    	    retEntity.put( "geom", tmpEntity.getGeom() );
    	    retEntities.add(retEntity);
    	}

    	return retEntities;
    }

}
