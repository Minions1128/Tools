# Git 简单命令

## 配置Git

http://www.runoob.com/w3cnote/git-guide.html

## 添加文件

touch test.txt
git add test.txt
git commit -m "add a file"
git push

## 删除文件

git rm test.txt
git commit -m "remote a file"
git push

##删除本地所有未提交的更改

1. git clean -df
2. git reset --hard
