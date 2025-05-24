package com.tjlgzh.campusdetectionwarningsystem1.pojo.dto;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class opinionInformationPageDTO {
    private int page;
    //每页显示记录数
    private int pageSize;
    private int offset;
    private String timeHorizon;
    private String context;
    private String classification;
    private LocalDateTime time;
    private String place;
    private String courseEvent;
    private String handleSchool;
    private String socialImpact;
}
