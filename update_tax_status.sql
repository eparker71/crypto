ALTER TABLE data 
ADD COLUMN tax_status text;

UPDATE Data 
SET [tax_status] = 'SHORT'
where Timestamp > DATE('now', '-1 year');

UPDATE Data 
SET [tax_status] = 'LONG'
where Timestamp < DATE('now', '-1 year');

