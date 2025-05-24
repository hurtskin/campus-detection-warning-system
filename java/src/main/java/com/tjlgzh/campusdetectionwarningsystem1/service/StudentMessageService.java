package com.tjlgzh.campusdetectionwarningsystem1.service;


import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.StudentMessagePageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;

public interface StudentMessageService {

    PageResult page(StudentMessagePageDTO dto);
}
