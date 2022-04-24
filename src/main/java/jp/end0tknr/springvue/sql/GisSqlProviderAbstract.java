package jp.end0tknr.springvue.sql;

import java.util.List;

import org.apache.commons.lang3.StringUtils;

public abstract class GisSqlProviderAbstract {
	private String selectLimit = "200";

	public String toTblName() {
    	String tblName	= toSnakeStr( this.getClass().getSimpleName() );
    	tblName = tblName.replace("_sql_provider","");
		return tblName;
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

    public String sqlFindByCoord(List<Double> coord) {

    	String sqlStr =
    			" SELECT *, ST_AsText(geom) as geom_text "+
    			" FROM " + toTblName() +
    			" WHERE "+
    			" lng BETWEEN "+ coord.get(3).toString() +" AND " +
                coord.get(1).toString() +" AND " +
                " lat BETWEEN "+ coord.get(2).toString() +" AND " +
                coord.get(0).toString() +
    			" ORDER BY lat DESC, lng "+
    			" LIMIT "+selectLimit;
    	//System.out.println( sqlStr );

    	 return sqlStr;
    }

}
