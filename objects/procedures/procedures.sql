CREATE OR REPLACE PROCEDURE etl.sp_add_entry(p_message VARCHAR, p_name VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO etl.entries (message, username)
    VALUES (p_message, p_name);
END;
$$;
