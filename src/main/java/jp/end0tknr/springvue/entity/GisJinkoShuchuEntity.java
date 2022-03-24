package jp.end0tknr.springvue.entity;

import java.util.Date;
import java.util.List;

public class GisJinkoShuchuEntity extends GisEntityAbstract {

    private Integer gid;
    private Integer a16_001;
    private String a16_002;
    private String a16_003;
    private Short a16_004;
    private Integer a16_005;
    private Double a16_006;
    private Integer a16_007;
    private Double a16_008;
    private Double a16_009;
    private Double a16_010;
    private Date a16_011;
    private String geom;
	private String geom_text;

    public Integer getGid() {		return gid;}
    public Integer getA16_001(){	return a16_001;}
    public String getA16_002() {	return a16_002;}
    public String getA16_003() {	return a16_003;}
    public Short getA16_004()  {	return a16_004;}
    public Integer getA16_005(){	return a16_005;}
    public Double getA16_006() {	return a16_006;}
    public Integer getA16_007(){	return a16_007;}
    public Double getA16_008() {	return a16_008;}
    public Double getA16_009() {	return a16_009;}
    public Double getA16_010() {	return a16_010;}
    public Date getA16_011() {	    return a16_011;}
	public List<Double> getGeom() {
		return convGeomText2Coords(geom_text);
	}
}