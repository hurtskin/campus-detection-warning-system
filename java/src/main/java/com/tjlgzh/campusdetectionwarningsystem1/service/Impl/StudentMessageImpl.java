package com.tjlgzh.campusdetectionwarningsystem1.service.Impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;

import com.tjlgzh.campusdetectionwarningsystem1.mapper.StudentMessageMapper;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.StudentMessagePageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.StudentMessage;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.service.StudentMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class StudentMessageImpl implements StudentMessageService {
    @Autowired
    private StudentMessageMapper studentMessageMapper;
    @Override
    public PageResult page(StudentMessagePageDTO dto) {
        int offset = (dto.getPage() - 1) * dto.getPageSize();

        // 设置分页参数
        dto.setOffset(offset);  // 设置偏移量
        dto.setPageSize(dto.getPageSize());  // 设置每页大小

        // 执行分页查询
        List<StudentMessage> result = studentMessageMapper.page(dto);

        // 计算总记录数
        long total = studentMessageMapper.countTotal(dto);

        // 返回分页结果
        return new PageResult(total, result);
    }
}
