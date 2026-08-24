-- 建立 Schema
CREATE SCHEMA IF NOT EXISTS "LineBot";

-- 1. 建立 MemberProfile 表
CREATE TABLE IF NOT EXISTS "LineBot"."MemberProfile" (
    "Id" SERIAL PRIMARY KEY,
    "UserId" VARCHAR(40) NOT NULL,
    "UserName" VARCHAR(40) NOT NULL,
    "UserContent" VARCHAR(20) NOT NULL,
    "Role" VARCHAR(20) NOT NULL,
    "isAttending" BOOLEAN DEFAULT NULL,
    "Intent" VARCHAR(32) DEFAULT NULL,
    "PlayedDate" VARCHAR(5) DEFAULT NULL,
    "Status" VARCHAR(10) DEFAULT NULL,
    "LastRepliedAt" TIMESTAMP DEFAULT NULL,
    "TimeStamp" TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 建立唯一索引 (對應 unique=True)
CREATE UNIQUE INDEX IF NOT EXISTS "ix_LineBot_MemberProfile_UserId" ON "LineBot"."MemberProfile" ("UserId");

-- 2. 建立 AttendanceRecord 表
CREATE TABLE IF NOT EXISTS "LineBot"."AttendanceRecord" (
    "Id" SERIAL PRIMARY KEY,
    "UserId" VARCHAR(40) NOT NULL,
    "UserName" VARCHAR(40) NOT NULL,
    "isAttending" BOOLEAN DEFAULT FALSE,
    "PlayedDate" VARCHAR NOT NULL,
    "TimeStamp" TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 建立索引 (對應 index=True)
CREATE INDEX IF NOT EXISTS "ix_LineBot_AttendanceRecord_UserId" ON "LineBot"."AttendanceRecord" ("UserId");