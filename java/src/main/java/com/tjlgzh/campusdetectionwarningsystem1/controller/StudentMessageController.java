package com.tjlgzh.campusdetectionwarningsystem1.controller;


import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.StudentMessagePageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.result.Result;
import com.tjlgzh.campusdetectionwarningsystem1.service.StudentMessageService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/studentMessage")
@Slf4j
public class StudentMessageController {
    @Autowired
    private StudentMessageService studentMessageService;
    @PostMapping("/page")
    public Result<PageResult> page(@RequestBody StudentMessagePageDTO dto){
        log.info("分页查询:{}",dto);
        PageResult pageResult = studentMessageService.page(dto);
        return Result.success(pageResult);
    }
}
