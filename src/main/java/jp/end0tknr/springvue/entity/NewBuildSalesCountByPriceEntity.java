package jp.end0tknr.springvue.entity;

import java.util.Date;

public class NewBuildSalesCountByPriceEntity {
    private String  pref;
    private String  city;
    private Integer price;
    private Date    calc_date;

    private Integer onsale_count;
    private Integer onsale_days;
    private Integer discuss_count;
    private Integer discuss_days;
    private Float   sold_count;

    public String getPref() {          return pref;         }
    public String getCity() {          return city;         }
    public Integer getPrice() {        return price;        }
    public Date getCalc_date() {       return calc_date;    }
    public Integer getOnsale_count() { return onsale_count; }
    public Integer getOnsale_days()  { return onsale_days;  }
    public Integer getDiscuss_count(){ return discuss_count;}
    public Integer getDiscuss_days() { return discuss_days; }
    public Float   getSold_count(){    return sold_count;   }

}