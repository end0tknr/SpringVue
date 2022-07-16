package jp.end0tknr.springvue.entity;

import java.util.Date;

public class NewbuildSalesCountByCityScaleEntity {
    private String pref;
    private String city;
    private Date calc_date;
    private String scale_sales;

    public String getPref() {        return pref;    }
    public String getCity() {        return city;    }
    public Date getCalc_date() {     return calc_date;  }
    public String getScale_sales() { return scale_sales;}  // json string
}