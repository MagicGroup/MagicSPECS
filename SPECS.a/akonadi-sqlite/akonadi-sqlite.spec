
## Can be either MYSQL(uptsream default), SQLITE, or POSTGRES(untested)
%global database_backend SQLITE 

%define real_name akonadi

Summary: PIM Storage Service
Summary(zh_CN.UTF-8): 个人信息管理存储服务
Name:    %{real_name}-sqlite
Version: 1.8.0
Release: 3%{?dist}

Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: LGPLv2+
URL:     http://download.akonadi-project.org/
%if 0%{?snap}
# git clone git://git.kde.org/akonadi
# git archive --prefix=akonadi-%{version}/ master | bzip2 > akonadi-%{version}-%{snap}.tar.bz2
Source0: akonadi-%{version}-%{snap}.tar.bz2
%else
# Official release
Source0: ftp://ftp.kde.org/pub/kde/stable/akonadi/src/akonadi-%{version}.tar.bz2
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define mysql_conf_timestamp 20110629

BuildRequires: automoc4
BuildRequires: boost-devel
BuildRequires: cmake >= 2.6.0
%if "%{?database_backend}" == "MYSQL"
BuildRequires: mysql-devel
BuildRequires: mysql-server
%endif
# for xsltproc
BuildRequires: libxslt
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtSql) pkgconfig(QtXml)
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(soprano) 
BuildRequires: pkgconfig(sqlite3) >= 3.6.23

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%if "%{?database_backend}" == "MYSQL"
Requires: qt4-mysql%{?_isa}
# not *strictly* required, but we need a functional default configuration
Requires: mysql-server
%endif
Requires(postun): /usr/sbin/ldconfig

Provides: %{real_name}

%description
%{summary}.
%if "%{?database_backend}" == "MYSQL"
Requires an available instance of mysql server at runtime.  
Akonadi can spawn a per-user one automatically if the mysql-server 
package is installed on the machine.
See also: %{_sysconfdir}/akonadi/mysql-global.conf
%endif

%description -l zh_CN.UTF-8
个人信息管理存储服务。
%if "%{?database_backend}" == "MYSQL"
需要一个 mysql 服务的可用实例在运行。
如果你的机器上装有 mysql-sever 包，Akonadi 可以自动产生每个用户。
可以查看: %{_sysconfdir}/akonadi/mysql-global.conf
%endif

%package devel
Summary: Developer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发文件
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发文件。

%prep
%setup -q -n akonadi-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DCONFIG_INSTALL_DIR=%{_sysconfdir} \
  %{?database_backend:-DDATABASE_BACKEND=%{database_backend}} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot} 
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

mkdir -p %{buildroot}%{_datadir}/akonadi/agents

%if "%{?database_backend}" == "MYSQL"
# create "big" config (analog to -mobile.conf)
install -p \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global-big.conf

# default to small/mobile config
install -p \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global-mobile.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global.conf

touch -d %{mysql_conf_timestamp} \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-global*.conf \
  %{buildroot}%{_sysconfdir}/akonadi/mysql-local.conf
%else
rm -f %{buildroot}%{_sysconfdir}/akonadi/mysql-global-mobile.conf
rm -f %{buildroot}%{_sysconfdir}/akonadi/mysql-global.conf
%endif

# create/own %{_libdir}/akondi
mkdir -p %{buildroot}%{_libdir}/akonadi

# %%ghost'd global akonadiserverrc 
touch akonadiserverrc 
install -p -m644 -D akonadiserverrc %{buildroot}%{_sysconfdir}/xdg/akonadi/akonadiserverrc
magic_rpm_clean.sh

%check
#make test -C %{_target_platform}
#export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
#test "$(pkg-config --modversion akonadi)" = "%{version}"


%clean
rm -rf %{buildroot}


%post -p /usr/sbin/ldconfig

%posttrans
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
/usr/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  update-mime-database %{_datadir}/mime &> /dev/null ||:
fi


%files
%defattr(-,root,root,-)
%doc AUTHORS lgpl-license
%dir %{_sysconfdir}/xdg/akonadi/
%ghost %config(missingok,noreplace) %{_sysconfdir}/xdg/akonadi/akonadiserverrc
%dir %{_sysconfdir}/akonadi/
# example conf's
%if "%{?database_backend}" == "MYSQL"
%{_sysconfdir}/akonadi/mysql-global-big.conf
%{_sysconfdir}/akonadi/mysql-global-mobile.conf
%config(noreplace) %{_sysconfdir}/akonadi/mysql-global.conf
%config(noreplace) %{_sysconfdir}/akonadi/mysql-local.conf
%endif
%{_bindir}/akonadi_agent_launcher
%{_bindir}/akonadi_agent_server
%{_bindir}/akonadi_control
%{_bindir}/akonadi_rds
%{_bindir}/akonadictl
%{_bindir}/akonadiserver
%{_libdir}/akonadi/
%{_libdir}/libakonadiprotocolinternals.so.1*
%{_datadir}/dbus-1/interfaces/org.freedesktop.Akonadi.*.xml
%{_datadir}/dbus-1/services/org.freedesktop.Akonadi.*.service
%{_datadir}/mime/packages/akonadi-mime.xml
%{_datadir}/akonadi/
%{_qt4_plugindir}/sqldrivers/libqsqlite3.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/akonadi/
%{_libdir}/pkgconfig/akonadi.pc
%{_libdir}/libakonadiprotocolinternals.so
%{_libdir}/cmake/Akonadi/


%changelog
* Sat Nov 17 2012 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Sat Nov 17 2012 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Thu Oct 27 2011 Liu Di <liudidi@gmail.com> - 1.6.2-3
- 升级到 1.6.2
