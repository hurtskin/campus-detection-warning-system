package com.tjlgzh.campusdetectionwarningsystem1.controller;


import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.schoolOpinionPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.result.Result;
import com.tjlgzh.campusdetectionwarningsystem1.service.schoolOpinionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/schoolOpinion")
@Slf4j
public class schoolOpinionController {
    @Autowired
    private schoolOpinionService schoolOpinion;
    @PostMapping("/page")
    public Result<PageResult> page(@RequestBody schoolOpinionPageDTO dto){
        log.info("分页查询:{}",dto);
        PageResult pageResult = schoolOpinion.page(dto);
        return Result.success(pageResult);
    }
}
