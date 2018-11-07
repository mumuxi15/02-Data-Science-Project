!/usr/bin/python
sqlite> .mode csv
sqlite> .import rejected_07_17.csv tmp
sqlite> .schema tmp
sqlite> 

CREATE TABLE rej(
id integer primary key,
loan_amnt FLOAT,application_d VARCHAR(10),title VARCHAR(20),fico FLOAT,dti FLOAT,
addr_state VARCHAR(10),emp_length VARCHAR(20));
	
	
INSERT INTO rej(loan_amnt,fico,dti,application_d,title,addr_state,emp_length)
SELECT CAST("Amount Requested" AS FLOAT),CAST("Risk_Score" AS FLOAT),CAST("Debt-To-Income Ratio" AS FLOAT),
"Application Date","Loan Title","State","Employment Length"
FROM tmp;

# create 
.import accepted_07_17.csv acc
