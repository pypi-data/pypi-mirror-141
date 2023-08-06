set PATH=C:\Program Files\Python39;C:\Program Files\Python39\Scripts;C:\Program Files\CMake\bin;%PATH%
virtualenv.exe -p "C:\Program Files\Python39\python.exe" .
call .\Scripts\activate
python setup.py bdist_wheel --dist-dir dist3
