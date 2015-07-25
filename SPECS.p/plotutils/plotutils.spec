
Name:      plotutils
Version:   2.6
Release:   11%{?dist}
Summary:   GNU vector and raster graphics utilities and libraries
Summary(zh_CN.UTF-8): GNU 向量和栅格图形的工具和库

Group:     Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
# libxmi is GPLv2+
# rest is GPLv3+
License:   GPLv2+ and GPLv3+
URL:       http://www.gnu.org/software/plotutils/
Source0:   ftp://ftp.gnu.org/gnu/plotutils/plotutils-%{version}.tar.gz
Patch0:    plotutils-2.6-png15.patch
Patch1:    plotutils-aarch64.patch
Patch2:    plotutils-werror-format-security.patch

BuildRequires:   flex
BuildRequires:   libpng-devel
BuildRequires:   xorg-x11-proto-devel
BuildRequires:   libX11-devel
BuildRequires:   libXaw-devel
BuildRequires:   libXt-devel
BuildRequires:   libXext-devel
BuildRequires:   byacc

Requires(post):  /sbin/install-info
Requires(post):  /sbin/ldconfig
Requires(preun): /sbin/install-info

%description
The GNU plotutils package contains software for both programmers and
technical users. Its centerpiece is libplot, a powerful C/C++ function
library for exporting 2-D vector graphics in many file formats, both
vector and raster. It can also do vector graphics animations. Besides
libplot, the package contains command-line programs for plotting
scientific data. Many of them use libplot to export graphics

%description -l zh_CN.UTF-8
GNU 向量和栅格图形的工具和库。

%package devel
Summary:     Headers for developing programs that will use %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:       Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:    %{name} = %{version}-%{release}


%description devel
This package contains the header files needed for developing %{name}
applications

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -b .png15
%patch1 -p1 -b .aarch64
%patch2 -p1 -b .format-security

%build
%configure --disable-static --enable-libplotter --enable-libxmi --enable-ps-fonts-in-pcl

# fix rpath handling
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf docs-to-include
make install DESTDIR=$RPM_BUILD_ROOT
mkdir docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/ode docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/pic2plot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/libplot docs-to-include
mv ${RPM_BUILD_ROOT}%{_datadir}/tek2plot docs-to-include
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
magic_rpm_clean.sh

%post
/sbin/install-info %{_infodir}/libxmi.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/plotutils.info %{_infodir}/dir || :
/sbin/ldconfig


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libxmi.info %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/plotutils.info %{_infodir}/dir || :
fi


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc AUTHORS COMPAT COPYING NEWS THANKS README PROBLEMS KNOWN_BUGS
%doc docs-to-include/*
%{_bindir}/graph
%{_bindir}/ode
%{_bindir}/double
%{_bindir}/plot
%{_bindir}/pic2plot
%{_bindir}/plotfont
%{_bindir}/spline
%{_bindir}/tek2plot
%{_bindir}/hersheydemo
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_infodir}/*.info*


%files devel
%defattr(-, root, root, -)
%doc TODO
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Fri Jul 24 2015 Liu Di <liudidi@gmail.com> - 2.6-11
- 为 Magic 3.0 重建

* Wed Dec 04 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-10
- Fix FTBFS when "-Werror=format-security" is used

* Tue Nov 26 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-9
- Apply aarch64 support patch (#926356)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-6
- Fix license tag (upstream relicensed in version 2.5.1)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 22 2012 Tom Callaway <spot@fedoraproject.org> - 2.6-4
- fix build against libpng15

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.6-2
- Rebuild for new libpng

* Wed Mar  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.6-1
- Update to 2.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5-5
- Autorebuild for GCC 4.3

* Mon Aug 20 2007 Denis Leroy <denis@poolshark.org> - 2.5-4
- License tag update

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.5-3
- FE6 Rebuild

* Thu Aug 10 2006 Denis Leroy <denis@poolshark.org> - 2.5-2
- Some reformatting, added ldconfig Req

* Wed Aug  9 2006 Denis Leroy <denis@poolshark.org> - 2.5-1
- Initial version
