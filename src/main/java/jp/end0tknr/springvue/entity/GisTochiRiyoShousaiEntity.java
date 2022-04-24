package jp.end0tknr.springvue.entity;

public class GisTochiRiyoShousaiEntity extends GisEntityAbstract {
    private Integer gid;

    private String l03b_c_001;
    private String l03b_c_002;
    private String l03b_c_003;
    private String l03b_c_004;

	private Double lng;
	private Double lat;
	public Double getLng() {		return lng;		}
	public Double getLat() {		return lat;		}

    public Integer getGid() {	return gid;  }
    public String getL03b_c_001() {	return l03b_c_001;}
    public String getL03b_c_002() {	return l03b_c_002;}
    public String getL03b_c_003() {	return l03b_c_003;}
    public String getL03b_c_004() {	return l03b_c_004;}
}