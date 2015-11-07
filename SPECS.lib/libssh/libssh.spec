Name:           libssh
Version: 0.7.2
Release: 2%{?dist}
Summary:        A library implementing the SSH protocol
Summary(zh_CN.UTF-8): 实现 SSH 协议的库
License:        LGPLv2+
URL:            http://www.libssh.org
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        https://red.libssh.org/attachments/download/87/libssh-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
The ssh library was designed to be used by programmers needing a working SSH
implementation by the mean of a library. The complete control of the client is
made by the programmer. With libssh, you can remotely execute programs, transfer
files, use a secure and transparent tunnel for your remote programs. With its
Secure FTP implementation, you can play with remote files easily, without
third-party programs others than libcrypto (from openssl).

%description -l zh_CN.UTF-8
实现 SSH 协议的库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
# Remove examples, they are not packaged and do not build on EPEL 5
sed -i -e 's|add_subdirectory(examples)||g' CMakeLists.txt
rm -rf examples

%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj

%cmake \
    %{_builddir}/%{name}-%{version}
make %{?_smp_mflags} VERBOSE=1
make doc

popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS BSD ChangeLog COPYING README
%{_libdir}/libssh.so.*
%{_libdir}/libssh_threads.so.*

%files devel
%doc obj/doc/html
%{_includedir}/libssh/callbacks.h
%{_includedir}/libssh/legacy.h
%{_includedir}/libssh/libssh.h
%{_includedir}/libssh/server.h
%{_includedir}/libssh/sftp.h
%{_includedir}/libssh/ssh2.h
%{_libdir}/cmake/libssh-config-version.cmake
%{_libdir}/cmake/libssh-config.cmake
%{_libdir}/pkgconfig/libssh.pc
%{_libdir}/pkgconfig/libssh_threads.pc
%{_libdir}/libssh.so
%{_libdir}/libssh_threads.so

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 0.7.2-2
- 更新到 0.7.2

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 0.6.3-1
- 更新到 0.6.3

* Mon Feb 10 2014 - Andreas Schneider <asn@redhat.com> - 0.6.1-1
- Update to version 0.6.1.
- resolves: #1056757 - Fix scp mode.
- resolves: #1053305 - Fix known_hosts heuristic.

* Wed Jan 08 2014 - Andreas Schneider <asn@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Fri Jul 26 2013 - Andreas Schneider <asn@redhat.com> - 0.5.5-1
- Update to 0.5.5.
- Clenup the spec file.

* Thu Jul 18 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-5
- Add EPEL 5 support.
- Add Debian patches to enable Doxygen documentation.

* Tue Jul 16 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-4
- Add patch for #982685.

* Mon Jun 10 2013 Simone Caronni <negativo17@gmail.com> - 0.5.4-3
- Clean up SPEC file and fix rpmlint complaints.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Petr Lautrbach <plautrba@redhat.com> 0.5.4-1
- update to security 0.5.4 release
- CVE-2013-0176 (#894407)

* Tue Nov 20 2012 Petr Lautrbach <plautrba@redhat.com> 0.5.3-1
- update to security 0.5.3 release (#878465)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Petr Lautrbach <plautrba@redhat.com> 0.5.2-1
- update to 0.5.2 version (#730270)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun  1 2011 Jan F. Chadima <jchadima@redhat.com> - 0.5.0-1
- bounce versionn to 0.5.0 (#709785)
- the support for protocol v1 is disabled

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Jan F. Chadima <jchadima@redhat.com> - 0.4.8-1
- bounce versionn to 0.4.8 (#670456)

* Mon Sep  6 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.6-1
- bounce versionn to 0.4.6 (#630602)

* Thu Jun  3 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.4-1
- bounce versionn to 0.4.4 (#598592)

* Wed May 19 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.3-1
- bounce versionn to 0.4.3 (#593288)

* Tue Mar 16 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.2-1
- bounce versionn to 0.4.2 (#573972)

* Tue Feb 16 2010 Jan F. Chadima <jchadima@redhat.com> - 0.4.1-1
- bounce versionn to 0.4.1 (#565870)

* Fri Dec 11 2009 Jan F. Chadima <jchadima@redhat.com> - 0.4.0-1
- bounce versionn to 0.4.0 (#541010)

* Thu Nov 26 2009 Jan F. Chadima <jchadima@redhat.com> - 0.3.92-2
- typo in spec file

* Thu Nov 26 2009 Jan F. Chadima <jchadima@redhat.com> - 0.3.92-1
- bounce versionn to 0.3.92 (0.4 beta2) (#541010)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.2-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Jan F. Chadima <jchadima@redhat.com> - 0.2-2
- Small changes during review

* Mon Jun 01 2009 Jan F. Chadima <jchadima@redhat.com> - 0.2-1
- Initial build

