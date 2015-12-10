#
# spec file for package krename (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg krename
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.0.14
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	A TDE batch file renaming utility
Summary(zh_CN.UTF-8): KDE 下一个强大的批量重命名程序
Group: Applications/Tools
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1: krename.zh_CN.po
Source2: krename.desktop
Source3: krename_dir.desktop
Source4: krenameservicemenu.desktop


Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

%description
Krename is a very powerful batch file renamer for KDE3 which can rename a list of files based on a set of expressions. It can copy/move the files to another directory or simply rename the input files. Krename supports many conversion operations, including conversion of a filename to lowercase or to uppercase, conversion of the first letter of every word to uppercase, adding numbers to filenames, finding and replacing parts of the filename, and many more. It can also change access and modification dates, permissions, and file ownership.

%description -l zh_CN.UTF-8
Krename 是 KDE 下的一个非常强大的批量重命名工具，它可以基于一个表达式集合
为一连串文件重命名。它可以复制/移动文件到其它目录或者只是重命名输入的文件。
Krename 支持许多转换选项，包括把文件名转成大写或小写，转换每个单词的首字母
大写，在文件名上添加数字，查找和替换部分文件名，以及许多其它内容。它还可以
更改访问和修改日期、许可权以及所有权。

##########


%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

install -d -m755 $RPM_BUILD_ROOT%{tde_datadir}/locale/zh_CN/LC_MESSAGES
msgfmt %{SOURCE1} -o $RPM_BUILD_ROOT%{tde_datadir}/locale/zh_CN/LC_MESSAGES/krename.mo

%find_lang %{tde_pkg}


%clean
%__rm -rf %{buildroot}


%post
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_tdeappdir} &> /dev/null

%postun
for f in hicolor locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
update-desktop-database %{tde_tdeappdir} &> /dev/null

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/krename
%{tde_tdeappdir}/krename.desktop
%{tde_datadir}/apps/konqueror/servicemenus/krename_dir.desktop
%{tde_datadir}/apps/konqueror/servicemenus/krenameservicemenu.desktop
%{tde_datadir}/apps/krename/
%{tde_tdedocdir}/HTML/en/krename/
%{tde_datadir}/icons/hicolor/*/apps/krename.png
%{tde_datadir}/icons/locolor/*/apps/krename.png


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:3.0.14-1.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.0.14-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.0.14-1
- Initial release for TDE 14.0.0
