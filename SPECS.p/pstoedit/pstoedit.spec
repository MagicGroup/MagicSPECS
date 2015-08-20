Name:           pstoedit
Version:	3.70
Release:	1%{?dist}
Summary:        Translates PostScript and PDF graphics into other vector formats
Summary(zh_CN.UTF-8): 转换 PostScript 和 PDF 图像到其它向量格式

Group:          Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
License:        GPLv2+
URL:            http://www.pstoedit.net/
Source0:        http://downloads.sourceforge.net/pstoedit/pstoedit-%{version}.tar.gz

Requires:       ghostscript
BuildRequires:  gd-devel
BuildRequires:  libpng-devel
BuildRequires:  dos2unix
BuildRequires:  ghostscript
BuildRequires:  plotutils-devel
%ifnarch ia64 mips64el
BuildRequires:  libEMF-devel
%endif

%description
Pstoedit converts PostScript and PDF files to various vector graphic
formats. The resulting files can be edited or imported into various
drawing packages. Pstoedit comes with a large set of integrated format
drivers

%description -l zh_CN.UTF-8
 转换 PostScript 和 PDF 图像到其它向量格式。

%package devel
Summary:        Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       libpng-devel

%description devel
This package contains the header files needed for developing %{name}
applications

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

dos2unix doc/*.htm doc/readme.txt


%build
# Buildling without ImageMagick support, to work around bug 507035
%configure --disable-static --with-emf --without-swf --without-magick

# http://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 doc/pstoedit.1 $RPM_BUILD_ROOT%{_mandir}/man1/
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc copying doc/readme.txt 
%{_datadir}/pstoedit
%{_mandir}/man1/*
%{_bindir}/pstoedit
%{_libdir}/*.so.*
%{_libdir}/pstoedit


%files devel
%doc doc/changelog.htm
%{_includedir}/pstoedit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4


%changelog
* Fri Aug 07 2015 Liu Di <liudidi@gmail.com> - 3.70-1
- 更新到 3.70

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 3.62-2
- rebuild for new GD 2.1.0

* Mon Apr 29 2013 Jiri Popelka <jpopelka@redhat.com> - 3.62-1
- 3.62
- remove autoreconf

* Mon Mar 25 2013 Jiri Popelka <jpopelka@redhat.com> - 3.61-3
- Run autoreconf prior to running configure (#926382)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Jiri Popelka <jpopelka@redhat.com> - 3.61-1
- 3.61

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.60-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Jiri Popelka <jpopelka@redhat.com> - 3.60-2
- Correct source url.

* Mon Aug 29 2011 Jiri Popelka <jpopelka@redhat.com> - 3.60-1
- Update to new upstream 3.60, bugfix release
- Remove Rpath

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.45-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.45-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Denis Leroy <denis@poolshark.org> - 3.45-8
- Fix parallel build (#510281)
- Remove ImageMagick support, to work around bug 507035

* Tue Mar 10 2009 Denis Leroy <denis@poolshark.org> - 3.45-7
- Removed EMF BR for ia64 arch (#489412)
- Rebuild for ImageMagick

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.45-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Denis Leroy <denis@poolshark.org> - 3.45-5
- Added patch for improved asymptote support (#483503)
- Added patch to fix incorrect cpp directive

* Wed Sep 24 2008 Denis Leroy <denis@poolshark.org> - 3.45-4
- Fixed cxxflags patch fuziness issue

* Wed May 14 2008 Denis Leroy <denis@poolshark.org> - 3.45-3
- Rebuild for new ImageMagick

* Sun Feb 17 2008 Denis Leroy <denis@poolshark.org> - 3.45-2
- Added patch for gcc 4.3 rebuild

* Thu Sep 20 2007 Denis Leroy <denis@poolshark.org> - 3.45-1
- Update to new upstream 3.45, bugfix release
- Updated quiet patch for 3.45

* Mon Aug 20 2007 Denis Leroy <denis@poolshark.org> - 3.44-7
- License tag update

* Sun Mar 25 2007 Denis Leroy <denis@poolshark.org> - 3.44-6
- Added patch to add -quiet option

* Wed Nov 22 2006 Denis Leroy <denis@poolshark.org> - 3.44-5
- Added libEMF support

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 3.44-4
- FE6 Rebuild

* Fri Aug 18 2006 Denis Leroy <denis@poolshark.org> - 3.44-3
- Added svg/libplot support

* Thu Jun 15 2006 Denis Leroy <denis@poolshark.org> - 3.44-2
- Added missing Requires and BuildRequires
- Patched configure to prevent CXXFLAGS overwrite

* Thu Jun  8 2006 Denis Leroy <denis@poolshark.org> - 3.44-1
- First version

