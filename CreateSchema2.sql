DROP DATABASE IF EXISTS truonghoc2; 
CREATE DATABASE truonghoc2;
USE truonghoc2;
SET NAMES utf8mb4;

DROP TABLE IF EXISTS truong;
CREATE TABLE truong(
	matr VARCHAR(20) NOT NULL,
    tentr VARCHAR(100) NOT NULL,
    dchitr VARCHAR(255) NOT NULL,
    PRIMARY KEY(matr) /*clustered index*/
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS hs;
CREATE TABLE hs(
    mahs CHAR(12) NOT NULL,
	ho VARCHAR(10) NOT NULL,
    ten VARCHAR(40) NOT NULL,
    cccd CHAR(12) DEFAULT NULL,
    ntns DATE NOT NULL,
    dchi_hs VARCHAR(255) NOT NULL,
    PRIMARY KEY(mahs) /*clustered index*/
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS hoc;
CREATE TABLE hoc(
	matr VARCHAR(20) NOT NULL,
    mahs CHAR(12) NOT NULL,
    namhoc CHAR(11) NOT NULL,
    diemtb DECIMAL(4, 2) NOT NULL,
    xeploai VARCHAR(10) DEFAULT NULL,
    kqua VARCHAR(15) DEFAULT NULL,
    PRIMARY KEY(matr, mahs, namhoc),
    CONSTRAINT FOREIGN KEY(matr) REFERENCES truong(matr),
    CONSTRAINT FOREIGN KEY(mahs) REFERENCES hs(mahs)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX index_ten ON truong(tentr);
CREATE INDEX index_xeploai ON hoc(xeploai);
CREATE INDEX index_namhoc ON hoc(namhoc);

DROP TRIGGER IF EXISTS update_xeploai_kqua;
DELIMITER //

CREATE TRIGGER update_xeploai_kqua BEFORE INSERT ON hoc
FOR EACH ROW
BEGIN
    DECLARE xeploai_var VARCHAR(10);
    DECLARE kqua_var VARCHAR(15);
    
    IF NEW.diemtb >= 9.0 THEN
        SET xeploai_var = 'Xuất sắc';
        SET kqua_var = 'Hoàn thành';
    ELSEIF NEW.diemtb >= 8.0 THEN
        SET xeploai_var = 'Giỏi';
        SET kqua_var = 'Hoàn thành';
    ELSEIF NEW.diemtb >= 6.5 THEN
        SET xeploai_var = 'Khá';
        SET kqua_var = 'Hoàn thành';
    ELSEIF NEW.diemtb >= 5.0 THEN
        SET xeploai_var = 'Trung bình';
        SET kqua_var = 'Hoàn thành';
    ELSE
        SET xeploai_var = 'Yếu';
        SET kqua_var = 'Chưa hoàn thành';
    END IF;
    
    SET NEW.xeploai = xeploai_var;
    SET NEW.kqua = kqua_var;
END//

DELIMITER ;

