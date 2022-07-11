package jp.end0tknr.springvue.entity;

public class TownProfile {

	private String pref;
    private String city;
    private String town;
    private Double lng;
    private Double lat;
    private String summary;

    public String getPref(){        return pref;    }
    public String getCity(){        return city;    }
    public String getTown(){        return town;    }
    public Double getLng() {        return lng;     }
    public Double getLat() {        return lat;     }
    public String getSummary() {    return summary; }

    public void setPref(String pref) {     this.pref = pref;    }
    public void setCity(String city) {     this.city = city;    }
    public void setTown(String town) {     this.town = town;    }
    public void setLng(Double lng) {       this.lng = lng;      }
    public void setLat(Double lat) {       this.lat = lat;      }
    public void setSummary(String summary){this.summary = summary;}
}