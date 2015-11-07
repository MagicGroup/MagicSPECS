Summary:	The NetBSD Editline library
Summary(zh_CN.UTF-8): NetBSD 行编辑库
Name:		libedit
Version: 3.1.20150325
Release:	2%{?dist}
License:	BSD
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://www.thrysoee.dk/editline/
%define snap %(echo %{version} | awk -F. '{print $3}')
%define ver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:	http://www.thrysoee.dk/editline/%{name}-%{snap}-%{ver}.tar.gz

BuildRequires:	ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD Editline library.
It provides generic line editing, history, and tokenization functions, similar
to those found in GNU Readline.

%description -l zh_CN.UTF-8
NetBSD 行编辑库。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	ncurses-devel

%description devel
This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-%{snap}-%{ver}

# Suppress rpmlint error.
iconv -f ISO8859-1 -t UTF-8 -o ChangeLog.utf-8 ChangeLog
touch -r ChangeLog ChangeLog.utf-8
mv -f ChangeLog.utf-8 ChangeLog

%build
%configure --disable-static --enable-widec

# Fix unused direct shared library dependencies.
sed -i "s/lcurses/ltinfo/" src/Makefile

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING THANKS
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc examples/fileman.c examples/tc1.c examples/wtc1.c
%doc %{_mandir}/man3/*
%doc %{_mandir}/man5/editrc.5*
%{_includedir}/histedit.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%dir %{_includedir}/editline
%{_includedir}/editline/readline.h

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 3.1.20150325-2
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 3.1.20150325-1
- 更新到 3.1.20150325

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 3.1.20140620-1
- 更新到 3.1.20140620

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.0-6.20110802cvs
- 为 Magic 3.0 重建

* Fri Nov 18 2011 Kamil Dudka <kdudka@redhat.com> - 3.0-5.20110802cvs
- fix code defects found by Coverity

* Wed Nov  9 2011 Adam Williamson <awilliam@redhat.com> 3.0-4.20110802cvs
- rebuild to keep it 'newer' than the f15 and f16 builds

* Fri Aug 26 2011 Kamil Dudka <kdudka@redhat.com> 3.0-3.20110802cvs
- Update to 3.0 (20110802 snap), fixes #732989

* Thu Mar 24 2011 Jerry James <loganjerry@gmail.com> - 3.0-3.20110227cvs
- Update to 3.0 (20110227 snap)
- Drop upstreamed -sigwinch patch
- Preserve ChangeLog timestamp when converting to UTF-8
- Fix "unused direct shared library dependency" warning from rpmlint
- Don't BR gawk; it is on the exceptions list

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.20100424cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jerry James <loganjerry@gmail.com> - 3.0-2.20100424cvs
- Update to 3.0 (20100424 snap)
- Enable wide-character (Unicode) support

* Tue Mar 30 2010 Kamil Dudka <kdudka@redhat.com> 3.0-2.20090923cvs
- eliminated compile-time warnings
- fix to not break the read loop on SIGWINCH, patch contributed
  by Edward Sheldrake (#575383)

* Tue Nov 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> 3.0-1.20090923cvs
- Update to 3.0 (20090923 snap)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-4.20080712cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3.20080712cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.11-2.20080712cvs
- Add ncurses-devel requires to -devel subpackage (BZ#481252)

* Sun Jul 28 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.11-1.20080712cvs
- Version bump to 20080712-2.11.

* Sat Feb 16 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.10-4.20070831cvs
- Rebuilding with gcc-4.3 in Rawhide.

* Sun Nov 04 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-3.20070831cvs
- Removed 'Requires: ncurses-devel'.

* Sat Nov 03 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-2.20070831cvs
- Changed character encoding of ChangeLog from ISO8859-1 to UTF-8.

* Sun Sep 03 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.10-1.20070831cvs
- Initial build. Imported SPEC from Rawhide.
