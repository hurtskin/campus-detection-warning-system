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
public class schoolOpinion {
    private Long id;
    private Integer infoAttr;
    private String title;
    private String content;
    private LocalDateTime time;
    private String word;
    private String issuer;
    private String region;
}
