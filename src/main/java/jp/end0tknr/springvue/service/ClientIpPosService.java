package jp.end0tknr.springvue.service;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class ClientIpPosService {
	 Logger logger = LoggerFactory.getLogger( ClientIpPosService.class );

    public Map<String,String> getClientIp(HttpServletRequest request) {
    	String ip = request.getRemoteAddr();

        String xForwardedFor =  request.getHeader("X-Forwarded-For");
        //ELB由の場合
        if (xForwardedFor != null) {
        	ip = xForwardedFor;
        }

        String ip_type = calcIpType(ip);

        Map<String, String> map = new HashMap<>();
        map.put("ip",      ip);
        map.put("ip_type", ip_type);
        return map;
    }

    // refer to https://qiita.com/Nobu12/items/211ffa773c1758578b1c
    private String calcIpType(String client_ip) {

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
