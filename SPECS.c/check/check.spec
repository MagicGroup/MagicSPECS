Name:           check
Version: 0.9.12
Release:        7%{?dist}
Summary:        A unit test framework for C
Summary(zh_CN.UTF-8): C 语言的单元测试框架
Source0:        http://downloads.sourceforge.net/check/%{name}-%{version}.tar.gz
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        LGPLv2+
URL:            http://check.sourceforge.net/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
Check is a unit test framework for C. It features a simple interface for 
defining unit tests, putting little in the way of the developer. Tests 
are run in a separate address space, so Check can catch both assertion 
failures and code errors that cause segmentation faults or other signals. 
The output from unit tests can be used within source code editors and IDEs.

%description -l zh_CN.UTF-8
C 语言的单元测试框架。

%package devel
Summary:        Libraries and headers for developing programs with check
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and headers for developing programs with check

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package static
Summary:        Static libraries of check
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description static
Static libraries of check.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q

%build
%configure CFLAGS="${RPM_OPT_FLAGS} -fPIC"
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
if [ -e %{_infodir}/%{name}.info* ]; then
  /sbin/install-info \
    --entry='* Check: (check).               A unit testing framework for C.' \
    %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun -p /usr/sbin/ldconfig

%preun
if [ $1 = 0 -a -e %{_infodir}/%{name}.info* ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LESSER ChangeLog ChangeLogOld NEWS README SVNChangeLog
%doc THANKS TODO
%{_libdir}/libcheck.so.*
%{_infodir}/check*
%{_bindir}/checkmk

%files devel
%defattr(-,root,root,-)
%doc doc/example
%{_includedir}/check.h
%{_libdir}/libcheck.so
%{_libdir}/pkgconfig/check.pc
%{_datadir}/aclocal/check.m4
%{_includedir}/check_stdint.h
%{_mandir}/man1/checkmk.1.gz

#check used to be static only, hence this.
%files static
%defattr(-,root,root,-)
%doc COPYING.LESSER
%{_libdir}/libcheck.a

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 0.9.12-7
- 为 Magic 3.0 重建

* Sun Mar 09 2014 Liu Di <liudidi@gmail.com> - 0.9.12-6
- 更新到 0.9.12

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.9.8-6
- 为 Magic 3.0 重建

* Fri Jul 27 2012 Liu Di <liudidi@gmail.com> - 0.9.8-5
- 为 Magic 3.0 重建

* Mon Feb 14 2011 Jerry James <loganjerry@gmail.com> - 0.9.8-3
- Rebuild for new gcc (Fedora 15 mass rebuild)

* Mon Nov 29 2010 Jerry James <loganjerry@gmail.com> - 0.9.8-2
- Add license file to -static package.
- Remove BuildRoot tag.

* Mon Sep 28 2009 Jerry James <loganjerry@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Thu Aug  6 2009 Jerry James <loganjerry@gmail.com> - 0.9.6-5
- Support --excludedocs (bz 515933)
- Replace broken upstream info dir entry

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr  7 2009 Jerry James <loganjerry@gmail.com> - 0.9.6-3
- Add check-0.9.6-strdup.patch

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9.6-1
- update to 0.9.6

* Mon Dec  1 2008 Jerry James <loganjerry@gmail.com> - 0.9.5-3
- Fix unowned directory (bz 473635)
- Drop unnecessary BuildRequires
- Replace patches with addition of -fPIC to CFLAGS in the spec file
- Add some more documentation files

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-2.1
- Autorebuild for GCC 4.3

* Thu Aug  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.5-1
- 0.9.5 bump

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 0.9.3-5
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.3-4.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.3-4.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Warren Togami <wtogami@redhat.com> 0.9.2-4
- import into FC5 for gstreamer-0.10

* Fri Dec  2 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.2-3
- enabled -fPIC to resolve bz 174313

* Sat Sep 17 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.2-2
- get rid of the so file (not needed)
- only make devel package

* Sun Aug 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.2-1
- initial package for Fedora Extras
