package jp.end0tknr.springvue.entity;

import java.util.Date;

public class NewBuildSalesCountByTownEntity {
    private String pref;
    private String city;
    private String town;
    private Date calc_date;
    private Integer onsale_count;
    private Long    onsale_price;
    private Integer onsale_days;
    private Integer discuss_count;
    private Long    discuss_price;
    private Integer discuss_days;
    private Float   sold_count;
    private Long    sold_price;

    public String getPref() {       return pref;   }
    public String getCity() {       return city;   }
    public String getTown() {       return town;   }
    public Date getCalc_date() {    return calc_date;   }

    public Integer getOnsale_count(){  return onsale_count; }
    public Long    getOnsale_price(){  return onsale_price; }
    public Integer getOnsale_days() {  return onsale_days;  }

    public Integer getDiscuss_count(){ return discuss_count; }
    public Long    getDiscuss_price(){ return discuss_price; }
    public Integer getDiscuss_days() { return discuss_days;  }

    public Float   getSold_count() {   return sold_count;  }
    public Long    getSold_price() {   return sold_price;  }



}