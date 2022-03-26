package jp.end0tknr.springvue.entity;

public class GisEntity {

	private String data_name;
	private String column_name;
	private String data_type;
	private String description;
	private Integer kbyte;
	private Integer rows;

	public String getColumn_name() {	return column_name;	}
	public String getData_type() {		return data_type;	}
	public String getDescription() {	return description;	}
	public String getData_name() {		return data_name;	}
	public Integer getKbyte() {			return kbyte;		}
	public Integer getRows() {			return rows;		}
}
