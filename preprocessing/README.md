
# Overview
This folder contains all the preprocessing codes for the project.


## 1. preprocessingbookinform.py
### Features
+ Publication Year Cleaning:
Handles incomplete or malformed publication years:
Example: 19-- -> 1975, 198- -> 1985, 199- -> 1995.
Supports normalization of ranges (e.g., 2004-2007 -> 2004).
+ Author Name Normalization:
 저자 정보가 없을 경우, 해당 정보를 저자 미상으로 채운다.
+ Classification Code Cleaning:
1의 자리가 소거된 세 자리 수의 형태로 분류 코드를 정규화한다.
Example: Converts 115.133C1 to 110
+  Removes unnecessary columns

### Example input & output
### input
+ File format: .txt


"도서ID","등록일자","수서방법","분류코드","ISBN","서명","저자","출판사","출판년도","소장위치"


SS_228194,"2013-10-08",학과신청,"298","9782020258113", BookName,"author",publisher,"2009","4층인문"
### output
+ File format: .csv

  
도서ID	등록일자	수서방법	분류코드	서명	저자	출판년도	소장위치


SS_228194	2013	학과신청	290	BookName	author	2009	4층인문
