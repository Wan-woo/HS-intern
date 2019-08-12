/*
 Navicat Premium Data Transfer

 Source Server         : HsSqlite
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 12/08/2019 11:37:07
 修改数据库 增加新的数据记录之后的备份
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for backupFieldKey
-- ----------------------------
DROP TABLE IF EXISTS "backupFieldKey";
CREATE TABLE "backupFieldKey" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "objectName" VARCHAR(4000),
  "fieldChosed" varchar(4000),
  "keyChosed" VARCHAR(4000),
  "isSystemDefine" integer,
  "modifier" VARCHAR(4000),
  "modificationTime" integer
);

-- ----------------------------
-- Records of "backupFieldKey"
-- ----------------------------
INSERT INTO "backupFieldKey" VALUES (1, '表1', '字段1', '字段1', 1, '', 1565575029);
INSERT INTO "backupFieldKey" VALUES (2, '表1', '字段2', '字段1', 1, '', 1565577029);
INSERT INTO "backupFieldKey" VALUES (3, '表1', '字段3', '字段1', 1, NULL, NULL);
INSERT INTO "backupFieldKey" VALUES (4, '表2', '字段1', '字段1', 0, 'zwd', 1565575029);
INSERT INTO "backupFieldKey" VALUES (5, '表2', '字段2', '字段1', 0, 'zwy', 1565577029);

-- ----------------------------
-- Table structure for backupInformation
-- ----------------------------
DROP TABLE IF EXISTS "backupInformation";
CREATE TABLE "backupInformation" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "backupVersion" integer,
  "backupTime" integer,
  "beginTime" integer,
  "endTime" integer,
  "hasContrast" integer
);

-- ----------------------------
-- Records of "backupInformation"
-- ----------------------------
INSERT INTO "backupInformation" VALUES (5, 1, 190808, 190704, 190801, 1);
INSERT INTO "backupInformation" VALUES (8, 2, 190808, 190704, 190801, 0);
INSERT INTO "backupInformation" VALUES (9, 3, 190808, 190704, 190801, 0);
INSERT INTO "backupInformation" VALUES (10, 4, 190808, 190704, 190801, 0);

-- ----------------------------
-- Table structure for backupObjectNameList
-- ----------------------------
DROP TABLE IF EXISTS "backupObjectNameList";
CREATE TABLE "backupObjectNameList" (
  "Id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "backupVersion" INTEGER,
  "objectName" VARCHAR(4000),
  "backupObjectName" VARCHAR(4000),
  "ObjectType" INTEGER
);

-- ----------------------------
-- Records of "backupObjectNameList"
-- ----------------------------
INSERT INTO "backupObjectNameList" VALUES (1, '', '表1', '', 1);
INSERT INTO "backupObjectNameList" VALUES (2, NULL, '表2', '', 1);
INSERT INTO "backupObjectNameList" VALUES (3, NULL, '表3', '', 1);
INSERT INTO "backupObjectNameList" VALUES (4, NULL, '存储过程1', '', 2);
INSERT INTO "backupObjectNameList" VALUES (5, 1, '表1', 'backup1', 1);
INSERT INTO "backupObjectNameList" VALUES (6, 3, '表1', 'backup2', 1);
INSERT INTO "backupObjectNameList" VALUES (7, 1, '表2', 'backup3', 1);

-- ----------------------------
-- Table structure for contrastResults
-- ----------------------------
DROP TABLE IF EXISTS "contrastResults";
CREATE TABLE "contrastResults" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "backupObjectName" VARCHAR(4000),
  "differenceType" INTEGER,
  "primaryKeyId" VARCHAR(4000),
  "differenceField" VARCHAR(4000)
);

-- ----------------------------
-- Table structure for functionQuotaList
-- ----------------------------
DROP TABLE IF EXISTS "functionQuotaList";
CREATE TABLE "functionQuotaList" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "functionQuotaName" VARCHAR(4000),
  "functionQuotaType" INTEGER
);

-- ----------------------------
-- Records of "functionQuotaList"
-- ----------------------------
INSERT INTO "functionQuotaList" VALUES (1, '功能1', 1);
INSERT INTO "functionQuotaList" VALUES (2, '功能2', 1);
INSERT INTO "functionQuotaList" VALUES (3, '指标1', 2);

-- ----------------------------
-- Table structure for moduleObject
-- ----------------------------
DROP TABLE IF EXISTS "moduleObject";
CREATE TABLE "moduleObject" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "moudleName" VARCHAR(4000),
  "objectName" VARCHAR(4000),
  "objectType" INTEGER,
  "isSystemDefineMoudle" integer
);

-- ----------------------------
-- Records of "moduleObject"
-- ----------------------------
INSERT INTO "moduleObject" VALUES (1, '模块1', '表1', 1, 1);
INSERT INTO "moduleObject" VALUES (2, '模块1', '表2', 1, 1);
INSERT INTO "moduleObject" VALUES (3, '模块2', '表2', 1, 0);

-- ----------------------------
-- Table structure for moudleList
-- ----------------------------
DROP TABLE IF EXISTS "moudleList";
CREATE TABLE "moudleList" (
  "moudleId" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "moudleName" VARCHAR(4000),
  "isSystemDefineModule" integer
);

-- ----------------------------
-- Records of "moudleList"
-- ----------------------------
INSERT INTO "moudleList" VALUES (1, '模块1', 1);
INSERT INTO "moudleList" VALUES (2, '模块2', 0);

-- ----------------------------
-- Table structure for objectFunctionQuota
-- ----------------------------
DROP TABLE IF EXISTS "objectFunctionQuota";
CREATE TABLE "objectFunctionQuota" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "objectName" VARCHAR(4000),
  "objectType" INTEGER,
  "functionQuotaName" VARCHAR(4000),
  "functionQuotaType" INTEGER,
  "isSystemDefineMoudle" integer NOT NULL
);

-- ----------------------------
-- Records of "objectFunctionQuota"
-- ----------------------------
INSERT INTO "objectFunctionQuota" VALUES (1, '表1', 1, '功能1', 1, 1);
INSERT INTO "objectFunctionQuota" VALUES (2, '表2', 1, '功能1', 1, 1);
INSERT INTO "objectFunctionQuota" VALUES (3, '表2', 1, '功能2', 1, 0);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Records of "sqlite_sequence"
-- ----------------------------
INSERT INTO "sqlite_sequence" VALUES ('moudleList', 2);
INSERT INTO "sqlite_sequence" VALUES ('moduleObject', 3);
INSERT INTO "sqlite_sequence" VALUES ('functionQuotaList', 3);
INSERT INTO "sqlite_sequence" VALUES ('contrastResults', 0);
INSERT INTO "sqlite_sequence" VALUES ('backupInformation', 11);
INSERT INTO "sqlite_sequence" VALUES ('backupFieldKey', 5);
INSERT INTO "sqlite_sequence" VALUES ('backupObjectNameList', 7);
INSERT INTO "sqlite_sequence" VALUES ('objectFunctionQuota', 3);

-- ----------------------------
-- Table structure for testzwd
-- ----------------------------
DROP TABLE IF EXISTS "testzwd";
CREATE TABLE "testzwd" (
  "id" INTEGER NOT NULL,
  "name" TEXT,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of "testzwd"
-- ----------------------------
INSERT INTO "testzwd" VALUES (1, NULL);

-- ----------------------------
-- Auto increment value for backupFieldKey
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 5 WHERE name = 'backupFieldKey';

-- ----------------------------
-- Auto increment value for backupInformation
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 11 WHERE name = 'backupInformation';

-- ----------------------------
-- Auto increment value for backupObjectNameList
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 7 WHERE name = 'backupObjectNameList';

-- ----------------------------
-- Indexes structure for table backupObjectNameList
-- ----------------------------
CREATE INDEX "IDU_backupOist_backupVionD6AE"
ON "backupObjectNameList" (
  "backupVersion" ASC
);

-- ----------------------------
-- Auto increment value for contrastResults
-- ----------------------------

-- ----------------------------
-- Auto increment value for functionQuotaList
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'functionQuotaList';

-- ----------------------------
-- Indexes structure for table functionQuotaList
-- ----------------------------
CREATE UNIQUE INDEX "IDU_functioist_functioameC8F1"
ON "functionQuotaList" (
  "functionQuotaName" ASC
);

-- ----------------------------
-- Auto increment value for moduleObject
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'moduleObject';

-- ----------------------------
-- Auto increment value for moudleList
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 2 WHERE name = 'moudleList';

-- ----------------------------
-- Auto increment value for objectFunctionQuota
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 3 WHERE name = 'objectFunctionQuota';

PRAGMA foreign_keys = true;
