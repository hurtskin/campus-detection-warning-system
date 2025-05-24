package com.tjlgzh.campusdetectionwarningsystem1.service;


import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.schoolOpinionPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;

public interface schoolOpinionService {
    PageResult page(schoolOpinionPageDTO dto);
}
