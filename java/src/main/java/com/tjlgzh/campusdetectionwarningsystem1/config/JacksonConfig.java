package com.tjlgzh.campusdetectionwarningsystem1.config;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class JacksonConfig {

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper objectMapper = new ObjectMapper();
        // 禁用未知属性失败特性，防止因前端传入多余字段导致反序列化失败
        objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        // 允许将空字符串视为空对象，在特定场景下可处理空值传递问题
        objectMapper.configure(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT, true);
        // 可继续添加其他针对 ArrayList<Long> 处理有益的配置
        // 例如，设置 Long 类型的反序列化处理方式，如果有特殊需求的话
        // objectMapper.configure(DeserializationFeature., value);

        return objectMapper;
    }
}