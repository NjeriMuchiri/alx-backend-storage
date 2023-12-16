-- the 'users' table already exists

-- Creating a trigger to reset valid_email when the email is updated
DELIMITER //
CREATE TRIGGER update_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
DELIMITER ;
