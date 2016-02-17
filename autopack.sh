#!/bin/bash -x
# 返回值 
# 1 = 无法准备源码，即不能下载源码或其它问题
# 2 = spec 格式错误
# 3 = 打包过程出错
# 4 = 安装过程出错
# 5 = 使用方法错误
# 6 = 需要的命令没有安装
# 7 = 没有 yum
# 8 = spec名 或 目录名有问题
# 9 = 不支持的架构
#10 = 没有中文翻译
#11 = 没有清理语句
#12 = 自动更新出错
#13 = 跳过编译
if [ -z "$1" ] ; then
        echo "使用方法：$0 包名（不带.spec）"
        exit 5
fi
set -o pipefail
#进入脚本所在的目录
pushd $(dirname $0)
# 变量设置
# 是否记录调试信息
DEBUG=1
# 是否记录编译日志
LOG=1
# 是否给 release 加 1
# 一般仅在重编译时使用
AUTOBUMP=0
# rpmbuild 的 _topdir 变量
TOPDIR=$(rpm --eval "%{_topdir}")
PACKAGER="Magic Group"
PACKEMAIL="<magicgroup@linuxfans.org>"
# rpmbuild 中是否执行 check 段
CHECK=0
NODEPS=0
# RPM 下的目录名
ARCH=$(uname -m)
if [ "$ARCH" = "mips64" ];then
	ARCH=mips64el
fi
#是否安装编译好的rpm
INSTALLRPMS=0
FORCEINSTALLRPMS=0
#是否自动更新软件版本
AUTOUPDATE=1
# 使用用户的配置
if [ -f ~/.magicspec ]; then
	. ~/.magicspec
fi
# 使用软件包本身的配置，也可以放一些需要前置执行的脚本。
if [ -f ./packspec ]; then
	. ./packspec
fi
# rpmbuild 中是否执行 check 段
if [ "$CHECK" = 1 ] ;then
        NOCHECK=""
else
        NOCHECK="--nocheck"
fi
# rpmbuild 是否忽略依赖关系
if [ "$NODEPS" = 1 ] ; then
	BUILDDEPS="--nodeps"
else
	BUILDDEPS=""
fi
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
        export RPM_PACKAGER="$PACKAGER $PACKEMAIL"
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
					exit 6
				fi
			fi
		done
	else
		echo "没有 yum 命令，系统中必须有 yum 才可以继续执行脚本"
		exit 7
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
		sh $1 2>&1 | tee "$LOGFILE"
	fi
}
function debug_run ()
{
	if [ $DEBUG = "1" ];then
		"$@"
	else	
		"$@" 2>&1  | tee -a "$LOGFILE"
	fi
}

#检查spec文件 
function checkspec()
{
	DIR=`ls -d SPECS.*/$1`
	#判断一些环境变量，首先是是否必须有中文翻译，默认非必须
	if [ -z "$HAVECNUTF8" ]; then
        	HAVECNUTF8=0
	fi
	#其次是否必须有清理语句，用来清理非中文语言等。默认非必须，正式制作的时候建议必须。
	if [ -z "$HAVECLEAN" ]; then
		HAVECLEAN=0
	fi
	#以上的变量均可在这个文件中重新设置。
	if [ -f ~/.magicspecrc ];then
        	. ~/.magicspecrc
	fi
	#判断目录下是否有 .spec 文件，并取得其文件名
	SPECCOUNT=`ls $DIR/*.spec 2>/dev/null | wc -l`
	if [ $SPECCOUNT -gt 1 ];then
        	echo "当前目录的 .spec 文件过多，只有一个 spec 文件的情况下，脚本才能正确执行"
        	touch specfail && exit 8
	fi
	if [ $SPECCOUNT = "0" ];then
        	echo "当前目录中没有 .spec 文件，脚本退出！"
        	touch specfail && exit 8
	fi
	#判断 spec 文件名是否和目录名一致。
	SPECNAME=$(ls $DIR/*.spec)
	NAME=$(basename $SPECNAME)
	if ! [ $NAME = "$1.spec" ] ; then
	        echo "spec 文件名和所在目录的名字不一致，请检查原因。"
        	touch specfail && exit 8
	fi
	debug_echo "当前的 spec 文件名是 $SPECNAME"
	#判断是否跳过 spec 解析判断
	if ! [ -f $DIR/ignorespeccheck ]; then
		#判断 spec 文件是否有问题
		if !  (debug_run rpmspec -P $SPECNAME );then
  		        echo "spec 文件格式有错误，请检查，脚本退出！" 
        		touch specfail && exit 2
		fi
	fi
	if ! (rpmspec -P $SPECNAME | grep "Summary(zh_CN.UTF-8)" > /dev/null); then
        	if [ $HAVECNUTF8 = "1" ];then
                	echo "spec 中没有中文简介，请添加"
                	touch specfail && exit 10
        	else
                	debug_echo "spec 中没有中文简介"
        	fi
	fi	
	if ! (rpmspec -P $SPECNAME | grep "magic_rpm_clean.sh" > /dev/null); then
        	if [ $HAVECLEAN = "1" ];then
                	echo "spec 中没有清理语句，请添加"
                	#这里要做自动添加的尝试，但有些难
                	touch specfail && exit 11
        	else
                	debug_echo "spec 中没有清理语句"
        	fi
	fi
}

#准备源码
function preparefiles()
{
	# 建立打包用目录。
	DIR=`ls -d SPECS.*/$1`
	echo "建立打包使用的目录"
	for dir in SOURCES RPMS SRPMS BUILD BUILDROOT;do
		if ! [ -d $TOPDIR/$dir ]; then
			mkdir -p $TOPDIR/$dir
		fi
	done
	cp -f $DIR/* $TOPDIR/SOURCES
}

#下载源码
function downsources()
{
	#下载 spec 中指定的源码，注意 spec 中必须事先写好。
	#判断 spec 中的指定的源码地址是否有 http 或 ftp。
	#所在目录
	DIR=`ls -d SPECS.*/$1`
	#spec文件全名
	SPECNAME=$(ls $DIR/*.spec)
	#spec中的源文件列表
	SOURCELIST=`spectool -S $SPECNAME |cut -d " " -f2`
	if [ x"$SOURCELIST" == x"" ] ;then
		echo "请手工下载源码"
		touch $DIR/downfail
		exit 1
	else
	for source in  $SOURCELIST ;do
		#如果以 http 或 ftp 开头，则取出最后的文件名。
		if [[ $source =~ ^http ]] || [[ $source =~ ^ftp ]] ; then
			sourcefile=`echo ${source##*/}`
			sourceurl=$source
		else
		#否则就以 $source 为文件名
			sourcefile=$source
		fi
		# 首先判断在 SOURCES 目录中是否存在
		if ! [ -f $TOPDIR/SOURCES/$sourcefile ]; then
			# 如果不存在，则先从 apt 服务器上下载
			echo "正在从 magic 的服务器上下载源码 $sourcefile"
			SDIR=SOURCES.`dirname $DIR |cut -f2 -d"."`
			if ! ( debug_run $DOWN $TOPDIR/SOURCES "http://apt.linuxfans.org/magic/3.0/sources/$SDIR/$1/$sourcefile" ) ; then
				#如果无法下载，则有官方下载地址的就尝试从官方下载
				echo "Magic 的服务器上没有 $sourcefile，尝试从 spec 中提供的地址下载"
				if ! [ x"$sourceurl" = x"" ]; then
					if ! ( debug_run $DOWN $TOPDIR/SOURCES $sourceurl ) ; then
						echo "官方地址无法下载，退出。"
						touch $DIR/downfail
						exit 1
					fi
				else
					echo "找不到源码文件，退出。"
					touch $DIR/downfail
                                        exit 1
				fi
			fi
		fi
	done
	fi
}

#下载补丁
function downpatches()
{
        #下载 spec 中指定的源码，注意 spec 中必须事先写好。
        #判断 spec 中的指定的源码地址是否有 http 或 ftp。
        #所在目录
        DIR=`ls -d SPECS.*/$1`
        #spec文件全名
        SPECNAME=$(ls $DIR/*.spec)
        #spec中的源文件列表
        PATCHESLIST=`spectool -P $SPECNAME |cut -d " " -f2`
        for rpatch in  $PATCHESLIST ;do
                #如果以 http 或 ftp 开头，则取出最后的文件名。
                if [[ $rpatch =~ ^http ]] || [[ $rpatch =~ ^ftp ]] ; then
                        patchfile=`echo ${rpatch##*/}`
                        patchurl=$rpatch
                else
                #否则就以 $source 为文件名
                        patchfile=$rpatch
                fi
                # 首先判断在 SOURCES 目录中是否存在
                if ! [ -f $TOPDIR/SOURCES/$patchfile ]; then
                        # 如果不存在，则先从 apt 服务器上下载
                        echo "正在从 magic 的服务器上下载补丁 $patchfile"
                        SDIR=SOURCES.`dirname $DIR |cut -f2 -d"."`
                        if ! ( debug_run $DOWN $TOPDIR/SOURCES "http://apt.linuxfans.org/magic/3.0/sources/$SDIR/$1/$patchfile" ) ; then
                                #如果无法下载，则有官方下载地址的就尝试从官方下载
                                if ! [ x"$patchurl" = x"" ]; then
                                        if ! ( debug_run $DOWN $TOPDIR/SOURCES $patchurl ) ; then
                                                echo "官方地址无法下载，退出。"
                                                exit 1
                                        fi
                                else
                                        echo "找不到源码文件，退出。"
                                        exit 1
                                fi
                        fi
                fi
        done
}

#下载 git 等版本控制系统的源码，需要有 make_包名_git[svn/cvs/hg]_package.sh 脚本
function downvcssources()
{
        #所在目录
        DIR=`ls -d SPECS.*/$1`
        #spec文件全名
        SPECNAME=$(ls $DIR/*.spec)
	VCSDATE=$(cat $SPECNAME |grep "%define vcsdate"|cut -d " " -f3)
	TODAY=$(date +%Y%m%d)
	if ! [ x"$VCSDATE" = x"$TODAY" ]; then
		if [ $AUTOUPDATE = "1" ]; then
			sed -i 's/%define vcsdate.*/%define vcsdate '"$TODAY"'/g' $SPECNAME
			rpmdev-bumpspec -c "更新到 $TODAY 日期的仓库源码" $SPECNAME
			cp -f $SPECNAME $TOPDIR/SOURCES
			VCSDATE=$TODAY
		fi
		debug_run echo "从 $2 仓库中下载 $1 的源代码"
        	pushd $TOPDIR/SOURCES
			if ! [ -f make_$1_$2_package.sh ] ; then
				echo "没有下载源代码的脚本，退出。"
				exit 1
			fi
                	if ! ( sh make_$1_$2_package.sh $VCSDATE ) ; then
                        	echo "无法从 $1 版本控制系统下载 $2 的源代码！退出。"
                        	exit 1
                	fi
        	popd
		debug_run echo "源代码下载完成"
	else
		debug_run echo "无需更新"
	fi
}

#安装依赖关系函数		
function installbuildrequires()
{
	#判断编译依赖关系
	#所在目录
        DIR=`ls -d SPECS.*/$1`
        #spec文件全名
        SPECNAME=$(ls $DIR/*.spec)
	#这里还需要对版本进行处理
	for i in `rpmspec -q --buildrequires $SPECNAME |cut -d " " -f 1`;do
		#这个方式判断不是很准确，但目前没有更好的方式。
        	if ! (rpm -qi $i > /dev/null 2>&1);then
                echo "安装编译需要依赖包 $i"
                debug_run sudo yum install $i -y || :
        fi
	done
}

#打包函数
function build()
{
        #开始打包
        #所在目录
        DIR=`ls -d SPECS.*/$1`
        #spec文件全名
        SPECNAME=$(ls $DIR/*.spec)
	NAME=$(basename $SPECNAME)
        echo "正在打包 $DIR ...，可能需要一段时间"
        if ! (debug_run rpmbuild -ba --clean --rmsource --rmspec $BUILDDEPS $NOCHECK $TOPDIR/SOURCES/$NAME ) ; then
                echo "打包过程出错，请检查 build.log 文件" 
		touch $DIR/buildfail     
                exit 3
        fi
        echo "打包完成，清理目录"
	rm -f $DIR/*fail
	rm -f $DIR/hasupdate
}

#安装函数
function installrpms()
{
	echo "正在安装 $1 编译出的 rpm 包。"
	DIR=`ls -d SPECS.*/$1`
	SPECNAME=$(ls $DIR/*.spec)
	pushd $TOPDIR/RPMS/$ARCH
		mv ../noarch/*.rpm . > /dev/null 2>&1
		if ! [ -d debuginfo ]; then
			mkdir debuginfo
		fi
		mv *debuginfo*.rpm debuginfo
		if [ $FORCEINSTALLRPMS = "1" ]; then
			INSTALLCOMMAND="rpm -Uvh --nodeps --force"
		else
			INSTALLCOMMAND="yum localinstall -y"
		fi
		if ! ( debug_run sudo $INSTALLCOMMAND `rpmspec -q --rpms $SPECNAME` ) ; then
			echo "无法安装编译好的 rpm 包，可能存在依赖问题，请检查 build.log 文件。"
			exit 4
		fi
	popd
}

#自动更新版本函数
function autoupdate () 
{
        DIR=`ls -d SPECS.*/$1`
        SPECNAME=$(ls $DIR/*.spec)
        if [ -f $DIR/getnewver ]; then
                ./autoupdate.sh $1 || exit 12
                #spec 有更新，所以需要重新复制
		if [ -f $DIR/hasupdate ] ; then
 	               cp -f $SPECNAME $TOPDIR/SOURCES || exit 12
		fi
        fi
}

#release +1
function autobumpspec () 
{
        DIR=`ls -d SPECS.*/$1`
        SPECNAME=$(ls $DIR/*.spec)
	if [ -z "$2" ]; then
		rpmdev-bumpspec -c "为 Magic 3.0 重建" $SPECNAME
	else
		rpmdev-bumpspec -c "$2" $SPECNAME
	fi
	#spec 有更新，所以需要重新复制
        cp -f $SPECNAME $TOPDIR/SOURCES || exit 12
}
	
#主程序
#判断对应的目录是否存在
DIR=`ls -d SPECS.*/$1`
COUNT=`ls -d SPECS.*/$1 | wc -l`
SPECNAME=$(ls $DIR/*.spec)
if [ $COUNT -ne 1 ]; then
	echo "$1 不在源码树中，请检查输入是否正确"
	exit 1
fi
if [ -f $DIR/ignore ]; then
	echo "$1 已经过时，不再编译，直接退出"
	exit 13 
fi
if [ -f $DIR/ignorearch ]; then
	for IGNOREARCH in `cat $DIR/ignorearch`; do
		if [ x"$IGNOREARCH" = x"$ARCH" ]; then
			echo "$1 不能在本机架构 $ARCH 上打包，直接退出"
			exit 9
		fi
	done
fi
rm -f $LOGFILE
#检查需要的命令
checkcommand || exit 1
#检测 spec
preparefiles $1 || exit 1
checkspec $1 || exit 1
#更新 spec
if [ $AUTOBUMP = "1" ]; then
	if [ $AUTOUPDATE = "1" ]; then
		echo "自动更新 $1 版本"
		if [ -f $DIR/getnewver ] ; then
			autoupdate $1 || echo "$1 版本更新未成功，请检查网络环境和相关配置"
			if [ -f $DIR/buildfail ] || [ -f $DIR/downfail ] || [ -f $DIR/hasupdate ] ; then
				echo "暂不更新 release "			
			elif [ -f $DIR/buildfail ] || [ -f $DIR/downfail ] || [ -f $DIR/hasupdate ] ; then
                                echo "暂不更新 release "     
			else
				autobumpspec $1 $2
			fi
		elif [ -f $DIR/buildfail ] || [ -f $DIR/downfail ] || [ -f $DIR/hasupdate ] ; then
                        echo "暂不更新 release "
		else     
			autobumpspec $1 $2
		fi
	elif  [ -f $DIR/buildfail ] || [ -f $DIR/downfail ] || [ -f $DIR/hasupdate ] ; then
		echo "暂不更新 release"
	else
		autobumpspec $1 $2
	fi
else
        if [ $AUTOUPDATE = "1" ]; then
                echo "自动更新 $1 版本"
                autoupdate $1 || echo "$1 版本更新未成功，请检查网络环境和相关配置"
        fi	
fi
if [ $AUTOUPDATE = "1" ]; then
#首先判断是否使用版本控制系统的源码，如果是，则下载，目前支持git/cvs/svn/hg
	GIT=$(cat $SPECNAME | grep "^%define git 1" |wc -l)
	CVS=$(cat $SPECNAME | grep "^%define cvs 1" |wc -l)
	SVN=$(cat $SPECNAME | grep "^%define svn 1" |wc -l)
	HG=$(cat $SPECNAME | grep "^%define hgm 1" |wc -l)
	if [ $GIT = "1" ] ; then
		echo "$1.spec 中使用了 git 仓库中的源码，使用脚本下载"
		downvcssources $1 git || exit 1
	fi
	if [ $CVS = "1" ] ; then
        	echo "$1.spec 中使用了 cvs 仓库中的源码，使用脚本下载"
        	downvcssources $1 cvs || exit 1
	fi
	if [ $SVN = "1" ] ; then
        	echo "$1.spec 中使用了 svn 仓库中的源码，使用脚本下载"
        	downvcssources $1 svn || exit 1
	fi
	if [ $HG = "1" ] ; then
        	echo "spec 中使用了 hg 仓库中的源码，使用脚本下载"
        	downvcssources $1 hg || exit 1
	fi
fi
#然后下载源码
downsources $1 || exit 1
# 下载补丁
downpatches $1 || exit 1
# 安装依赖
if [ "NODEPS" = 0 ]; then
installbuildrequires $1 || exit 1
fi
# 打包
build $1 || exit 1
if [ $INSTALLRPMS = "1" ]; then
	installrpms $1 || exit 1
fi
popd
