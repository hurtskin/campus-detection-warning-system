package com.tjlgzh.campusdetectionwarningsystem1.service.Impl;



import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.tjlgzh.campusdetectionwarningsystem1.mapper.OpinionInformationMapper;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.dto.opinionInformationPageDTO;
import com.tjlgzh.campusdetectionwarningsystem1.pojo.entity.opinionInformation;
import com.tjlgzh.campusdetectionwarningsystem1.result.PageResult;
import com.tjlgzh.campusdetectionwarningsystem1.service.opinionInformationService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Objects;

@Service
@Slf4j
public class opinionInformationImpl implements opinionInformationService {
    @Autowired
    private OpinionInformationMapper opinionInformationMapper;
    @Override
    public PageResult page(opinionInformationPageDTO dto) {
        // 开始分页
        // 计算 offset
        int offset = (dto.getPage() - 1) * dto.getPageSize(); // 计算偏移量

        // 设置分页参数
        dto.setOffset(offset);
        dto.setPageSize(dto.getPageSize());

        // 设置时间范围（根据用户输入的时间范围进行处理）
        if (Objects.equals(dto.getTimeHorizon(), "今天")) {
            dto.setTime(LocalDateTime.now().minusDays(1));
        } else if (Objects.equals(dto.getTimeHorizon(), "前三天")) {
            dto.setTime(LocalDateTime.now().minusDays(3));
        } else if (Objects.equals(dto.getTimeHorizon(), "近七天")) {
            dto.setTime(LocalDateTime.now().minusWeeks(1));
        } else if (Objects.equals(dto.getTimeHorizon(), "近30天")) {
            dto.setTime(LocalDateTime.now().minusMonths(1));
        } else {
            // 其他情况按时间解析
            if (dto.getTimeHorizon() != null && !dto.getTimeHorizon().isEmpty()) {
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
                try {
                    LocalDateTime dateTime = LocalDateTime.parse(dto.getTimeHorizon(), formatter);
                    log.info("解析后的日期时间: {}", dateTime);
                    dto.setTime(dateTime);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

        // 执行分页查询
        List<opinionInformation> result = opinionInformationMapper.page(dto);

        // 获取总记录数和分页数据
        long total = opinionInformationMapper.countTotal(dto);


        // 返回分页结果
        return new PageResult(total, result);
    }

    //添加数据
    @Override
    public void add(opinionInformationPageDTO dto) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
        try {
            LocalDateTime dateTime = LocalDateTime.parse(dto.getTimeHorizon(), formatter);
            log.info("解析后的日期时间:{}",dateTime);
            dto.setTime(dateTime);
        } catch (Exception e) {
            e.printStackTrace();
        }
        opinionInformation opinionInformation = new opinionInformation();
        BeanUtils.copyProperties(dto,opinionInformation);
        opinionInformation.setEventType(dto.getClassification());
        opinionInformationMapper.add(opinionInformation);
    }

    @Override
    public void batchDelete(List<Long> ids) {
        opinionInformationMapper.batchDelete(ids);
    }
}

