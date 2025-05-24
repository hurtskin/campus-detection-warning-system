package com.tjlgzh.campusdetectionwarningsystem1.controller;


import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.opinionInformationPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.result.Result;
import com.tjlgzh.campusdetectionwarningsystem1.service.opinionInformationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/opinionInformation")
@Slf4j
public class opinionInformationController {
    @Autowired
    private opinionInformationService opinionInformationService;
    @PostMapping("/page")
    public Result<PageResult> page(@RequestBody opinionInformationPageDTO dto){
        log.info("分页查询：{}",dto);
        PageResult pageResult = opinionInformationService.page(dto);
        return Result.success(pageResult);
    }
    @PostMapping("/add")
    public Result add(@RequestBody opinionInformationPageDTO dto){
        log.info("添加数据：{}",dto);
        opinionInformationService.add(dto);
        return Result.success();
    }
    //删除
    @PostMapping("/delete")
    public Result batchDelete(@RequestBody List<Long> ids){
        log.info("根据ids删除数据：{}",ids);
        opinionInformationService.batchDelete(ids);
        return Result.success();
    }
}
