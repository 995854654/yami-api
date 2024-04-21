create table `user_info`(
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL COMMENT '用户ID',
    username VARCHAR(255) COMMENT '用户名',
    password VARCHAR(255) COMMENT '密码',
    UNIQUE INDEX `user_id_unique_index` (`user_id`)
) default charset=utf8 COMMENT '用户表';

create table `user_profile` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
    `name` VARCHAR(100) NOT NULL COMMENT '用户姓名',
    email VARCHAR(255) NOT NULL COMMENT '邮箱',
    avatar_path VARCHAR(255) NOT NULL COMMENT '头像地址'
) default charset=utf8 COMMENT '用户信息表';

create table `attachment_info` (
    `id` int not null PRIMARY KEY AUTO_INCREMENT,
    attachment_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
    user_id VARCHAR(255) NOT NULL COMMENT '跟用户绑定的用户ID',
    filename VARCHAR(255) NOT NULL COMMENT '文件名称',
    filetype VARCHAR(25) COMMENT '文件类型',
    filesize VARCHAR(100) COMMENT '文件大小',
    filepath VARCHAR(255) COMMENT '文件路径',
   UNIQUE INDEX `attachment_id_unique_index` (`attachment_id`)
) default charset=utf8 COMMENT '附件信息表';