package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.GisChikaEntity;
import jp.end0tknr.springvue.repository.GisChikaRepository;

@Service
public class GisChikaService {

    @Autowired
    GisChikaRepository gisChikaRepository;

    public  List<GisChikaEntity> findByAddress(String address) {
        return gisChikaRepository.findByAddress(address);
    }

}
