package jp.end0tknr.springvue.entity;

import java.util.Date;

public class NewbuildSalesCountByShopCityScaleEntity {
	private String pref;
    private String city;
    private String shop;
    private Date calc_date;
    private String scale_sales;

    public String getPref() {        return pref;    }
    public String getCity() {        return city;    }
    public String getShop() {        return shop;    }
    public Date getCalc_date() {     return calc_date;}
    public String getScale_sales() { return scale_sales;}
}