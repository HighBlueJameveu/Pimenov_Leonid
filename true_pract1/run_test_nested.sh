# Создаем VFS с глубокой вложенностью
cat <<EOF > vfs_nested.csv
type,path,content
dir,/,
dir,/level1,
dir,/level1/level2,
dir,/level1/level2/level3,
file,/level1/level2/level3/deep_file.txt,VGhpcyBpcyBhIGRlZXAgZmlsZSE=
EOF

python3 main.py --vfs vfs_nested.csv --script script_test2.txt