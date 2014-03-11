%global pkgname Firebird-2.5.2.26539-0
%global fbroot %{_libdir}/%{name}
%global major 2.5.2


Summary: SQL relational database management system
Name:  firebird
Version: 2.5.2.26539.0
Release: 2%{?dist}

Group:  Applications/Databases
License: Interbase
URL:  http://www.firebirdsql.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

Source0: http://downloads.sourceforge.net/firebird/%{pkgname}.tar.bz2
Source1: firebird-logrotate
Source2: README.Fedora
Source3: firebird.conf
Source4: firebird-classic@.service
Source5: firebird-classic.socket
Source6: firebird-superclassic.service
Source7: firebird-superserver.service

# from upstream
Patch0: firebird-2.5.2-svn-CORE-3946.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: libtool
BuildRequires: ncurses-devel
BuildRequires: libtermcap-devel
BuildRequires: libicu-devel
BuildRequires: libedit-devel
BuildRequires: gcc-c++
%if 0%{?fedora}>=14
BuildRequires: libstdc++-static
%endif
%ifnarch %{ix86} x86_64
BuildRequires: libatomic_ops-devel
%endif
BuildRequires: systemd-units

Requires: %{name}-arch = %{version}-%{release}
Requires: grep
Requires: sed
Requires(post):  /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/sbin/userdel
Requires(postun): /usr/sbin/groupdel
Requires(pre):  /usr/sbin/groupadd
Requires(pre):  /usr/sbin/useradd
Requires:  %{name}-libfbclient
Requires:  logrotate
Requires:  %{name}-filesystem 

%description
This package contains common files between firebird-classic, firebird-superclassic and
firebird-superserver. You will need this if you want to use either one.

%package  doc
Summary:  Documentation for Firebird SQL RDBMS
Group:    Applications/Databases

%description doc
This are the Firebird SQL Database shared doc and examples files.

%package  filesystem
Summary:  Filesystem for Firebird SQL RDBMS
Group:    Applications/Databases

%description filesystem
This is the Firebird SQL Database root file system.

%package   classic-common
Summary:   Common files for Firebird "classic" and "superclassic" servers
Group:     Applications/Databases
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libfbembed = %{version}-%{release}
Conflicts: %{name}-superserver

%description classic-common
This package contains the command line utilities and files common to classic and superclassic Firebird servers.

%package  devel
Summary:  Development Libraries for Firebird SQL RDBMS
Group:   Applications/Databases
Requires:  %{name}-libfbclient = %{version}-%{release}
Requires:  %{name}-libfbembed = %{version}-%{release}

%description devel
Development libraries for firebird.

%package  classic
Summary:  Classic server for Firebird SQL RDBMS
Group:   Applications/Databases
Provides:  %{name}-arch = %{version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires:  %{name} = %{version}-%{release}
Conflicts:  %{name}-superclassic
Requires:  %{name}-libfbembed = %{version}-%{release}
Requires:  %{name}-classic-common = %{version}-%{release} 

%description classic
This is the Classic server Firebird SQL RDBMS.
It can also be used as an embedded server, when paired with the
client-embedded package.

%package  superclassic
Summary:  SuperClassic (single process) server for Firebird SQL RDBMS
Group:   Applications/Databases
Provides:  %{name}-arch = %{version}-%{release}
Requires:  %{name} = %{version}-%{release}
Conflicts:  %{name}-classic
Requires:  %{name}-classic-common = %{version}-%{release} 
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description  superclassic
The "superclassic" architecture uses a new thread to handle each connection.
This allows for good scaling on multi-processor machines without consuming too much operating system resources..

%package  superserver
Summary:  Superserver (single process) server for Firebird SQL RDBMS
Group:   Applications/Databases
Provides:  %{name}-arch = %{version}-%{release}
Requires:  %{name} = %{version}-%{release}
Conflicts:  %{name}-classic-common
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description  superserver
This is the Superserver (single process) Firebird SQL RDBMS.

%package  libfbclient
Summary:  Multi-threaded, non-local client libraries for Firebird SQL RDBMS
Group:   System Environment/Libraries
Requires(post):  /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description  libfbclient
Multi-threaded, non-local client libraries for Firebird SQL Database

%package  libfbembed
Summary:  Multi-process, local client libraries for Firebird SQL RDBMS
Group:   System Environment/Libraries
Requires(post):  /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description  libfbembed
Multi-process, local client libraries for Firebird SQL RDBMS


%prep
%setup -q -n %{pkgname}
%patch0
# convert intl character to UTF-8
iconv -f ISO-8859-1 -t utf-8 -c ./doc/README.intl     -o ./doc/README.intl

%build

# classic
%ifarch sparc64 
export CXXFLAGS='-m64'
export CFLAGS='-m64'
export LDFLAGS='-m64'
%endif
%ifarch sparcv9 
export CXXFLAGS='-m32'
export CFLAGS='-m32'
export LDFLAGS='-m32'
%endif

NOCONFIGURE=1 ./autogen.sh
%configure --prefix=%{fbroot} --with-system-icu --with-system-editline \
 --with-fbbin=%{fbroot}/bin-classic --with-fbinclude=%{_includedir}/%{name} \
 --with-fbsbin=%{_sbindir} --with-fbconf=%{_sysconfdir}/%{name} --with-fblib=%{_libdir} \
 --with-fbdoc=%{_defaultdocdir}/%{name} --with-fbudf=%{fbroot}/UDF --with-fbsample=%{_defaultdocdir}/%{name}/examples \
 --with-fbsample-db=%{_localstatedir}/lib/%{name}/data/ \
 --with-fbhelp=%{_localstatedir}/lib/%{name}/system/ --with-fbintl=%{fbroot}/intl \
 --with-fbmisc=%{fbroot}/misc --with-fbsecure-db=%{_localstatedir}/lib/%{name}/system \
 --with-fbmsg=%{_localstatedir}/lib/%{name}/system --with-fblog=%{_localstatedir}/log/%{name} \
 --with-fbglock=%{_var}/run/%{name} --with-fbplugins=%{fbroot}/plugins-classic
%ifarch sparc64 
sed "s@COMMON_FLAGS=-m32@COMMON_FLAGS=-m64@" -i ./gen/make.platform 
%endif
  
# Can't use make %{?_smp_mflags} as parallel build is broken
make

cd gen
sed "s@exit 1@# exit 1@" -i ./install/makeInstallImage.sh
sed "s@chown@echo ""# chown@g" -i ./install/makeInstallImage.sh
sed "s@chmod@echo ""# chmod@g" -i ./install/makeInstallImage.sh
./install/makeInstallImage.sh

mv  ./buildroot/ buildroot-classic
cd ..

# superserver
%configure --prefix=%{fbroot} --with-system-icu --with-system-editline --enable-superserver \
 --with-fbbin=%{fbroot}/bin-superserver --with-fbinclude=%{_includedir}/%{name} \
 --with-fbsbin=%{_sbindir} --with-fbconf=%{_sysconfdir}/%{name} --with-fblib=%{_libdir} \
 --with-fbdoc=%{_defaultdocdir}/%{name} --with-fbudf=%{fbroot}/UDF --with-fbsample=%{_defaultdocdir}/%{name}/examples \
 --with-fbsample-db=%{_localstatedir}/lib/%{name}/data/ \
 --with-fbhelp=%{_localstatedir}/lib/%{name}/system/ --with-fbintl=%{fbroot}/intl \
 --with-fbmisc=%{fbroot}/misc --with-fbsecure-db=%{_localstatedir}/lib/%{name}/system \
 --with-fbmsg=%{_localstatedir}/lib/%{name}/system --with-fblog=%{_localstatedir}/log/%{name} \
 --with-fbglock=%{_var}/run/%{name} --with-fbplugins=%{fbroot}/plugins-superserver
  
%ifarch sparc64 
sed "s@COMMON_FLAGS=-m32@COMMON_FLAGS=-m64@" -i ./gen/make.platform 
%endif

# Can't use make %{?_smp_mflags} as parallel build is broken
make clean
make

cd gen
sed "s@exit 1@echo ""# exit 1@" -i ./install/makeInstallImage.sh
sed "s@chown@echo ""# chown@g" -i ./install/makeInstallImage.sh
sed "s@chmod@echo ""# chmod@g" -i ./install/makeInstallImage.sh
./install/makeInstallImage.sh


%install
# we wanted to setup both Classic and Superserver, we need to do all here
rm -Rf %{buildroot}
install -d %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{fbroot}/bin-superserver
mkdir -p %{buildroot}%{fbroot}/bin-classic
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{fbroot}/UDF
mkdir -p %{buildroot}%{fbroot}/intl
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/data
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/system
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_var}/run/%{name}
touch %{buildroot}%{_var}/run/%{name}/fb_guard
mkdir -p %{buildroot}%{fbroot}/plugins-superserver
mkdir -p %{buildroot}%{fbroot}/plugins-classic
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/tmpfiles.d/
mkdir -p %{buildroot}%{_initrddir} 
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}

cd %{buildroot}
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{_sysconfdir}/%{name}/I*.txt
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sysconfdir}/%{name}/* %{buildroot}%{_sysconfdir}/%{name}
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/bin-classic/* %{buildroot}%{fbroot}/bin-classic
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_config %{buildroot}%{fbroot}/bin-classic/fb_config
sed "s@-classic@-superserver@" %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_config > %{buildroot}%{fbroot}/bin-superserver/fb_config
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fbguard %{buildroot}%{_sbindir}/fbguard
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_inet_server %{buildroot}%{_sbindir}/fb_inet_server
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_lock_print %{buildroot}%{_sbindir}/fb_lock_print
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_sbindir}/fb_smp_server %{buildroot}%{_sbindir}/fb_smp_server
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sbindir}/fbserver %{buildroot}%{_sbindir}/fbserver
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/fb_inet_server
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/fb_smp_server
rm -f %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/changeMultiConnectMode.sh
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/bin-superserver/* %{buildroot}%{fbroot}/bin-superserver
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_includedir}/*.h %{buildroot}%{_includedir}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_includedir}/%{name}/* %{buildroot}%{_includedir}/%{name}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_sysconfdir}/%{name}/* %{buildroot}%{_sysconfdir}/%{name}
rm -f %{buildroot}%{_sysconfdir}/%{name}/README
rm -f %{buildroot}%{_sysconfdir}/%{name}/WhatsNew

cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{_libdir}/lib* %{buildroot}%{_libdir}
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/UDF/* %{buildroot}%{fbroot}/UDF
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_localstatedir}/lib/%{name}/data/* %{buildroot}%{_localstatedir}/lib/%{name}/data
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{_localstatedir}/lib/%{name}/system/* %{buildroot}%{_localstatedir}/lib/%{name}/system
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/plugins-superserver/* %{buildroot}%{fbroot}/plugins-superserver
cp -d %{_builddir}/%{pkgname}/gen/buildroot-classic%{fbroot}/plugins-classic/* %{buildroot}%{fbroot}/plugins-classic
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/intl/fbintl %{buildroot}%{fbroot}/intl/fbintl
cp -d %{_builddir}/%{pkgname}/gen/buildroot%{fbroot}/intl/fbintl.conf %{buildroot}%{_sysconfdir}/%{name}/fbintl.conf
ln -s %{_sysconfdir}/%{name}/fbintl.conf .%{fbroot}/intl/fbintl.conf

cd %{buildroot}%{_libdir}
ln -s libfbclient.so libgds.so
ln -s libfbclient.so.%{major} libgds.so.0
cd %{buildroot}

echo 1 > %{buildroot}%{_localstatedir}/log/%{name}/%{name}.log
sed "s@%{name}.log@%{_localstatedir}/log/%{name}/%{name}.log@g" %{SOURCE1} > %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

install -p -m 644 -D %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/%{name}-classic\@.service
install -p -m 644 -D %{SOURCE5} $RPM_BUILD_ROOT%{_unitdir}/%{name}-classic.socket

install -p -m 644 -D %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/%{name}-superclassic.service
install -p -m 644 -D %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}/%{name}-superserver.service

sed "s@%%{fbroot}@%{fbroot}@g" %{SOURCE2} > %{_builddir}/%{pkgname}/doc/README.Fedora

cd %{buildroot}
ln -s %{fbroot}/bin/fbsvcmgr .%{_bindir}/fbsvcmgr
ln -s %{fbroot}/bin/fbtracemgr .%{_bindir}/fbtracemgr
ln -s %{fbroot}/bin/gbak .%{_bindir}/gbak
ln -s %{fbroot}/bin/gdef .%{_bindir}/gdef
ln -s %{fbroot}/bin/gfix .%{_bindir}/gfix
ln -s %{fbroot}/bin/gpre .%{_bindir}/gpre
ln -s %{fbroot}/bin/gsec .%{_bindir}/gsec
ln -s %{fbroot}/bin/gsplit .%{_bindir}/gsplit
ln -s %{fbroot}/bin/gstat .%{_bindir}/gstat-fb
ln -s %{fbroot}/bin/isql .%{_bindir}/isql-fb
ln -s %{fbroot}/bin/nbackup .%{_bindir}/nbackup
ln -s %{fbroot}/bin/qli .%{_bindir}/qli
ln -s %{fbroot}/bin/fb_config .%{_bindir}/fb_config
magic_rpm_clean.sh

%clean
rm -Rf %{buildroot}

%post libfbclient -p /sbin/ldconfig

%postun libfbclient -p /sbin/ldconfig

%post libfbembed -p /sbin/ldconfig

%postun libfbembed -p /sbin/ldconfig

%post classic-common
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-classic" ]; then 
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-classic,}
fi

%post classic
%if 0%{?fedora}>=16
 [ -e %{_sysconfdir}/xinetd.d/%{name} ] && rm -f %{_sysconfdir}/xinetd.d/%{name}
%endif
%systemd_post firebird-classic.socket
exit 0

%preun classic
%systemd_preun firebird-classic.socket
exit 0

%postun classic
%systemd_postun_with_restart firebird-classic.socket

%preun classic-common
if [ $1 -eq 0 ]; then
 if [ "$(readlink %{fbroot}/bin 2> /dev/null)" = "%{fbroot}/bin-classic" ]; then
  rm -f %{fbroot}/bin
 fi
fi

%preun superclassic
%systemd_preun firebird-superclassic.service

%post superclassic
%systemd_post firebird-superclassic.service

%postun superclassic
%systemd_postun_with_restart firebird-superclassic.service

%post superserver
if [ "$(readlink %{fbroot}/bin 2> /dev/null)" \!= "%{fbroot}/bin-superserver" ]; then 
 [ -e %{fbroot}/bin ] && rm -f %{fbroot}/bin
 ln -s %{fbroot}/bin{-superserver,}
fi
%systemd_post firebird-superserver.service

%postun superserver
%systemd_postun_with_restart firebird-superserver.service

%preun superserver
%systemd_preun firebird-superserver.service


%pre 
# Create the firebird group if it doesn't exist
getent group %{name} || /usr/sbin/groupadd -r %{name} 
getent passwd %{name} >/dev/null || /usr/sbin/useradd -d / -g %{name} -s /bin/nologin -r %{name} 

# Add gds_db to /etc/services if needed
FileName=/etc/services
newLine="gds_db 3050/tcp  # Firebird SQL Database Remote Protocol"
oldLine=`grep "^gds_db" $FileName`
if [ -z "$oldLine" ]; then
 echo $newLine >> $FileName
fi


%post 
/sbin/ldconfig
/bin/systemd-tmpfiles --create  %{_sysconfdir}/tmpfiles.d/firebird.conf

%postun 
/sbin/ldconfig

%files 
%defattr(0644,root,root,0755)
%doc builds/install/misc/IDPLicense.txt
%doc builds/install/misc/IPLicense.txt
%doc doc/README.Fedora
%defattr(0755,root,root,0755)
%dir %{fbroot}
%defattr(0644,root,root,0755)
%dir %attr(0755,root,root) %{_localstatedir}/lib/%{name}
%dir %attr(0770,%{name},%{name}) %{_localstatedir}/lib/%{name}/data
%attr(0660,%{name},%{name}) %{_localstatedir}/lib/%{name}/data/employee.fdb
%dir %{_localstatedir}/log/%{name}
%dir %{fbroot}/intl
%dir %{fbroot}/UDF
%{fbroot}/UDF/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr (0600,%{name},%{name}) %{_localstatedir}/lib/%{name}/system/security2.fdb
%{_localstatedir}/lib/%{name}/system/*.msg
%{_localstatedir}/lib/%{name}/system/help.fdb
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/fbintl.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/aliases.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/firebird.conf
%config(noreplace) %attr (0664,%{name},%{name}) %{_sysconfdir}/%{name}/fbtrace.conf
%{fbroot}/intl/fbintl.conf
%config(noreplace) %attr(0664,%{name},%{name})  %{_localstatedir}/log/%{name}/%{name}.log
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%{_libdir}/libib_util.so
%defattr(0755,root,root,0750)
%{fbroot}/intl/fbintl
%defattr(0755,root,root,0755)
%{_bindir}/*
%{_sbindir}/fbguard
%{_sbindir}/fb_lock_print
%ghost %dir %attr(0775,%{name},%{name}) %{_var}/run/%{name}
%ghost %attr(0644,%{name},%{name}) %{_var}/run/%{name}/fb_guard
%dir %{_sysconfdir}/tmpfiles.d  
%defattr(0644,root,root)
%{_sysconfdir}/tmpfiles.d/firebird.conf  

%files doc
%defattr(0644,root,root,0755)
%doc gen/buildroot-classic%{_defaultdocdir}/%{name}
%doc gen/buildroot-classic%{fbroot}/misc/intl.sql
%doc gen/buildroot-classic%{fbroot}/misc/upgrade
%doc gen/buildroot-classic%{_sysconfdir}/%{name}/README
%doc gen/buildroot-classic%{_sysconfdir}/%{name}/WhatsNew

%files devel
%defattr(0644,root,root,0755)
%dir %{_includedir}/%{name}
%{_includedir}/*.h
%{_includedir}/%{name}/*.h
%{_libdir}/libfb*.so
%{_libdir}/libgds.so

%files filesystem
%defattr(0644,root,root,0755)
%doc doc/README.Fedora
%defattr(0755,root,root,0755)
%dir %{fbroot}


%files libfbclient
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%{_libdir}/libfbclient.so.*
%{_libdir}/libgds.so.0


%files libfbembed
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%{_libdir}/libfbembed.so.*


%files classic
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%{_unitdir}/%{name}-classic*

%files superclassic
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%defattr(0755,root,root,0755)
%{_unitdir}/%{name}-superclassic.service
%{_sbindir}/fb_smp_server

%files classic-common
%dir %{fbroot}/bin-classic
%dir %{fbroot}/plugins-classic
%defattr(0755,root,root,0755)
%{fbroot}/bin-classic/*
%{fbroot}/plugins-classic/*
%{_sbindir}/fb_inet_server


%files superserver
%defattr(0644,root,root,0755)
%doc doc/license/IDPL.txt
%doc doc/license/README.license.usage.txt
%defattr(0644,root,root,0755)
%dir %{fbroot}/bin-superserver
%dir %{fbroot}/plugins-superserver
%defattr(0755,root,root,0755)
%{_unitdir}/%{name}-superserver.service
%{fbroot}/bin-superserver/*
%{fbroot}/plugins-superserver/*.so
%{_sbindir}/fbserver


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.5.2.26539.0-2
- 为 Magic 3.0 重建

* Fri Nov 09 2012 Philippe Makowski <makowski@fedoraproject.org>  2.5.2.26539.0-1
- new upstream (bug fix release)
- added patch from upstream to fix Firebird CORE-3946

* Sat Aug 25 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-4
- Modernize systemd scriptlets (bug #850109)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1.26351.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-2
- rebuild for icu 4.8

* Thu Jan 19 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26351.0-1
- Fix non-fatal POSTIN fix rh #781691
- new upstream

* Fri Jan 06 2012 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26349.0-4
- Rebuild for GCC-4.7

* Mon Nov 28 2011 Philippe Makowski <makowski@fedoraproject.org> 2.5.1.26349.O-3
- Better systemd support fix rh #757624

* Sun Oct 02 2011 Karsten Hopp <karsten@redhat.com> 2.5.1.26349.O-2
- drop ppc64 configure script hack, not required anymore

* Thu Sep 29 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.1.26349.0-1
- new upstream (bug fix release)
- added patch from upstream to fix Firebird CORE-3610

* Thu Sep 22 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-10
- Add support for systemd (rh #737281)

* Fri Apr 22 2011 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-8
- added patch from upstream to fix rh #697313

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 2.5.0.26074.0-7
- rebuild for icu 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0.26074.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Philippe Makowski <makowski[at]fedoraproject.org>  2.5.0.26074.0-5
- services must not be enabled by default

* Tue Jan 25 2011 Karsten Hopp <karsten@redhat.com> 2.5.0.26074.0-4
- firebird got miscompiled on ppc and had an empty libfbclient.so.2.5.0
  bump release and rebuild

* Wed Dec 22 2010 Philippe Makowski <makowski[at]fedoraproject.org>  2.5.0.26074.0-3
- Fix wrong assign file for classic and classic common

* Thu Dec 16 2010 Dan Horák <dan[at]danny.cz>  2.5.0.26074.0-2
- sync the s390(x) utilities list with other arches
- add libatomic_ops-devel as BR: on non-x86 arches

* Sat Dec 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-1
- Fix rh #656587 /var/run mounted as tempfs

* Mon Nov 22 2010 Philippe Makowski <makowski@fedoraproject.org>  2.5.0.26074.0-0
- build with last upstream

* Tue Jun 29 2010 Dan Horák <dan[at]danny.cz>  2.1.3.18185.0-9
- update the s390(x) patch to match upstream

* Fri Jun 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.1.3.18185.0-8
 - conditional BuildRequires libstdc++-static

* Fri Jun 04 2010 Philippe Makowski <makowski@fedoraproject.org>  2.1.3.18185.0-7
- build with last upstream
- Fix rh #563461 with backport mainstream patch CORE-2928


* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> 2.1.3.18185.0-6
- rebuild for icu 4.4

* Sat Sep 05 2009 Karsten Hopp <karsten@redhat.com> 2.1.3.18185.0-5
- fix build on s390x for F-12 mass rebuild (Dan Horák)

* Mon Aug 11 2009  Philippe Makowski <makowski at fedoraproject.org> 2.1.3.18185.0-4
- build it against system edit lib
- set correct setuid for Classic lock manager
- set correct permission for /var/run/firebird

* Wed Aug 05 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.3.18185.0-2
- rename /usr/bin/gstat to /usr/bin/gstat-fb  to avoid conflict with ganglia-gmond (rh #515510)
- remove stupid rm -rf in postun

* Thu Jul 30 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.3.18185.0-1
- Update to 2.1.3.18185
- Fix rh #514463
- Remove doc patch 
- Apply backport initscript patch

* Sat Jul 11 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-11
- change xinetd script (rh #506528)
- add missing library (and header files) for build php4-interbase module (rh #506728)
- update README.fedora
- automatically created user now have /bin/nologin as shell to make things a little more secure

* Tue May 12 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-8
- patch to fix gcc 4.4.0 and icu 4.2 build error

* Tue May 12 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-7
- patch to change lock files location and avoid %%{fbroot} owned by firebird user (rh #500219)
- add README.fedora
- add symlinks in /usr/bin
- change xinetd reload (rh #500219)

* Sat May 02 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-6
- add filesystem-subpackage
- remove common subpackage and use the main instead
- add logrotate config

* Thu Apr 30 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-5
- fix directories owning

* Thu Apr 23 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-4
- major cleaning install process to take care of the two architectures (Classic and Superserver) the right way

* Wed Apr 22 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-3
- fix group creation

* Sun Apr 19 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-2
- fix autogen issue for f11
- patch init script
- fix ppc64 lib destination issue

* Sun Apr 19 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.2.18118.0-1
- backport doc patch
- update to 2.1.2.18118
- cleanup macros
- specifie libdir
- change firebird user login

* Sat Mar 28 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.1.17910.0-5
- Major packaging restructuring
 
* Mon Mar 21 2009  Philippe Makowski <makowski at firebird-fr.eu.org> 2.1.1.17190.0-4
- Create a doc package
- major cleaning to avoid rpmlint errors
- revert to 2.1.1 (last stable build published)

* Mon Mar 09 2009  Jonathan MERCIER <bioinfornatics at gmail.com> 2.1.2.18116.0-3
- Perform %%configure with option --with-system-icu
- Add libicu-devel in BuildRequires
- Use iconv for convert files to UTF-8

* Fri Mar 05 2009  Jonathan MERCIER <bioinfornatics at gmail.com> 2.1.2.18116.0-2
- Update to 2.1.2
- Use %%global instead of %%define
- Change ${SOURCE1} to %%{SOURCE1}
- Change Group Database to Applications/Databases
- Change License IPL to Interbase
- Perform %%configure section's with some module
- Cconvert cyrillic character to UTF-8

* Thu Jul 17 2008 Arkady L. Shane <ashejn@yandex-team.ru> 2.1.1.17910.0-1
- Update to 2.1.1

* Fri Apr 18 2008 Arkady L. Shane <ashejn@yandex-team.ru> 2.1.0.17798.0-1
- Update to 2.1.0

* Thu Sep 27 2007 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.3.12981.1-1
- Update to 2.0.3

* Thu Sep 13 2007 Arkady L. Shane <ashejn@yandex-team.ru> 2.0.1.12855.0-1
- Initial build for Fedora
- cleanup Mandriva spec
