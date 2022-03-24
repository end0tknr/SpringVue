package jp.end0tknr.springvue.entity;

import java.util.List;

public class GisGyoseiKuikiEntity extends GisEntityAbstract {
    private Integer gid;
    private String n03_001;
    private String n03_002;
    private String n03_003;
    private String n03_004;
    private String n03_007;
    private String geom;
	private String geom_text;


    public Integer getGid() {		return gid;}
    public String getN03_001() {	return n03_001;}
    public String getN03_002() {	return n03_002;}
    public String getN03_003() {	return n03_003;}
    public String getN03_004() {	return n03_004;}
    public String getN03_007() {	return n03_007;}
	public List<Double> getGeom() {
		return convGeomText2Coords(geom_text);
	}

}