DROP TABLE IF EXISTS `user_info`;
DROP TABLE IF NOT EXISTS `user_info`(
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(100) NOT NULL COMMENT '用户ID',
    username VARCHAR(100) UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) COMMENT '密码',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE INDEX `user_id_unique_index` (`user_id`)
) default charset=utf8 COMMENT '用户表';

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
    attachment_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
    user_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
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
    role_id VARCHAR(50) NOT NULL COMMENT '角色ID',
    user_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
    role_name VARCHAR(100) NOT NULL COMMENT '角色内容'
) default charset=utf8 COMMENT '角色信息表';