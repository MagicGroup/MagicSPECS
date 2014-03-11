%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 0
%endif

Summary: Utilities for managing accounts and shadow password files
Summary(zh_CN.UTF-8): 用来管理帐号和屏蔽口令文件的工具
Name: shadow-utils
Version: 4.1.4.3
Release: 2%{?dist}
Epoch: 2
URL: http://pkg-shadow.alioth.debian.org/
Source0: ftp://pkg-shadow.alioth.debian.org/pub/pkg-shadow/shadow-%{version}.tar.bz2
Source1: shadow-utils.login.defs
Source2: shadow-utils.useradd
Patch0: shadow-4.1.4.2-redhat.patch
Patch1: shadow-4.1.4.3-goodname.patch
Patch2: shadow-4.1.4.2-leak.patch
Patch3: shadow-4.1.4.2-fixes.patch
Patch4: shadow-4.1.4.2-infoParentDir.patch
Patch5: shadow-4.1.4.3-semange.patch
Patch6: shadow-4.1.4.2-acl.patch
Patch7: shadow-4.1.4.2-underflow.patch
Patch8: shadow-4.1.4.3-uflg.patch
Patch9: shadow-4.1.4.2-gshadow.patch
Patch10: shadow-4.1.4.3-nopam.patch
Patch11: shadow-4.1.4.3-IDs.patch
#696213 #674878 #739147
Patch12: shadow-4.1.4.3-man.patch
#749205

License: BSD
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
BuildRequires: autoconf, automake, libtool, gettext-devel
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts. The pwconv command
converts passwords to the shadow password format. The pwunconv command
unconverts shadow passwords and generates an npasswd file (a standard
UNIX password file). The pwck command checks the integrity of password
and shadow files. The lastlog command prints out the last login times
for all users. The useradd, userdel, and usermod commands are used for
managing user accounts. The groupadd, groupdel, and groupmod commands
are used for managing group accounts.

%description -l zh_CN.UTF-8
shadow-utils 软件包包括把 UNIX 口令文件转换成屏蔽口令格式，以及管理用户和组
群帐号的程序所必须的程序。pwconv 命令把口令转换成屏蔽口令格式。pwunconv 命
令把屏蔽口令转换回去，然后生成一个 npasswd 文件(一个标准 UNIX 口令文件)。pwck
命令检查口令和屏蔽文件的完整性。lastlog 命令为所有用户打印出最后登录的时间。
useradd、userdel、和 usermod 命令用来管理用户帐号。groupadd、groupdel、和
groupmod 命令用来管理组群帐号。

%prep
%setup -q -n shadow-%{version}

%patch0 -p1 -b .redhat
%patch1 -p1 -b .goodname
%patch2 -p1 -b .leak
%patch3 -p1 -b .fixes
%patch4 -p1 -b .infoParentDir
%patch5 -p1 -b .semange
#%patch6 -p1 -b .acl
%patch7 -p1 -b .underflow
%patch8 -p1 -b .uflg
%patch9 -p1 -b .gshadow
%patch10 -p1 -b .nopam
%patch11 -p1 -b .IDs
%patch12 -p1 -b .man

iconv -f ISO88591 -t utf-8  doc/HOWTO > doc/HOWTO.utf8
cp -f doc/HOWTO.utf8 doc/HOWTO

%build
%configure \
	--enable-shadowgrp \
	--without-audit \
	--with-sha-crypt \
%if %{WITH_SELINUX}
	--with-selinux \
%endif
	--without-libcrack \
	--without-libpam \
	--disable-shared
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd


ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser
#ln -s %{_mandir}/man8/useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
ln -s useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8
for subdir in $RPM_BUILD_ROOT/%{_mandir}/{??,??_??,??_??.*}/man* ; do
	test -d $subdir && test -e $subdir/useradd.8 && echo ".so man8/useradd.8" > $subdir/adduser.8
done

# Remove binaries we don't use.
rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_sysconfdir}/login.access
rm $RPM_BUILD_ROOT/%{_sysconfdir}/limits
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_sbindir}/chgpasswd
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/limits.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/limits.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/login.access.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/login.access.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/porttime.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/porttime.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/chgpasswd.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man8/chgpasswd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man3/getspnam.*
rm $RPM_BUILD_ROOT/%{_mandir}/*/man3/getspnam.*

magic_rpm_clean.sh
%find_lang shadow
find $RPM_BUILD_ROOT%{_mandir} -depth -type d -empty -delete
for dir in $(ls -1d $RPM_BUILD_ROOT%{_mandir}/{??,??_??}) ; do
    dir=$(echo $dir | sed -e "s|^$RPM_BUILD_ROOT||")
    lang=$(basename $dir)
    echo "%%lang($lang) $dir/man*/*" >> shadow.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f shadow.lang
%defattr(-,root,root)
%doc NEWS doc/HOWTO README
%dir %{_sysconfdir}/default
%attr(0644,root,root)	%config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root)	%config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%{_bindir}/chage
%{_bindir}/faillog
%{_bindir}/gpasswd
%{_bindir}/lastlog
%{_bindir}/newgrp
%{_sbindir}/adduser
%attr(0750,root,root)	%{_sbindir}/user*
%attr(0750,root,root)	%{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%{_sbindir}/chpasswd
%{_sbindir}/newusers
%{_sbindir}/vipw
%{_sbindir}/vigr
%{_mandir}/man1/chage.1*
%{_mandir}/man1/gpasswd.1*
%{_mandir}/man1/sg.1*
%{_mandir}/man1/newgrp.1*
%{_mandir}/man3/shadow.3*
%{_mandir}/man5/shadow.5*
%{_mandir}/man5/login.defs.5*
%{_mandir}/man5/gshadow.5*
%{_mandir}/man5/faillog.5*
%{_mandir}/man8/adduser.8*
%{_mandir}/man8/group*.8*
%{_mandir}/man8/user*.8*
%{_mandir}/man8/pwck.8*
%{_mandir}/man8/grpck.8*
%{_mandir}/man8/chpasswd.8*
%{_mandir}/man8/newusers.8*
%{_mandir}/man8/*conv.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/faillog.8*
%{_mandir}/man8/vipw.8*
%{_mandir}/man8/vigr.8*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2:4.1.4.3-2
- 为 Magic 3.0 重建


