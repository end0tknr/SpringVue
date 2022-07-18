package jp.end0tknr.springvue.entity;

import java.util.regex.Pattern;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ClientIpPosEntity {
	 Logger logger = LoggerFactory.getLogger( ClientIpPosEntity.class );

	private String client_ip;
	private String ip_type;
    private Double lng;
    private Double lat;
    private String pref;
    private String city;

    public String getClient_ip() {			return client_ip;  }
    public String getIp_type() {			return ip_type;    }
    public Double getLng() {        		return lng;    		}
    public Double getLat() {        		return lat;    		}
    public String getPref() {        		return pref;      	}
    public String getCity() {        		return city;    	}

    public void setClient_ip(String client_ip) {
    	this.client_ip = client_ip;
    	logger.info("IP "+ client_ip);

    	String ip_type_tmp = calcIp_type(client_ip);
    	logger.info("IP TYPE "+ip_type_tmp);
    	this.ip_type = ip_type_tmp;
    }

    public void setLng(Double lng) {       this.lng = lng;    }
    public void setLat(Double lat) {       this.lat = lat;    }
    public void setPref(String pref) {     this.pref = pref;  }
    public void setCity(String city) {		this.city = city;  }

    // refer to https://qiita.com/Nobu12/items/211ffa773c1758578b1c
    private String calcIp_type(String client_ip) {

    	String[] addressList = client_ip.split(Pattern.quote("."));

    	if (addressList.length < 4) {
    		return null;
    	}

        int firstSet  = Integer.valueOf( addressList[0] );
        int secondSet = Integer.valueOf( addressList[1] );

        // LOCAL
        if (firstSet == 127) {
        	return "private";
        }
        // CLASS A
        if (firstSet == 10) {
        	return "private";
        }
        // CLASS B
        if (firstSet == 172) {
        	 if (16 <= secondSet && secondSet <= 31) {
             	return "private";
        	 }
          	return "global";
        }
        // CLASS C
        if (firstSet == 192 && secondSet == 168 ) {
            return "private";
        }
      	return "global";
    }




}