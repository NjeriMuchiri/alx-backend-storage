DELIMITER //

-- Creation of the ComputeAverageScoreForUser stored procedure
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Calculation the total score for the user
    SELECT SUM(score), COUNT(DISTINCT project_id) INTO total_score, total_projects
    FROM corrections
    WHERE user_id = p_user_id;

    -- Update of the average score for the user
    UPDATE users
    SET average_score = IFNULL(total_score / total_projects, 0)
    WHERE id = p_user_id;
END //

DELIMITER ;
