Summary: SGML and XML parser
Summary(zh_CN.UTF-8): SGML和XML解析器
Name: opensp
Version: 1.5.2
Release: 9%{?dist}
Requires: sgml-common >= 0.5
URL: http://openjade.sourceforge.net/
Source: http://download.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
Patch0: opensp-multilib.patch
License: Distributable
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: xmlto, jadetex

%description
OpenSP is an implementation of the ISO/IEC 8879:1986 standard SGML
(Standard Generalized Markup Language). OpenSP is based on James
Clark's SP implementation of SGML. OpenSP is a command-line
application and a set of components, including a generic API.

%description -l zh_CN.UTF-8
OpenSP是ISO/IEC 8879:1986 标准SGML(标准通用标注语言)的实现。
OpenSP基于James Clark的SGML的SP实现。OpenSP是一个命令行应用
程序和一个组件集合，包括一个通用的API。

%package devel
Summary: Files for developing applications that use OpenSP
Summary(zh_CN.UTF-8): 使用OpenSP开发应用程序需要的文件
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
Header files and libtool library for developing applications that use OpenSP.

%description devel -l zh_CN.UTF-8
使用OpenSP开发应用程序所需要的头文件和libtool库。

%prep
%setup -q -n OpenSP-%{version}
%patch0 -p1 -b .multilib

%build
%configure --disable-dependency-tracking --disable-static --enable-http \
 --enable-default-catalog=%{_sysconfdir}/sgml/catalog \
 --enable-default-search-path=%{_datadir}/sgml:%{_datadir}/xml
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Fix up libtool libraries
find $RPM_BUILD_ROOT -name '*.la' | \
  xargs perl -p -i -e "s|-L$RPM_BUILD_DIR[\w/.-]*||g"

# oMy, othis ois osilly.
for file in nsgmls sgmlnorm spam spent sx ; do
   ln -s o$file $RPM_BUILD_ROOT%{_bindir}/$file
   echo ".so man1/o${file}.1" > $RPM_BUILD_ROOT%{_mandir}/man1/${file}.1
done

#
# Rename sx to sgml2xml.
mv $RPM_BUILD_ROOT%{_bindir}/sx $RPM_BUILD_ROOT%{_bindir}/sgml2xml
mv $RPM_BUILD_ROOT%{_mandir}/man1/{sx,sgml2xml}.1

#
# Clean out (installed) redundant copies of the docs and DTDs.
rm -rf $RPM_BUILD_ROOT%{_docdir}/OpenSP
rm -rf $RPM_BUILD_ROOT%{_datadir}/OpenSP

magic_rpm_clean.sh
#%find_lang sp5


%check
make check || : # failures as of 1.5.2pre1 :(


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
#%files -f sp5.lang
%defattr(-,root,root)
%doc doc/*.htm
%doc docsrc/releasenotes.html
%doc AUTHORS BUGS COPYING ChangeLog NEWS README
%doc pubtext/opensp-implied.dcl
%{_bindir}/*
%{_libdir}/libosp.so.*
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root)
%{_includedir}/OpenSP/
%{_libdir}/libosp.so
%{_libdir}/libosp.la


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.5.2-9
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.5.2-8
- 为 Magic 3.0 重建

* Thu Apr 02 2015 Liu Di <liudidi@gmail.com> - 1.5.2-7
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.5.2-6
- 为 Magic 3.0 重建

* Fri Jan 20 2012 Liu Di <liudidi@gmail.com> - 1.5.2-5
- 为 Magic 3.0 重建

* Fri Oct 06 2006 Liu Di <liudidi@gmail.com> - 1.5.2-1mgc
- rebuild for MagicLinux

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-3.1
- rebuild

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1.5.2-3
- Fixed multilib fix (bug #194702).

* Fri May 26 2006 Tim Waugh <twaugh@redhat.com> 1.5.2-2
- Fixed multilib devel conflicts (bug #192741).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com>  1.5.2-1
- 1.5.2.

* Tue Dec 14 2005 Tim Waugh <twaugh@redhat.com>  1.5.1-2
- Backported patch from 1.5.2pre1 to fix ArcEngine crash.

* Tue Dec 13 2005 Tim Waugh <twaugh@redhat.com>  1.5.1-1
- Back down to 1.5.1 for now.
- Fixes for GCC4.1.

* Sun Dec  4 2005 Ville Skytt盲 <ville.skytta at iki.fi> - 1.5.2-0.1.pre1
- Fix build dependencies.
- Require exact version of main package in -devel.
- Build with dependency tracking disabled.
- Add %%{_datadir}/xml to default search path.
- Run test suite during build.
- Add URL tag.
magic_rpm_clean.sh
- Use %%find_lang.
- Cosmetic improvements.

* Tue Nov 29 2005 Terje Bless <link@pobox.com> 1.5.2-0.pre1
- New package OpenSP.

