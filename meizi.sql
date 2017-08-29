DROP DATABASE IF EXISTS chaoxiubang;
CREATE DATABASE chaoxiubang;
USE chaoxiubang;
DROP TABLE IF EXISTS `meizi`;
CREATE TABLE `meizi` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键；自增长ID',
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `url` varchar(255) DEFAULT NULL UNIQUE KEY COMMENT '图片链接',
  `update_time` varchar(255) DEFAULT NULL COMMENT '更新时间',
  `click_amount` varchar(255) DEFAULT NULL COMMENT '点击数量',
  `tags` varchar(255) DEFAULT NULL  COMMENT '标签',
  `content` text COMMENT '写真集简介',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 CHARSET=utf8 COMMENT='美女写真';
