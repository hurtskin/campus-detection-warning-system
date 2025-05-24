package com.tjlgzh.campusdetectionwarningsystem1.service;



import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.opinionInformationPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;

import java.util.List;

public interface opinionInformationService {

    PageResult page(opinionInformationPageDTO dto);

    void add(opinionInformationPageDTO dto);

    void batchDelete(List<Long> ids);
}
