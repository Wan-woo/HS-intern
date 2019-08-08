create table  objectFunctionQuota
(
       id                INTEGER not null 	/*对应关系编号*/,
       objectName        VARCHAR(4000) 	/*对象名称 表、存储过程和视图的名称*/,
       objectType        INTEGER 	/*对象类型 表、存储过程和视图的名称*/,
       functionQuotaName VARCHAR(4000) 	/*功能或指标名称 功能或指标名称*/,
       functionQuotaType INTEGER 	/*功能或指标类型 功能或指标类型*/
);
