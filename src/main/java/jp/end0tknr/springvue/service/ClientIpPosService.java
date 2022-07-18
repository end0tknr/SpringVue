package jp.end0tknr.springvue.service;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.ClientIpPosEntity;
import jp.end0tknr.springvue.repository.ClientIpPosRepository;

@Service
public class ClientIpPosService {
	 Logger logger = LoggerFactory.getLogger( ClientIpPosService.class );

    @Autowired
    ClientIpPosRepository clientIpPosRepository;

    public  ClientIpPosEntity getClientPos(HttpServletRequest request) {
    	String clientIp = getClientIp(request);
    	ClientIpPosEntity clientIpPos = clientIpPosRepository.getClientPos(clientIp);
    	if (clientIpPos != null ) {
        	return clientIpPos;
    	}

    	logger.info("unknown ip address "+ clientIp );

    	clientIpPos = new ClientIpPosEntity();
    	clientIpPos.setClient_ip(clientIp);
    	return clientIpPos;
    }

    public String getClientIp(HttpServletRequest request) {
        String xForwardedFor =  request.getHeader("X-Forwarded-For");

        //ELB由の場合
        if (xForwardedFor != null) {
            return xForwardedFor;
        }
        return request.getRemoteAddr();
    }

    public ClientIpPosEntity getInitClientPos( String clientIp ) {
    	ClientIpPosEntity clientIpPos = new ClientIpPosEntity();
    	clientIpPos.setClient_ip(clientIp);
    	return clientIpPos;
    }
}
