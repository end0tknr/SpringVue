package jp.end0tknr.springvue.entity;

import java.util.Date;

public class SumStockSalesCountByShopEntity {
    private String pref;
    private String shop;
    private Date calc_date;

    private Integer onsale_count;
    private Long    onsale_price;
    private Integer onsale_days;
    private Integer discuss_count;
    private Long    discuss_price;
    private Integer discuss_days;

    public String getPref() {       return pref;   }
    public String getShop() {       return shop;   }
    public Date getCalc_date() {    return calc_date;   }

    public Integer getOnsale_count(){  return onsale_count; }
    public Long    getOnsale_price(){  return onsale_price; }
    public Integer getOnsale_days() {  return onsale_days;  }

    public Integer getDiscuss_count(){ return discuss_count; }
    public Long    getDiscuss_price(){ return discuss_price; }
    public Integer getDiscuss_days() { return discuss_days;  }
}