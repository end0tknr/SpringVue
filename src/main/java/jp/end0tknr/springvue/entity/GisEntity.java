package jp.end0tknr.springvue.entity;

public class GisEntity {

	private String data_name;
	private String column_name;
	private String data_type;
	private String description;
	private Integer kbyte;

	public String getColumn_name() {
		return column_name;
	}
	public void setColumn_name(String column_name) {
		this.column_name = column_name;
	}
	public String getData_type() {
		return data_type;
	}
	public void setData_type(String data_type) {
		this.data_type = data_type;
	}
	public String getDescription() {
		return description;
	}
	public void setDescription(String description) {
		this.description = description;
	}
	public String getData_name() {
		return data_name;
	}
	public void setData_name(String data_name) {
		this.data_name = data_name;
	}
	public Integer getKbyte() {
		return kbyte;
	}
	public void setKbyte(Integer kbyte) {
		this.kbyte = kbyte;
	}
}
