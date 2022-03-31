rem ローカル環境DB初期投入バッチ

rem ローカルDB(MySQL)に接続し、全テーブル削除
mysql -u root --password=t0tp50gx < init_db.sql

rem 不要なフォルダやファイル(0001_initial.pyなどを削除)
rd /Q /S numeron\migrations\__pycache__
rd /Q /S numeron\__pycache__
del numeron\migrations\0*

rem DB再構築及び初期データ投入
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata numeron\json\user.json
python manage.py loaddata numeron\json\rank.json