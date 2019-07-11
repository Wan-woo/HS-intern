/**
drop   table Student;
drop   table course;
drop   table score;
drop   table teacher;
**/
--表（一）Student (学生表)
CREATE table Student
(	sno char(3) primary key,
sname char(8),
Ssex char(2),
--sbirthday DATE,
class char(5)
);
--表（二）Course（课程表）
CREATE table course
(	cno char(5) primary key,
cname varchar(10),
tno char(3)
);
--表（三）Score(成绩表)
CREATE table score
(	sno char(3),
cno char(5),
degree decimal(4,1)
);
--表（四）Teacher(教师表)
CREATE table teacher
(	tno char(3) primary key,
tname char(4),
tsex char(2),
--tbirthday DATE,
prof char(6),
depary varchar(10)
);


INSERT INTO Student VALUES
(108,'曾华','男',95033);
INSERT INTO Student VALUES
(105,'匡明','男',95031);
INSERT INTO Student VALUES
(107,'王丽','女',95033);
INSERT INTO Student VALUES
(101,'李军','男',95033);
INSERT INTO Student VALUES
(109,'王芳','女',95031);
INSERT INTO Student VALUES
(103,'陆君','男',95031);

INSERT INTO Course VALUES
('3-105','计算机导论',825);
INSERT INTO Course VALUES
('3-245','操作系统',804);
INSERT INTO Course VALUES
('6-166','数字电路',856);
INSERT INTO Course VALUES
('9-888','高等数学',831);

INSERT INTO Score VALUES
(103,'3-245',86);
INSERT INTO Score VALUES
(105,'3-245',75);
INSERT INTO Score VALUES
(109,'3-245',68);
INSERT INTO Score VALUES
(103,'3-105',92);
INSERT INTO Score VALUES
(105,'3-105',88);
INSERT INTO Score VALUES
(109,'3-105',76);
INSERT INTO Score VALUES
(101,'3-105',64);
INSERT INTO Score VALUES
(107,'3-105',91);
INSERT INTO Score VALUES
(108,'3-105',78);
INSERT INTO Score VALUES
(101,'6-166',85);
INSERT INTO Score VALUES
(107,'6-166',79);
INSERT INTO Score VALUES
(108,'6-166',81);

INSERT INTO Teacher VALUES
(804,'李诚','男','副教授','计算机系');
INSERT INTO Teacher VALUES
(856,'张旭','男','讲师','电子工程系');
INSERT INTO Teacher VALUES
(825,'王萍','女','助教','计算机系');
INSERT INTO Teacher VALUES
(831,'刘冰','女','助教','电子工程系');
commit;