package jp.end0tknr.springvue.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DemoRestController {

    @RequestMapping("/hoge")
    public String index() {
        return "Hello Spring Boot !!";
    }
}
