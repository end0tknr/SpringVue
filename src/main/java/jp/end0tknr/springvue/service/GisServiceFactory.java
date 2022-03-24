package jp.end0tknr.springvue.service;

import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;

import jp.end0tknr.springvue.entity.GisEntity;
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

    public abstract List<HashMap> findByCoord(List coord);
}
