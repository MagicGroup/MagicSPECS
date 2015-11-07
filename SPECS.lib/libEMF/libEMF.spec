Summary:	A library for generating Enhanced Metafiles
Summary(zh_CN.UTF-8): 生成增强元文件(emf)的库
Name:		libEMF
Version:	1.0.7
Release:	5%{?dist}
License:	LGPLv2+ and GPLv2+
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:		http://libemf.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/libemf/libemf/%{version}/libEMF-%{version}.tar.gz
BuildRequires:	libstdc++-devel
ExcludeArch:    mips64el

%description
libEMF is a library for generating Enhanced Metafiles on systems which
don't natively support the ECMA-234 Graphics Device Interface
(GDI). The library is intended to be used as a driver for other
graphics programs such as Grace or gnuplot. Therefore, it implements a
very limited subset of the GDI.

%description -l zh_CN.UTF-8
生成增强元文件(emf)的库。

%package devel
Summary:	libEMF header files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
libEMF header files.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure \
	--disable-static \
	--enable-editing

make %{?_smp_mflags}

%install
export CPPROG="cp -p"
make install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libEMF.la
magic_rpm_clean.sh

%check
make check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING COPYING.LIB NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%doc doc/html
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/libEMF

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.0.7-5
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.0.7-4
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 07 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-1
- Update to latest upstream
- Drop all patches (upstreamed)
- Small packaging cleanups

* Mon Nov  5 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.6-2
- Fixes for non-x86 64bit architectures

* Mon Sep 03 2012 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.6-1
- updated to 1.0.6
- updated source URL
- dropped obsolete patch hunks and rebased patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.4-4
- Add support for ARM using definitions from WINE

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 25 2009 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.4-1
- updated to 1.0.4
- updated source URL
- dropped obsolete patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Dan Horak <dan[at]danny.cz> - 1.0.3-9
- add support for s390/s390x

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-7
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-6
- fixed compilation with gcc-4.3

* Mon Dec 03 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-5
- fixed compilation on Alpha platform (patch by Oliver Falk)

* Sat Aug 25 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-4
- rebuild for BuildID
- update license tag

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-3
- remove executable bit from libemf.h

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-2
- added license texts
- preserved timestamps during install
- added %%check section

* Sun Nov 19 2006 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 1.0.3-1
- adapted PLD spec
- enhanced amd64 patch
