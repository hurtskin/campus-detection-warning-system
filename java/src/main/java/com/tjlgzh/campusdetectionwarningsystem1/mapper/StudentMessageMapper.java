package com.tjlgzh.campusdetectionwarningsystem1.mapper;

import com.github.pagehelper.Page;

import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.StudentMessagePageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.StudentMessage;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface StudentMessageMapper {
    Page<StudentMessage> page(StudentMessagePageDTO dto);

    long countTotal(StudentMessagePageDTO dto);
}
