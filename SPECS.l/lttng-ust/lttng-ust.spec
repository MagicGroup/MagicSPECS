Name:           lttng-ust
Version:        2.6.2
Release:        3%{?dist}
License:        LGPLv2 and GPLv2 and MIT
Group:          Development/Libraries
Summary:        LTTng Userspace Tracer library
URL:            http://lttng.org
Source0:        http://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2

BuildRequires:  python
BuildRequires:  libuuid-devel texinfo libtool
BuildRequires:  userspace-rcu-devel >= 0.8.0
BuildRequires:  libtool autoconf automake

%description
This library may be used by user space applications to generate 
tracepoints using LTTng.

%package -n %{name}-devel
Summary:        LTTng Userspace Tracer library headers and development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       userspace-rcu-devel

%description -n %{name}-devel
This library provides support for developing programs using 
LTTng userspace tracing

%prep
%setup -q

%build
%ifarch s390 s390x
# workaround rhbz#837572 (ICE in gcc)
%global optflags %(echo %{optflags} | sed 's/-O2/-O1/')
%endif

#Reinitialize libtool with the fedora version to remove Rpath
libtoolize -cvfi
autoreconf -vif
%configure --docdir=%{_docdir}/%{name} --disable-static
# --with-java-jdk
# Java support was disabled in lttng-ust's stable-2.0 branch upstream in
# http://git.lttng.org/?p=lttng-ust.git;a=commit;h=655a0d112540df3001f9823cd3b331b8254eb2aa
# We can revisit enabling this when the next major version is released.

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%{_mandir}/man3/lttng-ust.3.gz
%{_mandir}/man3/lttng-ust-cyg-profile.3.gz
%{_mandir}/man3/lttng-ust-dl.3.gz
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/java-agent.txt


%files -n %{name}-devel
%{_bindir}/lttng-gen-tp
%{_mandir}/man1/lttng-gen-tp.1.gz
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%dir %{_docdir}/%{name}/examples
%{_docdir}/%{name}/examples/*

%changelog
* Sat Nov 21 2015 Liu Di <liudidi@gmail.com> - 2.6.2-3
- 为 Magic 3.0 重建

* Thu Aug 6 2015 Suchakra Sharma <suchakra@fedoraproject.org> - 2.6.2-2
- Remove remaining BR for SystemTap SDT and add python as a BR

* Thu Jul 23 2015 Michael Jeanson <mjeanson@gmail.com> - 2.6.2-1
- New upstream release
- Drop SystemTap SDT support
- Remove patches applied upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec  9 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.1-2
- Add patch to fix aarch64 support

* Mon Nov 03 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.5.1-1
- New upstream release
- Update URL

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.4.1-1
- New upstream bugfix release

* Sat Mar 1 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.4.0-1
- New upstream release
- Add new files (man and doc)

* Sat Feb 22 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-2
- Rebuilt for URCU Soname change

* Fri Sep 20 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-1
- New upstream release (include snapshop feature)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.1-1
- New upstream release
- Bump URCU dependency

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 2.1.2-2
- add build workaround for s390(x)

* Fri May 17 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.2-1
- New upstream bugfix release
- Remove patches applied upstream

* Wed Feb 27 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-2
- Remove dependency of probes on urcu-bp

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.5-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-2
- Add dependency on systemtap-sdt-devel for devel package

* Tue Jun 19 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-1
- New upstream release
- Updates from review comments

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.3-1
- New package, inspired by the one from OpenSuse

