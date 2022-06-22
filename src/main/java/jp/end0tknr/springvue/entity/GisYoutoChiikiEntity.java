package jp.end0tknr.springvue.entity;

public class GisYoutoChiikiEntity extends GisEntityAbstract {

    private Integer gid;
    private String a29_001;
    private String a29_002;
    private String a29_003;
    private Short a29_004;
    private String a29_005;
    private Integer a29_006;
    private Integer a29_007;
    private String a29_008;

	private Double lng;
	private Double lat;
	@Override
	public Double getLng() {		return lng;		}
	@Override
	public Double getLat() {		return lat;		}

    public Integer getGid() {		return gid;    }
    public String getA29_001() {	return a29_001;}
    public String getA29_002() {	return a29_002;}
    public String getA29_003() {	return a29_003;}
    public Short getA29_004() {		return a29_004;}
    public String getA29_005() {	return a29_005;}
    public Integer getA29_006() {	return a29_006;}
    public Integer getA29_007() {	return a29_007;}
    public String getA29_008() {	return a29_008;}

}