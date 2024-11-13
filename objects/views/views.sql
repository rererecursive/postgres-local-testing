CREATE VIEW etl.translate AS
SELECT REPLACE(message, 'bubble', 'wave') as message
FROM etl.entries;
