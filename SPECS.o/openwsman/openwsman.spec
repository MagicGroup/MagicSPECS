
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

# RubyGems's macros expect gem_name to exist.
%global gem_name %{name}

Name:           openwsman
BuildRequires:  swig
BuildRequires:  libcurl-devel libxml2-devel pam-devel sblim-sfcc-devel
BuildRequires:  python python-devel ruby ruby-devel rubygems-devel perl
BuildRequires:  python python-devel perl
BuildRequires:  perl-devel pkgconfig openssl-devel
#BuildRequires: java-1.8.0-openjdk-devel
BuildRequires:  cmake
BuildRequires:  systemd-units
Version: 2.6.2
Release: 3%{?dist}
Url:            http://www.openwsman.org/
License:        BSD
Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Summary:        Open source Implementation of WS-Management
Summary(zh_CN.UTF-8): WS-Management 的开发源实现 
Source:         https://github.com/Openwsman/openwsman/archive/v%{version}.tar.gz
# help2man generated manpage for openwsmand binary
Source1:        openwsmand.8.gz
# service file for systemd
Source2:        openwsmand.service
# script for testing presence of the certificates in ExecStartPre
Source3:        owsmantestcert.sh
Patch1:         openwsman-2.2.7-libssl.patch
Patch2:         openwsman-2.4.0-pamsetup.patch

%description
Openwsman is a project intended to provide an open-source
implementation of the Web Services Management specipication
(WS-Management) and to expose system management information on the
Linux operating system using the WS-Management protocol. WS-Management
is based on a suite of web services specifications and usage
requirements that exposes a set of operations focused on and covers
all system management aspects.

%description -l zh_CN.UTF-8
Web 服务管理的开源实现。


%package -n libwsman1
License:        BSD
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary:        Open source Implementation of WS-Management
Summary(zh_CN.UTF-8): %{name} 的运行库
Provides:       %{name} = %{version}-%{release}
Obsoletes:      %{name} < %{version}-%{release}

%description -n libwsman1
Openwsman library for packages dependent on openwsman

%description -n libwsman1 -l zh_CN.UTF-8
%{name} 的运行库。

%package -n libwsman-devel
License:        BSD
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary(zh_CN.UTF-8): %{name} 的开发包
Summary:        Open source Implementation of WS-Management
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel < %{version}-%{release}
Requires:       libwsman1 = %{version}-%{release}
Requires:       %{name}-server = %{version}-%{release}
Requires:       %{name}-client = %{version}-%{release}
Requires:       sblim-sfcc-devel libxml2-devel pam-devel
Requires:       libcurl-devel

%description -n libwsman-devel
Development files for openwsman

%description -n libwsman-devel -l zh_CN.UTF-8
%{name} 的开发包。

%package client
License:        BSD
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary:        Openwsman Client libraries
Summary(zh_CN.UTF-8): %{name} 的客户端运行库

%description client
Openwsman Client libraries

%description client -l zh_CN.UTF-8
%{name} 的客户端运行库。

%package server
License:        BSD
Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Requires:       net-tools
Requires(post):       chkconfig
Requires(preun):      chkconfig
Requires(postun):     initscripts
Summary:        Openwsman Server and service libraries
Summary(zh_CN.UTF-8): %{name} 的服务端和服务端运行库
Requires:       libwsman1 = %{version}-%{release}

%description server
Openwsman Server and service libraries

%description server -l zh_CN.UTF-8
%{name} 的服务端和服务端运行库。

%package python
License:        BSD
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Python bindings for openwsman client API
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Requires:       python
Requires:       libwsman1 = %{version}-%{release}

%description python
This package provides Python bindings to access the openwsman client
API.

%description python -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%package -n rubygem-%{gem_name}
License:        BSD
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Ruby client bindings for Openwsman
Summary(zh_CN.UTF-8): %{name} 的 Ruby 客户端绑定
Obsoletes:      %{name}-ruby < %{version}-%{release}

%description -n rubygem-%{gem_name}
The openwsman gem provides a Ruby API to manage systems using
the WS-Management protocol.

%description -n rubygem-%{gem_name} -l zh_CN.UTF-8
%{name} 的 Ruby 客户端绑定。

%package -n rubygem-%{gem_name}-doc
Summary: Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group: Documentation
Group(zh_CN.UTF-8): 文档
Requires: rubygem-%{gem_name} = %{version}-%{release}
BuildArch: noarch

%description -n rubygem-%{gem_name}-doc
Documentation for rubygem-%{gem_name}

%description -n rubygem-%{gem_name}-doc -l zh_CN.UTF-8
%{name} 的文档。

%package java
Requires:      java
Requires:      libwsman1 = %{version}
Summary:       Java bindings for openwsman client API
Summary(zh_CN.UTF-8): openwsman 客户端 API 的 JAVA 绑定
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description java
This package provides Java bindings to access the openwsman client API.

%description java -l zh_CN.UTF-8
openwsman 客户端 API 的 JAVA 绑定。

%package perl
License:        BSD
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Summary:        Perl bindings for openwsman client API
Summary(zh_CN.UTF-8): %{name} 的 Perl 绑定
Requires:       libwsman1 = %{version}-%{release}

%description perl
This package provides Perl bindings to access the openwsman client API.

%description perl -l zh_CN.UTF-8
%{name} 的 Perl 绑定。


%prep
%setup -q
%patch1 -p1 -b .libssl
%patch2 -p1 -b .pamsetup

# Fix wrong symlinks (fixed upstream, will be in 2.4.1)
ln -sf %{_bindir}/rdoc bindings/ruby/rdoc1_9.rb 
ln -sf %{_bindir}/rdoc bindings/ruby/rdoc2_0.rb 

%build
# Removing executable permissions on .c and .h files to fix rpmlint warnings. 
chmod -x src/cpp/WsmanClient.h

rm -rf build
mkdir build

export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DFEDORA -DNO_SSL_CALLBACK"
export SSL_LIB=`readlink %{_libdir}/libssl.so`
export CFLAGS="-D_GNU_SOURCE -fPIE -DPIE"
export LDFLAGS="$LDFLAGS -Wl,-z,now -pie"
cd build
cmake \
  -DCMAKE_INSTALL_PREFIX=/usr \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS -fno-strict-aliasing" \
  -DCMAKE_CXX_FLAGS_RELEASE:STRING="$RPM_OPT_FLAGS" \
  -DCMAKE_SKIP_RPATH=1 \
  -DPACKAGE_ARCHITECTURE=`uname -m` \
  -DLIB=%{_lib} \
   ..

make CFLAGS="-DSSL_LIB='\"$SSL_LIB\"'"

# Make the freshly build openwsman libraries available to build the gem's
# binary extension.
export LIBRARY_PATH=/builddir/build/BUILD/%{name}-%{version}/build/src/lib
export CPATH=/builddir/build/BUILD/%{name}-%{version}/include/
export LD_LIBRARY_PATH=/builddir/build/BUILD/%{name}-%{version}/build/src/lib/

%if 0%{?RUBY}
%gem_install -n ./bindings/ruby/%{name}-%{version}.gem
%endif

%install
cd build

# Do not install the ruby extension, we are proviging the rubygem- instead.
echo -n > bindings/ruby/cmake_install.cmake

make DESTDIR=%{buildroot} install
cd ..
rm -f %{buildroot}/%{_libdir}/*.la
rm -f %{buildroot}/%{_libdir}/openwsman/plugins/*.la
rm -f %{buildroot}/%{_libdir}/openwsman/authenticators/*.la
[ -d %{buildroot}/%{ruby_vendorlibdir} ] && rm -f %{buildroot}/%{ruby_vendorlibdir}/openwsmanplugin.rb
[ -d %{buildroot}/%{ruby_vendorlibdir} ] && rm -f %{buildroot}/%{ruby_vendorlibdir}/openwsman.rb
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 644 etc/openwsman.conf %{buildroot}/%{_sysconfdir}/openwsman
install -m 644 etc/openwsman_client.conf %{buildroot}/%{_sysconfdir}/openwsman
mkdir -p %{buildroot}/%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/openwsmand.service
install -m 644 etc/ssleay.cnf %{buildroot}/%{_sysconfdir}/openwsman
install -p -m 755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/openwsman
# install manpage
mkdir -p %{buildroot}/%{_mandir}/man8/
cp %SOURCE1 %{buildroot}/%{_mandir}/man8/
# install missing headers
install -m 644 include/wsman-xml.h %{buildroot}/%{_includedir}/openwsman
install -m 644 include/wsman-xml-binding.h %{buildroot}/%{_includedir}/openwsman
install -m 644 include/wsman-dispatcher.h %{buildroot}/%{_includedir}/openwsman

%if 0%{?RUBY}
mkdir -p %{buildroot}%{gem_dir}
cp -pa ./build%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

rm -rf %{buildroot}%{gem_instdir}/ext

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./build%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
%endif
magic_rpm_clean.sh

%post -n libwsman1 -p /sbin/ldconfig

%postun -n libwsman1 -p /sbin/ldconfig

%post server
/sbin/ldconfig
%systemd_post openwsmand.service

%preun server
%systemd_preun openwsmand.service

%postun server
rm -f /var/log/wsmand.log
%systemd_postun_with_restart openwsmand.service
/sbin/ldconfig

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig

%files -n libwsman1
%doc AUTHORS COPYING ChangeLog README.md TODO
%{_libdir}/libwsman.so.*
%{_libdir}/libwsman_client.so.*
%{_libdir}/libwsman_curl_client_transport.so.*

%files -n libwsman-devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%doc AUTHORS COPYING ChangeLog README.md

%files python
%{python_sitearch}/*.so
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%doc AUTHORS COPYING ChangeLog README.md

%if 0%{?RUBY}
%files -n rubygem-%{gem_name}
%doc AUTHORS COPYING ChangeLog README.md
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files -n rubygem-%{gem_name}-doc
%doc %{gem_docdir}
%endif

%files java
%defattr(-,root,root)
%{_javadir}/*jar


%files perl
%{perl_vendorarch}/openwsman.so
%{perl_vendorlib}/openwsman.pm
%doc AUTHORS COPYING ChangeLog README.md

%files server
# Don't remove *.so files from the server package.
# the server fails to start without these files.
%dir %{_sysconfdir}/openwsman
%config(noreplace) %{_sysconfdir}/openwsman/openwsman.conf
%config(noreplace) %{_sysconfdir}/openwsman/ssleay.cnf
%attr(0755,root,root) %{_sysconfdir}/openwsman/owsmangencert.sh
%attr(0755,root,root) %{_sysconfdir}/openwsman/owsmantestcert.sh
%config(noreplace) %{_sysconfdir}/pam.d/openwsman
%{_unitdir}/openwsmand.service
%dir %{_libdir}/openwsman
%dir %{_libdir}/openwsman/authenticators
%{_libdir}/openwsman/authenticators/*.so
%{_libdir}/openwsman/authenticators/*.so.*
%dir %{_libdir}/openwsman/plugins
%{_libdir}/openwsman/plugins/*.so
%{_libdir}/openwsman/plugins/*.so.*
%{_sbindir}/openwsmand
%{_libdir}/libwsman_server.so.*
%{_mandir}/man8/*
%doc AUTHORS COPYING ChangeLog README.md

%files client
%{_libdir}/libwsman_clientpp.so.*
%config(noreplace) %{_sysconfdir}/openwsman/openwsman_client.conf
%doc AUTHORS COPYING ChangeLog README.md


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.6.2-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.6.2-2
- 更新到 2.6.2

* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 2.6.1-2
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 2.6.1-1
- 更新到 2.6.1

* Fri Apr 03 2015 Liu Di <liudidi@gmail.com> - 2.4.14-1
- 更新到 2.4.14

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.4.6-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.6-1
- Update to openwsman-2.4.6

* Fri Apr 25 2014 Vít Ondruch <vondruch@redhat.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Mar 11 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.4-1
- Update to openwsman-2.4.4
- Provide rubygem-openwsman instead of openwsman-ruby (patch by Vit Ondruch)

* Wed Feb 05 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.3-2
- Update openwsmand man page

* Thu Jan 23 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.3-1
- Update to openwsman-2.4.3

* Tue Jan 07 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-3
- Start the service using SSL by default

* Mon Sep 30 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-2
- Build with full relro
- Fix provides/requires
- Fix pam.d config (patch by Ales Ledvinka)
  Resolves: #1013018

* Tue Sep 17 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.4.0-1
- Update to openwsman-2.4.0
- Fix bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3.6-7
- Perl 5.18 rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 2.3.6-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 18 2013 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.3.6-4
- Updated the dependency for ruby bindings and introduced the java bindings.

* Wed Mar 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.6-3
- rebuild for ruby 2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.6-1
- Update to openwsman-2.3.6

* Mon Sep 17 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.5-1
- Update to openwsman-2.3.5
- Enable ruby subpackage again

* Tue Aug 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-7
- Fix issues found by fedora-review utility in the spec file

* Thu Aug 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-6
- Use new systemd-rpm macros
  Resolves: #850405

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.3.0-4
- Perl 5.16 rebuild

* Mon May 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-3
- Rename service file

* Wed May 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-2
- Add systemd support

* Tue Mar 27 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.3.0-1
- Update to openwsman-2.3.0

* Thu Feb 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-4
- Fix libssl loading

* Thu Feb 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-3
- Temporarily disable ruby subpackage

* Thu Jan 26 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-2
- Remove unnecessary net-tools requirement
  Resolves: #784787

* Wed Jan 11 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-1
- Update to openwsman-2.2.7

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.5-3
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.5-2
- Perl 5.14 mass rebuild

* Wed Mar 23 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.5-1
- Update to openwsman-2.2.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-2
- Recompile with -DNO_SSL_CALLBACK

* Tue Nov 16 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-1
- Update to openwsman-2.2.4
- Add help2man generated manpage for openwsmand binary
- Add missing openwsman headers to libwsman-devel
- Add configuration file to openwsman-client

* Wed Sep 29 2010 jkeating - 2.2.3-9
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-8
- Move initscript to the right place
- Fix return values from initscript according to guidelines

* Tue Aug 10 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-7
- Moved the certificate generation from init script. The user will have to 
-   generate the certificate manually.

* Mon Aug  2 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-6
- Fixed the version checking of swig and forced all the ruby files to be 
-   installed into site{lib,arch} dirs 

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.2.3-4
- Mass rebuild with perl-5.12.0

* Thu Apr 22 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-3
- authors.patch: Moved all the AUTHORS info to AUTHORS file.
- Corrected the Source tag.
- Corrected the package dependencies to break cyclic dependencies.
- Fixed the default attributes.
- Fixed the preun & postun scripts, to make sure the openwsmand service
-    is stopped before the package is removed.
- Added 'condrestart' function to the init script.
- Had to let the *.so files be part of the openwsman-server becuase
-    some of the source files explicitly call out for *.so files.


* Thu Apr 15 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.3-2
- Updated the spec file to adhere to the upstream standard of breaking
- the package in server, client, lib modules 
- randfile.patch: when openwsmand daemon creates a certificate the
- first time it needs a file which have random content it. This
- is pointed to $HOME/.rnd in /etc/openwsman/ssleay.cnf. Changed this
- random file to /dev/urandom. 
- initscript.patch: patch to edit the init script so that the services
- are not started by default.


* Wed Mar  3 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-1
- Update to openwsman-2.2.3


* Wed Sep 23 2009 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.2.0-1
- Added the new 2.2.0 sources.
- Changed the release and version numbers.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.0-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Matt Domsch <Matt_Domsch@dell.com> - 2.1.0-1
- update to 2.1.0, resolves security issues

* Tue Aug 19 2008  <srinivas_ramanatha@dell.com> - 2.0.0-1%{?dist}
- Modified the spec file to adhere to fedora packaging guidelines.
