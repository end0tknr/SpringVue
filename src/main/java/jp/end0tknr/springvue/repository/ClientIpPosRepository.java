package jp.end0tknr.springvue.repository;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import jp.end0tknr.springvue.entity.ClientIpPosEntity;

@Mapper
public interface ClientIpPosRepository {

    @Select("SELECT * FROM client_ip_pos "+
    		" WHERE client_ip='${clientIp}'")
    ClientIpPosEntity getClientPos(String clientIp);
}
