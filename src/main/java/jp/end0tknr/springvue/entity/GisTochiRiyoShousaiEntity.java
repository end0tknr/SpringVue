package jp.end0tknr.springvue.entity;

import java.util.List;

public class GisTochiRiyoShousaiEntity extends GisEntityAbstract {
    private Integer gid;

    private String l03b_c_001;
    private String l03b_c_002;
    private String l03b_c_003;
    private String l03b_c_004;
	private String geom;
	private String geom_text;

    public Integer getGid() {	return gid;  }
    public String getL03b_c_001() {	return l03b_c_001;}
    public String getL03b_c_002() {	return l03b_c_002;}
    public String getL03b_c_003() {	return l03b_c_003;}
    public String getL03b_c_004() {	return l03b_c_004;}
	public List<Double> getGeom() {
		return convGeomText2Coords(geom_text);
	}
}