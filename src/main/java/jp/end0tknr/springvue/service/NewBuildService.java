package jp.end0tknr.springvue.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import jp.end0tknr.springvue.entity.NewBuildSalesCountByCity;
import jp.end0tknr.springvue.entity.NewBuildSalesCountByShop;
import jp.end0tknr.springvue.repository.NewBuildRepository;

@Service
public class NewBuildService {

    @Autowired
    NewBuildRepository newBuildRepository;

    public  List<NewBuildSalesCountByShop>
    getSalesCountByShop(String prefName) {
    	return newBuildRepository.getSalesCountByShop(prefName);
    }

    public  List<NewBuildSalesCountByCity>
    getSalesCountByCity(String prefName) {
    	return newBuildRepository.getSalesCountByCity(prefName);
    }


}
