%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define LIBMAJ 15

Summary:	GUI independent C++ database application libraries	
Summary(zh_CN.UTF-8): GUI 无关的 C++ 数据库程序库
Name:		hk_classes
Version: 	0.8.3
Release: 	3%{?dist}
License:	GPL
Group:		Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
Source:		http://hk-classes.sourceforge.net/hk_classes-0.8.3.tar.gz

Url:		http://hk-classes.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	fontconfig-devel
BuildRequires:	python-devel 
BuildRequires:  chrpath

# MYSQL support
BuildRequires:	mysql-devel 

# POSTGRESQL support
BuildRequires:  postgresql-devel 

# ODBC support
BuildRequires:  unixODBC-devel

# FIREBIRD support
%define with_firebird 1
BuildRequires:  firebird-devel

# XBASE support
#BuildRequires:  xbsql-devel
%define with_xbase 1
BuildRequires:	xbase-devel

# SQLITE2 support
%define with_sqlite2 1
BuildRequires:  sqlite-devel

#聽SQLITE3 support
%define with_sqlite3 1
BuildRequires:  sqlite-devel

Requires: 	%{name}-libs = %{version}-%{release}


%description
Hk_classes is a set of GUI independent C++ libraries which allow the rapid 
development of database applications and includes command line tools to use 
hk_classes in scripts.

%description -l zh_CN.UTF-8
GUI 无关的数据库程序库

%files
%defattr(-,root,root)
%doc ChangeLog COPYING NEWS INSTALL README
%{_bindir}/hk_actionquery
%{_bindir}/hk_exportcsv
%{_bindir}/hk_exporthtml
%{_bindir}/hk_exportxml
%{_bindir}/hk_importcsv
%{_bindir}/hk_report
%{_bindir}/hk_dbcopy
%config(noreplace) %{_sysconfdir}/hk_classes.conf
%{_mandir}/man1/hk_actionquery.1man*
%{_mandir}/man1/hk_exportcsv.1man*
%{_mandir}/man1/hk_exporthtml.1man*
%{_mandir}/man1/hk_exportxml.1man*
%{_mandir}/man1/hk_importcsv.1man*
%{_mandir}/man1/hk_report.1man*
%{_mandir}/man1/hk_dbcopy.1man*

##########

%package python
Summary:  	Python support for hk_classes
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Group: 		Development/Python
Group(zh_CN.UTF-8): 开发/库
Requires:	python-devel

%description python
Python scripting support for hk_classes.

%description python -l zh_CN.UTF-8
%{name} 的 python 绑定。

%files python
%defattr(-,root,root)
%python_sitearch/*

##########

%package libs
Summary:  	Libraries for hk_classes applications
Summary(zh_CN.UTF-8): %{name} 的运行库
Group: 		System/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
Hk_classes libraries for command-line scripts and application development.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files libs
%defattr(-,root,root)
%{_sysconfdir}/ld.so.conf.d/hk_classes.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libhk_classes.so.%{LIBMAJ}*
%{_libdir}/%{name}/drivers/libhk_dbasedriver.la
%{_libdir}/%{name}/drivers/libhk_dbasedriver.so
%{_libdir}/%{name}/drivers/libhk_dbasedriver.so.0
%{_libdir}/%{name}/drivers/libhk_dbasedriver.so.0.0.0
%if 0%{?with_firebird}
%{_libdir}/%{name}/drivers/libhk_firebirddriver.la
%{_libdir}/%{name}/drivers/libhk_firebirddriver.so
%{_libdir}/%{name}/drivers/libhk_firebirddriver.so.0
%{_libdir}/%{name}/drivers/libhk_firebirddriver.so.0.0.0
%endif
%{_libdir}/%{name}/drivers/libhk_mdbdriver.la
%{_libdir}/%{name}/drivers/libhk_mdbdriver.so
%{_libdir}/%{name}/drivers/libhk_mdbdriver.so.0
%{_libdir}/%{name}/drivers/libhk_mdbdriver.so.0.0.0
%{_libdir}/%{name}/drivers/libhk_mysqldriver.la
%{_libdir}/%{name}/drivers/libhk_mysqldriver.so
%{_libdir}/%{name}/drivers/libhk_mysqldriver.so.3
%{_libdir}/%{name}/drivers/libhk_mysqldriver.so.3.0.4
%{_libdir}/%{name}/drivers/libhk_odbcdriver.la
%{_libdir}/%{name}/drivers/libhk_odbcdriver.so
%{_libdir}/%{name}/drivers/libhk_odbcdriver.so.0
%{_libdir}/%{name}/drivers/libhk_odbcdriver.so.0.0.0
%{_libdir}/%{name}/drivers/libhk_paradoxdriver.la
%{_libdir}/%{name}/drivers/libhk_paradoxdriver.so
%{_libdir}/%{name}/drivers/libhk_paradoxdriver.so.0
%{_libdir}/%{name}/drivers/libhk_paradoxdriver.so.0.0.0
%{_libdir}/%{name}/drivers/libhk_postgresdriver.la
%{_libdir}/%{name}/drivers/libhk_postgresdriver.so
%{_libdir}/%{name}/drivers/libhk_postgresdriver.so.0
%{_libdir}/%{name}/drivers/libhk_postgresdriver.so.0.0.1
%if 0%{?with_sqlite2}
%{_libdir}/%{name}/drivers/libhk_sqlite2driver.la
%{_libdir}/%{name}/drivers/libhk_sqlite2driver.so
%{_libdir}/%{name}/drivers/libhk_sqlite2driver.so.0
%{_libdir}/%{name}/drivers/libhk_sqlite2driver.so.0.0.0
%endif
%if 0%{?with_sqlite3}
%{_libdir}/%{name}/drivers/libhk_sqlite3driver.la
%{_libdir}/%{name}/drivers/libhk_sqlite3driver.so
%{_libdir}/%{name}/drivers/libhk_sqlite3driver.so.0
%{_libdir}/%{name}/drivers/libhk_sqlite3driver.so.0.0.0
%endif

##########

%package devel
Summary:  	Development files for hk_classes applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: 		Development/Databases
Group(zh_CN.UTF-8): 开发/库
Requires: 	%{name}-libs = %{version}-%{release}

%description devel
Hk_classes header files for application development.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/%{name}/libhk_classes.la
%{_libdir}/%{name}/libhk_classes.so

##########

%prep
%setup -q -n %{name}-%{version}
autoreconf -fiv

%build
# HK_CLASSES specific variables !
%ifnarch mips64el
export CXXFLAGS="${RPM_OPT_FLAGS} -DHAVE_IO_H"
%endif
%if "%_lib" == "lib64"
export want_64bit=yes
%endif

%configure \
  --disable-static \
  %{?with_sqlite2:--with-sqlite} %{?!with_sqlite2:--without-sqlite} \
  %{?with_sqlite3:--with-sqlite3} %{?!with_sqlite3:--without-sqlite3}

%__make %{?_smp_mflags}


%install
%__rm -fr %buildroot
%__make install DESTDIR=%{?buildroot}

# (sb) create a default config file
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/hk_classes.conf
<?xml version="1.0" ?>

<HK_VERSION>0.8.2</HK_VERSION>
<GENERAL>
  <SHOWPEDANTIC>YES</SHOWPEDANTIC>
  <DRIVERPATH>%{_libdir}/%{name}/drivers</DRIVERPATH>
  <DEFAULTFONT>Courier</DEFAULTFONT>
  <DEFAULTFONTSIZE>12</DEFAULTFONTSIZE>
  <DEFAULTTEXTALIGNMENT>LEFT</DEFAULTTEXTALIGNMENT>
  <DEFAULTNUMBERALIGNMENT>RIGHT</DEFAULTNUMBERALIGNMENT>
  <MAXIMIZEDWINDOWS>NO</MAXIMIZEDWINDOWS>
  <DEFAULTPRECISION>2</DEFAULTPRECISION>
  <DEFAULTTHOUSANDSSEPARATOR>NO</DEFAULTTHOUSANDSSEPARATOR>
  <DEFAULTDRIVER>mysql</DEFAULTDRIVER>
  <DEFAULTSIZETYPE>ABSOLUTE</DEFAULTSIZETYPE>
  <MEASURESYSTEM>CM</MEASURESYSTEM>
</GENERAL>
<HK_REGIONAL>
  <DEFAULTTIMEFORMAT>h:m:s</DEFAULTTIMEFORMAT>
  <DEFAULTDATETIMEFORMAT>D.M.Y h:m:s</DEFAULTDATETIMEFORMAT>
  <DEFAULTDATEFORMAT>D.M.Y</DEFAULTDATEFORMAT>
  <LOCALE/>
</HK_REGIONAL>
<REPORT>
  <PRINTERCOMMAND>lpr</PRINTERCOMMAND>
  <REPORTFONTENCODING>ISO-8859-1</REPORTFONTENCODING>
</REPORT>
EOF

# (sb) get rid of rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*

# (sb) fix the .la files
perl -pi -e "s|-L$RPM_BUILD_DIR/%{name}-%{version}/hk_classes||g" $RPM_BUILD_ROOT%{_libdir}/%{name}/drivers/*.la

# 'ld.so.conf' file
mkdir -p %buildroot/%_sysconfdir/ld.so.conf.d
echo "%_libdir/%name" >  %buildroot/%_sysconfdir/ld.so.conf.d/%name.conf
magic_rpm_clean.sh

%clean
%__rm -fr %buildroot


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.8.3-3
- 为 Magic 3.0 重建

* Mon Oct 12 2015 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 为 Magic 3.0 重建

* Mon Apr 08 2013 Francois Andriot <francois.andriot@free.fr> 0.8.3-1
- Initial release for TDE 3.5.13.2
