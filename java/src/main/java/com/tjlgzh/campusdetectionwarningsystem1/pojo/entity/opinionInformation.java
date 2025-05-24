package com.tjlgzh.campusdetectionwarningsystem1.pojo.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class opinionInformation {
    private Long id;
    private LocalDateTime time;
    private String place;
    private String eventType;
    private String courseEvent;
    private String handleSchool;
    private String socialImpact;
}
