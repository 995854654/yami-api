DROP TABLE IF EXISTS `user_info`;
create TABLE IF NOT EXISTS `user_info`(
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL COMMENT '用户ID',
    username VARCHAR(100) UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) COMMENT '密码',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX `user_id_unique_index` (`user_id`)
) default charset=utf8 COMMENT '用户表';

INSERT INTO user_info(`user_id`, `username`, `password`) VALUES
('admin', 'admin', '$2b$12$PB/gsWbFHgUPJO55GvqcseHhARPd5mmo2eLQ4wcSUGt0MHMbOZg8K');

DROP TABLE IF EXISTS `user_profile`;
create TABLE IF NOT EXISTS `user_profile` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL COMMENT '跟用户绑定的用户ID',
    `name` VARCHAR(100) NOT NULL COMMENT '用户姓名',
    email VARCHAR(255) NOT NULL COMMENT '邮箱',
    avatar_path VARCHAR(255) NOT NULL COMMENT '头像地址',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset=utf8 COMMENT '用户信息表';

DROP TABLE IF EXISTS `attachment_info`;
CREATE table IF NOT EXISTS `attachment_info` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    attachment_id VARCHAR(100) NOT NULL COMMENT '文件ID',
    user_id VARCHAR(100) NOT NULL COMMENT '跟用户绑定的用户ID',
    filename VARCHAR(255) NOT NULL COMMENT '文件名称',
    filetype VARCHAR(25) COMMENT '文件类型',
    filesize VARCHAR(255) COMMENT '文件大小',
    filesize_format VARCHAR(255) COMMENT '文件大小，按照标准格式输出',
    filepath VARCHAR(255) COMMENT '文件路径',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   UNIQUE INDEX `attachment_id_unique_index` (`attachment_id`)
) default charset=utf8 COMMENT '附件信息表';

-- 一个用户可以有多个角色
DROP TABLE IF EXISTS `user_role`;
CREATE TABLE IF NOT EXISTS `user_role` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    role_id VARCHAR(100) NOT NULL COMMENT '角色ID',
    user_id VARCHAR(100) NOT NULL COMMENT '跟用户绑定的用户ID',
    role_name VARCHAR(100) NOT NULL COMMENT '角色内容'
) default charset=utf8 COMMENT '角色信息表';


-- LLM chat model
DROP TABLE IF EXISTS `llm_model`;
CREATE TABLE IF NOT EXISTS `llm_model` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    model_id VARCHAR(100) NOT NULL COMMENT 'LLM模型ID',
    model_type VARCHAR(255) NOT NULL COMMENT '模型类别',
    model_name VARCHAR(255) NOT NULL COMMENT '模型名称',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) default charset=utf8 COMMENT 'LLM模型表';

-- functional module
DROP TABLE IF EXISTS `function_module`;
CREATE TABLE IF NOT EXISTS `function_module` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    module_id VARCHAR(100) NOT NULL COMMENT '模块 ID',
    module_name VARCHAR(255) NOT NULL COMMENT '模块名称',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) default charset=utf8 COMMENT '功能模块表';

-- background job table
DROP TABLE IF EXISTS `background_job`;
CREATE TABLE IF NOT EXISTS `background_job` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    job_id VARCHAR(100) NOT NULL COMMENT '任务ID',
    job_type VARCHAR(255) NOT NULL COMMENT '任务类型',
    `creator` VARCHAR(255) NOT NULL COMMENT '创建者',
    `description` VARCHAR(255) NULL COMMENT '描述',
    `status` VARCHAR(100) NOT NULL COMMENT '进度',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP
) default charset=utf8 COMMENT '后台任务表';

-- resource table
DROP TABLE IF EXISTS `resource_info`;
CREATE TABLE IF NOT EXISTS `resource_info` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    resource_id VARCHAR(100) NOT NULL COMMENT '资源ID',
    job_id VARCHAR(100) NOT NULL COMMENT '对应后台任务的ID',
    user_id VARCHAR(100) NOT NULL COMMENT '对应用户的ID',
    resource_name VARCHAR(255) NOT NULL COMMENT '资源名称',
    data_source VARCHAR(255) NULL COMMENT '来源',
    resource_url TEXT NOT NULL COMMENT '资源的路径',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
) default charset=utf8 COMMENT '资源信息表';

