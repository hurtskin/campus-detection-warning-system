package com.tjlgzh.campusdetectionwarningsystem1.mapper;

import com.github.pagehelper.Page;

import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.schoolOpinionPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.schoolOpinion;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface SchoolOpinionMapper {
    Page<schoolOpinion> page(schoolOpinionPageDTO dto);
}
