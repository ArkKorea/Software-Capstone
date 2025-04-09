use test;

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
