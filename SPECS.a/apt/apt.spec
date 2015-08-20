# $Id: apt.spec 3053 2005-03-24 17:16:13Z dag $
# Authority: axel
# Upstream: Gustavo Niemeyer <niemeyer$conectiva,com>

%{?dist: %{expand: %%define %dist mgc30}}
%define LIBVER 3.3
%define git 1
%define vcsdate 20140228


%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define comps %{_datadir}/comps/%{_build_arch}/comps.xml

Summary: Debian's Advanced Packaging Tool with RPM support
Summary(zh_CN.UTF-8): 使用RPM支持的 Debian 高级包工具
Name: apt
Version: 0.5.15lorg3.95
Release: 10%{?dist}
License: GPL
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: https://apt-rpm.org

Packager: Liu Di <liudidi@gmail.com>
Vendor: MagicGroup
%if 0%{git}
#git clone http://apt-rpm.org/scm/apt.git
Source: %{name}-git%{vcsdate}.tar.xz
%else
Source: http://apt-rpm.org/testing/apt-0.5.15lorg3.94a.tar.bz2
%endif
Source201: make_apt_git_package.sh

# user editable template configs
Source1: apt.conf
Source2: sources.list
Source3: vendors.list
Source4: apt_preferences

# rpmpriorities generated + manually tweaked from comps.xml core group
Source5: rpmpriorities
Source19: comps2prio.xsl

# Sources 50-99 are for Lua-scripts not in contrib/
Source51: upgradevirt.lua
Source52: gpg-check.lua

# 150-199 for apt.conf.d
# "factory defaults"
Source150: default.conf

Source200: apt.service

Patch0: apt-0.5.15lorg3.94-rpmpriorities.patch

# Fix ppc mapping
Patch4: apt-0.5.15lorg3.2-ppc.patch
# band aid for mmap issues (#211254)
Patch1: apt-0.5.15lorg3.x-cache-corruption.patch
# fix build with lua 5.2
Patch3: apt-0.5.15lorg3.95-lua-5.2.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: rpm-devel >= 4.6, zlib-devel, gettext
BuildRequires: readline-devel, bison, lua-devel

%{!?dist:BuildRequires: beecrypt-devel, elfutils-devel}

Requires: rpm >= 4.0, zlib, bzip2-libs, libstdc++

%description
A port of Debian's apt tools for RPM based distributions, or at least
originally for Conectiva and now Red Hat Linux. It provides the apt-get
utility that provides a simpler, safer way to install and upgrade packages.
APT features complete installation ordering, multiple source capability and
several other unique features.

%description -l zh_CN.UTF-8
Debian的apt工具到基本rpm的发行版的一个移植，至少支持Conectiva和红帽Linux，
当然MagicLinux也支持。它提供了apt-get工具，可以简单安全的安装和升级包。
APT的特性有完全的安装次序，多个源的功能并有其它几个独特的特点。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name}的头文件，库和开发文档
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
这个包包含了 %{name} 的头文件，静态链接库和开发文档。如果你想使用 %{name}
开发程序，你需要安装 %{name}-devel。

%package python
Summary: Python bindings for libapt-pkg
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description python
The apt-python package contains a module which allows python programs
to access the APT library interface.

%package plugins-list
Summary: Additional commands to list extra packages and leaves
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description plugins-list
This package adds commands for listing all installed packages which
are not availabe in any online repository, and packages that are not
required by any other installed package:
apt-cache list-extras
apt-cache list-nodeps


%package plugins-log
Summary: Log the changes being introduced by the transaction
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}

%description plugins-log
This script will log the changes being introduced by
the transaction which is going to be run, and is based
on an idea of Panu Matilainen.

When some transaction is run, it will dump information
about it in /var/log/apt.log, or in the configured file.

%prep
%if 0%{git}
%setup -q -n %{name}-git%{vcsdate}
%else
%setup
%endif
%patch0 -p1 -b .rpmpriorities
%patch4 -p1 -b .ppc
%patch1 -p0 -b .mmap
%patch3 -p1 -b .lua-52

%{__perl} -pi.orig -e 's|RPM APT-HTTP/1.3|Dag RPM Repository %{dist}/%{_arch} APT-HTTP/1.3|' methods/http.cc

install -pm 644 %{SOURCE19} comps2prio.xsl

# don't require python, lua etc because of stuff in doc/contrib
find contrib/ -type f | xargs chmod 0644

cp -p %{SOURCE5} rpmpriorities
%if 0%{?generate_rpmpriorities}
xsltproc -o rpmpriorities comps2prio.xsl %{comps}
%endif

%build
autoreconf -fisv
%configure \
	--program-prefix="%{?_program_prefix}" \
	--includedir="%{_includedir}/apt-pkg"
#	--with-hashmap
%{__make} %{?_smp_mflags}

make -C python %{?_smp_mflags} PYTHON="%{__python}"
python -O -c "import py_compile; py_compile.compile('python/apt.py')"

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	includedir="%{buildroot}%{_includedir}/apt-pkg"
#%find_lang %{name}

# The state files
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/archives/partial
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/genpkglist
mkdir -p %{buildroot}%{_localstatedir}/cache/apt/gensrclist
mkdir -p %{buildroot}%{_localstatedir}/lib/apt/lists/partial

# The config files
mkdir -p %{buildroot}%{_sysconfdir}/apt
mkdir -p %{buildroot}%{_sysconfdir}/apt/apt.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/apt/sources.list.d
mkdir -p %{buildroot}%{_sysconfdir}/apt/vendors.list.d
#iinstall -pm 644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/apt/apt.conf
install -pm 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/apt/sources.list
install -pm 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/apt/vendors.list
install -pm 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/apt/preferences
install -pm 644 rpmpriorities %{buildroot}/%{_sysconfdir}/apt/

# install config parts
install -pm 644 %{SOURCE150} %{buildroot}%{_sysconfdir}/apt/apt.conf.d/

# Lua scripts
mkdir -p %{buildroot}%{_datadir}/apt/scripts
for script in %{SOURCE51} %{SOURCE52} ; do
 install -pm 755 $script %{buildroot}%{_datadir}/apt/scripts
done

%{__install} -p -m0644 etc/rpmpriorities %{buildroot}%{_sysconfdir}/apt/

# The python bindings
mkdir -p %{buildroot}%{python_sitearch}/
install -pm 755 python/_apt.so %{buildroot}%{python_sitearch}/
install -pm 644 python/apt.py* %{buildroot}%{python_sitearch}/
touch %{buildroot}%{python_sitearch}/apt.pyo

# Nightly updater scripts & default config
mkdir -p %{buildroot}%{_unitdir}
install -Dpm 755 %{SOURCE200} %{buildroot}%{_unitdir}/apt.service
install -Dpm 755 contrib/apt-cron/apt.cron %{buildroot}/%{_sysconfdir}/cron.daily/apt.cron
install -Dpm 644 contrib/apt-cron/apt.sysconfig %{buildroot}/%{_sysconfdir}/sysconfig/apt

# apt-plugins-list from contrib
%if 0%{!?_without_list:1}
install -pm 755 contrib/list-extras/list-extras.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/list-extras/list-extras.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
install -pm 755 contrib/list-nodeps/list-nodeps.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/list-nodeps/list-nodeps.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
%endif

# apt-plugins-log from contrib
%if 0%{!?_without_log:1}
install -pm 755 contrib/log/log.lua %{buildroot}/%{_datadir}/apt/scripts
install -pm 644 contrib/log/log.conf %{buildroot}/%{_sysconfdir}/apt/apt.conf.d/
%endif

# nuke .la files
rm -f %{buildroot}%{_libdir}/*.la

magic_rpm_clean.sh

mkdir -p %{buildroot}/var/lib/apt/lists/partial
touch %{buildroot}/var/lib/apt/lists/lock

%post
if [ $1 -eq 1 ] ; then
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
/sbin/ldconfig

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable apt.service > /dev/null 2>&1 || :
    /bin/systemctl stop apt.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart apt.service >/dev/null 2>&1 || :
fi
/sbin/ldconfig

%triggerun -- apt < 0.5.15lorg3.95-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply apt
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save apt >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del apt >/dev/null 2>&1 || :
/bin/systemctl try-restart apt.service >/dev/null 2>&1 || :

%clean
%{__rm} -rf %{buildroot}

#%files -f %{name}.lang
%files
%defattr(-, root, root, 0755)
%doc AUTHORS* COPYING* ABOUT* TODO comps2prio.xsl doc/examples/ contrib/

%dir %{_sysconfdir}/apt/
#%config(noreplace) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %{_sysconfdir}/apt/preferences
%config(noreplace) %{_sysconfdir}/apt/rpmpriorities
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/apt/vendors.list
%dir %{_sysconfdir}/apt/apt.conf.d/
# NOTE: no noreplace because we WANT to be able to change the defaults
# without user intervention!
%config %{_sysconfdir}/apt/apt.conf.d/default.conf
%config %{_sysconfdir}/apt/apt.conf.d/multilib.conf
%dir %{_sysconfdir}/apt/sources.list.d/
%dir %{_sysconfdir}/apt/vendors.list.d/

%config(noreplace) %{_sysconfdir}/sysconfig/apt
%{_sysconfdir}/cron.daily/apt.cron

%{_unitdir}/apt.service

%{_bindir}/apt-cache
%{_bindir}/apt-cdrom
%{_bindir}/apt-config
%{_bindir}/apt-shell
%{_bindir}/apt-get
%{_bindir}/countpkglist
%{_bindir}/genpkglist
%{_bindir}/gensrclist
%{_bindir}/genbasedir
%{_libdir}/libapt-pkg*.so.*
%{_libdir}/apt/
%dir %{_datadir}/apt/
%dir %{_datadir}/apt/scripts/
%{_datadir}/apt/scripts/gpg-check.lua
%{_datadir}/apt/scripts/upgradevirt.lua
%{_localstatedir}/cache/apt/
%{_localstatedir}/lib/apt/
%{_mandir}/man[58]/*.[58]*

%files devel
%defattr(-, root, root, 0755)
%{_libdir}/libapt-pkg.a
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libapt-pkg.so
%{_includedir}/apt-pkg/

%files python
%{python_sitearch}/_apt.so
%{python_sitearch}/apt.py*

%if 0%{!?_without_list:1}
%files plugins-list
%config %{_sysconfdir}/apt/apt.conf.d/list-extras.conf
%config %{_sysconfdir}/apt/apt.conf.d/list-nodeps.conf
%{_datadir}/apt/scripts/list-extras.lua
%{_datadir}/apt/scripts/list-nodeps.lua
%endif

%if 0%{!?_without_log:1}
%files plugins-log
%config %{_sysconfdir}/apt/apt.conf.d/log.conf
%{_datadir}/apt/scripts/log.lua
%endif

%changelog
* Wed Jul 29 2015 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-9
- 更新到 20150729 日期的仓库源码

* Wed Jul 29 2015 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-9
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-7
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.95-6
- 为 Magic 3.0 重建

* Thu Apr 30 2009 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.94a-4
- 在 rpm 4.7.0 上重建

* Mon Jan 21 2008 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.94a-1mgc
- update 

* Fri Sep 15 2006 Liu Di <liudidi@gmail.com> - 0.5.15lorg3.90-1mgc
- update

* Fri Jul 09 2006 Liu Di <liudidi@gmail.com> - 0.5.15lorg3-2mgc
- Rebuild for RPM 4.4, add cuit.lcuc.ort to apt source

* Tue May 16 2006 Liudi <liudidi@gmail.com>
- fix magic-apt setting

* Tue Aug 2 2005 KanKer <kanker@163.com>
- fix magic-apt setting error

* Wed Jul 27 2005 KanKer <kanker@163.com>
- rebuild

* Sat Nov 20 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-4 - 3053+/dag
- Added readline-devel as buildrequirement for apt-shell.

* Thu Jul 01 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-3
- Fix for apt-bug triggered by mach.

* Fri Jun 04 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-2
- Make apt understand about architectures.

* Tue Mar 23 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc6-1
- Updated to release 0.5.15cnc6.

* Sat Jan 24 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-1
- Added RHAS21 repository.

* Sun Jan 04 2004 Dag Wieers <dag@wieers.com> - 0.5.15cnc5-0
- Updated to release 0.5.15cnc5.

* Sat Dec 06 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc4-1
- Disabled the epoch promotion behaviour on RH9.

* Thu Dec 04 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc4-0
- Updated to release 0.5.15cnc4.

* Tue Nov 25 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc3-0
- Updated to release 0.5.15cnc3.

* Mon Nov 10 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc2-0
- Updated to release 0.5.15cnc2.

* Mon Nov 10 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-1
- Fixed apt pinning.
- Added RHFC1 repository.

* Sat Nov 08 2003 Dag Wieers <dag@wieers.com> - 0.5.15cnc1-0
- Updated to release 0.5.15cnc1.

* Sun Oct 26 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc6-1
- Added RHEL3 repository.

* Tue Jun 10 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc6-0
- Added newrpms and enable it by default.
- Updated to release 0.5.5cnc6.

* Tue Jun 03 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-4
- Added freshrpms and enable it by default.

* Sun Jun 01 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-3
- Work around a bug in apt (apt.conf).

* Fri May 30 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-2
- Moved sources.list to sources.d/

* Wed Apr 16 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc5-1
- Updated to release 0.5.5cnc5.

* Tue Apr 08 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-2
- RH90 repository rename from redhat/9.0 to redhat/9.

* Sat Apr 05 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-1
- FreshRPMS fixes to repository locations.

* Sun Mar 09 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc4.1-0
- Updated to release 0.5.5cnc4.1.

* Fri Feb 28 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc3-0
- Updated to release 0.5.5cnc3.

* Tue Feb 25 2003 Dag Wieers <dag@wieers.com> - 0.5.5cnc2-0
- Updated to release 0.5.5cnc2.

* Mon Feb 10 2003 Dag Wieers <dag@wieers.com> - 0.5.4cnc9-0
- Initial package. (using DAR)
