package com.tjlgzh.campusdetectionwarningsystem1.pojo.dto;

import lombok.Data;

@Data
public class schoolOpinionPageDTO {
    private String name;
    private int page;

    //每页显示记录数
    private int pageSize;
}
