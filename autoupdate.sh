#!/bin/bash
if [ -z "$1" ] ; then
        echo "使用方法：$0 包名（不带.spec）"
        exit 1
fi
# 变量设置
# 是否记录调试信息
DEBUG=0
# 是否记录编译日志
LOG=1
# 是否给 release 加 1
# 一般仅在重编译时使用
BUMP=0
# rpmbuild 的 _topdir 变量
TOPDIR=$(rpm --eval "%{_topdir}")
# 打包用户名
PACKAGER="Liu Di"
PACKEMAIL="<liudidi@gmail.com>"
# RPM 下的目录名
ARCH=$(uname -m)
if [ "$ARCH" = "mips64" ];then
ARCH=mips64el
fi
INSTALLRPMS=0
# 使用的下载命令
DOWNCOMMAND=wget
# 对应下载命令的命令行参数，其后应该跟随下载目录
case "$DOWNCOMMAND" in
	wget )
	DOWN="wget --no-check-certificate -c -P"
	;;
	aria2 )
	DOWN="aria2c --check-certificate=false -c -x 5 -s 5 -d"
	;;
	lftp )
	DOWN="lftp -c pget -O"
	;;
esac
# 设置日志文件
if [ $LOG = "1" ];then
	DIR=`ls -d SPECS.*/$1`
        LOGFILE=$DIR/build.log
else    
        LOGFILE=/dev/null
fi

if ! [ -z "$$RPM_PACKAGER" ];then
	export RPM_PACKAGER="Liu Di <liudidi@gmail.com>"
fi

# 检查系统中是否有打包所需的命令。
function checkcommand()
{
	if ! [ -f "/bin/yum" ] || [ -f "/bin/sudo" ]; then
		commandlist="rpm rpmbuild rpmspec spectool $DOWNCOMMAND"
		for command in $commandlist ; do
			if ! ( which $command > /dev/null 2>&1 ) ; then
				echo "系统中没有 $command 命令，尝试自动安装"
				if ! ( sudo yum install `yum provides \*/bin/$command | cut -d " " -f 1 ` ) ; then
					echo "不能安装 $command 命令所属的包，请手工安装"
					exit 1
				fi
			fi
		done
	else
		echo "没有 yum 命令，系统中必须有 yum 才可以继续执行脚本"
		exit 1
	fi
}

function debug_echo ()
{
	if [ $DEBUG = "1" ];then
		echo $1
	fi
}
function debug_runsh ()
{
	if [ $DEBUG = "1" ];then
		sh $1
	else
		sh $1 >> "$LOGFILE" 2>&1
	fi
}
function debug_run ()
{
	if [ $DEBUG = "1" ];then
		"$@"
	else	
		"$@" >> "$LOGFILE" 2>&1
	fi
}

#主程序
#进入脚本所在的目录
pushd $(dirname $0)
#判断对应的目录是否存在
DIR=`ls -d SPECS.*/$1`
COUNT=`ls -d SPECS.*/$1 | wc -l`
if [ $COUNT -ne 1 ]; then
	echo "$1 不在源码树中，请检查输入是否正确"
	exit 1
fi
#检查需要的命令
checkcommand || exit 1
#检测 spec
SPECNAME=$(ls $DIR/*.spec)
#首先判断是否使用版本控制系统的源码，如果是，则将日期更新到当前日期，目前支持git/cvs/svn/hg。
if `cat $SPECNAME | grep -q -E "%define git 1|%define svn 1|%define cvs 1|%define hg 1"` ; then
	TODAY=$(date +%Y%m%d)
	sed -i "s/%define vcsdate .*/%define vcsdate $TODAY/g" $SPECNAME
fi
#如果不是，则检测新版本
if [ -f $DIR/getnewver ]; then
	NEWVER=`$DIR/getnewver`
	echo $NEWVER
else
	echo "没有取得 $1 新版本号的脚本，请自行添加。"
	exit 1
fi
#取得当前 spec 中的版本
SPECVER=`rpmspec -q --qf "%{version}\n" $SPECNAME |head -n 1`
echo $SPECVER
#对比更新
if ! [ $NEWVER = $SPECVER ]; then
	#执行 spec 更新脚本
	echo "$1 版本有更新，更新 spec 文件。"
	if [ -f $DIR/updatespec ]; then
		./$DIR/updatespec $NEWVER
		rpmdev-bumpspec -n -c "更新到 $NEWVER" $SPECNAME
	else
		echo "不存在 spec 更新脚本，请自行添加。"
		exit 1
	fi
fi
popd
