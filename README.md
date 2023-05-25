# resMap
Step by step
1. Create virtual envoiment
2. install following modules:
<p>
  blinker==1.6.2<br>
  bson==0.5.10<br>
  certifi==2023.5.7<br>
  charset-normalizer==3.1.0<br>
  click==8.1.3<br>
  et-xmlfile==1.1.0<br>
  Flask==2.3.2<br>
  Flask-Cors==3.0.10<br>
  Flask-JWT-Extended==4.4.4<br>
  idna==3.4<br>
  itsdangerous==2.1.2<br>
  Jinja2==3.1.2<br>
  jsondiff==2.0.0<br>
  MarkupSafe==2.1.2<br>
  numpy==1.24.3<br>
  openpyxl==3.1.2<br>
  pandas==2.0.1<br>
  PyJWT==2.7.0<br>
  python-dateutil==2.8.2<br>
  pytz==2023.3<br>
  requests==2.30.0<br>
  six==1.16.0<br>
  tzdata==2023.3<br>
  urllib3==2.0.2<br>
  Werkzeug==2.3.4<br>
</p>
3. read following datas for explaining project structures:<br>
Main structure<br>
obects\defs.py -contains helper methods, errors.py -contains all error(you can set your all errors in db) <br>
services\services.py - all apies here<br>
setting\config.py db.py - all configured tools<br>
static\ - all static style and js files<br>
templates\ - all HTML files<br>
app.py - all registered apis here<br>
db.xlsx - in this case the xlsx file is using as data abse<br>
4. about code:<br>
There are 2 important methods in the helper file defs.py. They are: big_datas & jinja_data_maker. 
The big_datas takes all data from xlsx file and converts all data to dict data type via pandas. Then
it returns the dict data. The jinja_data_maker method converts all datas for jinja2 by inserted parameters.
<br>
<br>
<br>
<br>
<br>
<p>
Note: the using manuals of methods are in the appropriate methods.
</p>


