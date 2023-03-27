del database.db
python main.py --debug  --init
python -m nuitka main.py ^
--output-dir=dist ^
--onefile ^
--standalone ^
-o panbase.exe ^
--quiet ^
--remove-output ^
--show-progress ^
--include-data-file=database.db=database.db ^
--include-data-dir=admin-ui/dist=admin-ui/dist ^
--onefile-tempdir-spec="%TEMP%\panbase\0.1.0"