Name:		wavpack
Summary:	A completely open audiocodec
Summary(zh_CN.UTF-8): 完全开放的音频编码
Version:	4.75.2
Release:	3%{?dist}
License:	BSD
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Url:		http://www.wavpack.com/
Source:		http://www.wavpack.com/%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
WavPack is a completely open audio compression format providing lossless,
high-quality lossy, and a unique hybrid compression mode. Although the
technology is loosely based on previous versions of WavPack, the new
version 4 format has been designed from the ground up to offer unparalleled
performance and functionality.

%description -l zh_CN.UTF-8
这是一个完全开放的无损音频压缩格式。

%package devel
Summary:	WavPack - development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
Files needed for developing apps using wavpack

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/libwavpack.so.*
%{_mandir}/man1/wavpack.1*
%{_mandir}/man1/wvgain.1*
%{_mandir}/man1/wvunpack.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libwavpack.so
%doc ChangeLog README doc/*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 4.75.2-3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 4.75.2-2
- 为 Magic 3.0 重建

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 4.75.2-1
- 更新到 4.75.2

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 4.60.1-4
- 为 Magic 3.0 重建

* Wed Feb 22 2012 Liu Di <liudidi@gmail.com> - 4.60.1-3
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.60.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Peter Lemenkov <lemenkov@gmail.com> 4.60.1-1
- Version 4.60.1 (bugfix release)
- Added man-pages
- The only patch was rebased
- Small cosmetic spec-file cleanups

* Mon Sep 28 2009 Peter Lemenkov <lemenkov@gmail.com> 4.60-1
- Version 4.60

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.50.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.50.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 30 2008 Peter Lemenkov <lemenkov@gmail.com> 4.50.1-2
- Fixes to meet the Fedora Packaging Guidelines

* Sun Aug 24 2008 Peter Lemenkov <lemenkov@gmail.com> 4.50.1-1
- Version 4.50.1

* Wed Jun 18 2008 Peter Lemenkov <lemenkov@gmail.com> 4.50-1
- Version 4.50

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.41-2
- Autorebuild for GCC 4.3

* Sat May 12 2007 Peter Lemenkov <lemenkov@gmail.com> 4.41-1
- Version 4.41
- Removed unnecessary --with-pic

* Fri Dec 15 2006 Peter Lemenkov <lemenkov@gmail.com> 4.40-1.1
- Rebuild

* Fri Dec 15 2006 Peter Lemenkov <lemenkov@gmail.com> 4.40-1
- Version 4.40

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 4.32-3%{?dist}
- Rebuild for FC6

* Sat Jul 01 2006 Peter Lemenkov <lemenkov@newmail.ru> 4.32-2%{?dist}
- force PIC-only code

* Wed Jun 28 2006 Peter Lemenkov <lemenkov@newmail.ru> 4.32-1%{?dist}
- Version 4.32

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> 4.31-2%{?dist}
- rebuild

* Sat Jan 07 2006 Peter Lemenkov <lemenkov@newmail.ru> 4.31-1
- Fixed several issues with wavpack.pc.in
- Cosmetic fixes.
- Version 4.31

* Sun Nov 13 2005 Peter Lemenkov <lemenkov@newmail.ru> 4.3-1
- Initial build for FC-Extras
- Version 4.3

