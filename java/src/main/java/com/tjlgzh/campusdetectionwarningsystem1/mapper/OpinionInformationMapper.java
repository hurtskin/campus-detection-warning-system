package com.tjlgzh.campusdetectionwarningsystem1.mapper;

import com.github.pagehelper.Page;

import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.opinionInformationPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.opinionInformation;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface OpinionInformationMapper {
    Page<opinionInformation> page(opinionInformationPageDTO dto);

    void add(opinionInformation opinionInformation);

    void batchDelete(List<Long> ids);

    long countTotal(opinionInformationPageDTO dto);
}

