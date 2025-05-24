package com.tjlgzh.campusdetectionwarningsystem1.service.Impl;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;

import com.tjlgzh.campusdetectionwarningsystem1.mapper.SchoolOpinionMapper;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.schoolOpinionPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.schoolOpinion;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.service.schoolOpinionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class schoolOpinionImpl implements schoolOpinionService {
    @Autowired
    private SchoolOpinionMapper schoolOpinionMapper;
    @Override
    public PageResult page(schoolOpinionPageDTO dto) {
        PageHelper.startPage(dto.getPage(),dto.getPageSize());
        Page<schoolOpinion> page = schoolOpinionMapper.page(dto);
        Long total = page.getTotal();
        List<schoolOpinion> result = page.getResult();
        return new PageResult(total,result);
    }
}
