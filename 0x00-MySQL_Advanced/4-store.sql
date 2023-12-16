-- the 'items' and 'orders' tables already exist

-- Creating a trigger to update the quantity after inserting a new order
DELIMITER //
CREATE TRIGGER update_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;
