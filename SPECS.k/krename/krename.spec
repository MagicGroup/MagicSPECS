Summary: A powerfull batch renamer for KDE
Summary(zh_CN.UTF-8): KDE 下一个强大的批量重命名程序
Name: krename
Version: 3.0.14
License: GPL
Release: 1%{?dist}
Url: http://krename.sourceforge.net
Packager: Liu Di <liudidi@gmail.com>
Group: Applications/Tools
Group(zh_CN.UTF-8): 应用程序/工具
Source0: %{name}-%{version}.tar.bz2
Source1: krename.zh_CN.po
Source2: krename.desktop
Source3: krename_dir.desktop
Source4: krenameservicemenu.desktop
Patch1:	 krename-3.0.14-admin.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
Krename is a very powerful batch file renamer for KDE3 which can rename a list of files based on a set of expressions. It can copy/move the files to another directory or simply rename the input files. Krename supports many conversion operations, including conversion of a filename to lowercase or to uppercase, conversion of the first letter of every word to uppercase, adding numbers to filenames, finding and replacing parts of the filename, and many more. It can also change access and modification dates, permissions, and file ownership.

%description -l zh_CN.UTF-8
Krename 是 KDE 下的一个非常强大的批量重命名工具，它可以基于一个表达式集合
为一连串文件重命名。它可以复制/移动文件到其它目录或者只是重命名输入的文件。
Krename 支持许多转换选项，包括把文件名转成大写或小写，转换每个单词的首字母
大写，在文件名上添加数字，查找和替换部分文件名，以及许多其它内容。它还可以
更改访问和修改日期、许可权以及所有权。

%prep
%setup -q
%patch1 -p1

cp -f %{SOURCE2} %{SOURCE3} %{SOURCE4} krename/
chmod 777 admin/*

%build
make -f admin/Makefile.common
# Look for common rpm-options:
if [ -f /etc/opt/kde3/common_options ]; then
  . /etc/opt/kde3/common_options
  ./configure $configkde
else
  %configure -q
fi
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-ltdefx \-lDCOP \-lkio/g' krename/Makefile
make %{_smp_mflags}

%install
make install-strip DESTDIR=$RPM_BUILD_ROOT
install -d -m755 $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES
msgfmt %{SOURCE1} -o $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES/krename.mo

cd $RPM_BUILD_ROOT
find . -type d | sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' > $RPM_BUILD_DIR/master.list
find . -type f | sed 's,^\.,\%attr(-\,root\,root) ,' >>  $RPM_BUILD_DIR/master.list
find . -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >>  $RPM_BUILD_DIR/master.list

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir} %{_builddir}/master.list
#rm -rf $RPM_BUILD_ROOT
#cd $RPM_BUILD_DIR
#rm -rf %{name}-%{version}
#rm master.list

%files -f ../master.list

%changelog
* Tue May 08 2007 kde <athena_star {at} 163 {dot} com> - 3.0.14-1mgc
- update to 3.0.14
- modify the spec file
- fix the spec's translation and update krename.zh_CN.po

* Tue Jan 02 2007 Liu Di <liudidi@gmail.com> - 3.0.13-1mgc
- update to 3.0.13

* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 3.0.12-1mgc
- update to 3.0.12

* Sun Jul 31 2005 kde <jack@linux.net.cn> - 3.0.6-2mgc
- fix the translation and add krename.zh_CN.po

* Sun Jul 31 2005 kde <jack@linux.net.cn> - 3.0.6-1mgc
- modify the spec file
- add a krename.desktop file
