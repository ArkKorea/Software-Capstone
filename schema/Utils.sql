use test;

/*
-- 인당 기록 최근 30개 유지 프로시저

DELIMETER //

CREATE PROCEDURE manage_view_log(IN p_user_id INT)
BEGIN
    DECLARE row_count INT;

    SELECT COUNT(*) INTO row_count
    FROM view_log
    WHERE user_id = p_user_id;

    WHILE row_count > 30 DO
        DELETE v FROM view_log v
        JOIN (
            SELECT id FROM view_log
            WHERE user_id = p_user_id
            ORDER BY viewed_at ASC
            LIMIT 1
        ) AS sub ON v.id = sub.id;

        SET row_count = row_count -1;
    END WHILE;
END //

DELIMETER ;

-- 위 프로시저 실행을 위한 트리거 작성
DELIMETER //

CREATE TRIGGER after_insert_view_log
AFTER INSERT ON view_log
FOR EACH ROW
BEGIN
    CALL manage_view_log(NEW.user_id);
END //

DELIMETER ;
*/

DELIMITER //

CREATE TRIGGER after_insert_view_log
AFTER INSERT ON view_log
FOR EACH ROW
BEGIN
    -- 최근 30개만 유지하기 위해, 가장 오래된 기록 삭제
    DELETE FROM view_log
    WHERE user_id = NEW.user_id
    AND id NOT IN (
        SELECT id FROM (
            SELECT id FROM view_log
            WHERE user_id = NEW.user_id
            ORDER BY viewed_at DESC
            LIMIT 30
        ) AS temp
    );
END //

DELIMITER ;
