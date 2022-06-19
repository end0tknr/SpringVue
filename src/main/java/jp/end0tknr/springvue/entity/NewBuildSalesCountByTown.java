package jp.end0tknr.springvue.entity;

import java.util.Date;

public class NewBuildSalesCountByTown {
    private String pref;
    private String city;
    private String town;
    private Date calc_date;
    private Integer calc_days;
    private Integer sold_count;
    private Long sold_price;
    private Integer sold_days;
    private Integer on_sale_count;
    private Long on_sale_price;
    private Integer on_sale_days;

    public String getPref() {          return pref;         }
    public String getCity() {          return city;         }
    public String getTown() {          return town;         }
    public Date getCalc_date() {       return calc_date;    }
    public Integer getCalc_days() {    return calc_days;    }
    public Integer getSold_count() {   return sold_count;   }
    public Long getSold_price() {      return sold_price;   }
    public Integer getSold_days() {    return sold_days;    }
    public Integer getOn_sale_count() {return on_sale_count;}
    public Long getOn_sale_price() {   return on_sale_price;}
    public Integer getOn_sale_days() { return on_sale_days; }

    public void setPref(String pref) {      		this.pref = pref;    		}
    public void setCity(String city) {             this.city = city;    		}
    public void setTown(String town) {      		this.town = town;			}
    public void setCalc_date(Date calc_date) {     this.calc_date = calc_date; }
    public void setCalc_days(Integer calc_days) {  this.calc_days = calc_days; }
    public void setSold_count(Integer sold_count) {this.sold_count = sold_count;}
    public void setSold_price(Long sold_price) {   this.sold_price = sold_price;}
    public void setSold_days(Integer sold_days) {  this.sold_days = sold_days;  }
    public void setOn_sale_count(Integer on_sale_count) {   this.on_sale_count = on_sale_count;}
    public void setOn_sale_price(Long on_sale_price) {   this.on_sale_price = on_sale_price;   }
    public void setOn_sale_days(Integer on_sale_days) {  this.on_sale_days = on_sale_days;     }
}