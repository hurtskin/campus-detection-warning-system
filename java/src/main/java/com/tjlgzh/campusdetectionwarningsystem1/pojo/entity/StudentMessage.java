package com.tjlgzh.campusdetectionwarningsystem1.pojo.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentMessage {
    private Integer id;
    private String name;
    private String major;
    private String grade;
    private String sex;
}
