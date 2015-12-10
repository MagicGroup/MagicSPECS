%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           lcms
Version:        1.19
Release:        10%{?dist}
Summary:        Color Management System
Summary(zh_CN.UTF-8): 颜色管理系统

Group:          Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
License:        MIT
URL:            http://www.littlecms.com/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         lcms-1.19-rhbz675186.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  swig >= 1.3.12
BuildRequires:  zlib-devel


Provides:       littlecms = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form.

%description -l zh_CN.UTF-8
颜色管理系统。

%package        libs
Summary:        Library for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Introduced in F-9 to solve multilib transition
Obsoletes:      lcms < 1.17-3

%description    libs
The %{name}-libs package contains library for %{name}.

%description libs -l zh_CN.UTF-8 
%{name} 的运行库。

%package     -n python-%{name}
Summary:        Python interface to LittleCMS
Summary(zh_CN.UTF-8): %{name} 的 Python 接口
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       python
Provides:       python-littlecms = %{version}-%{release}

%description -n python-%{name}
Python interface to LittleCMS.

%description -n python-%{name} -l zh_CN.UTF-8
%{name} 的 Python 接口。

%package        devel
Summary:        Development files for LittleCMS
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        static
Summary:        Static files for LittleCMS
Summary(zh_CN.UTF-8): %{name} 的静态库
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-devel = %{version}-%{release}
Requires:       pkgconfig
Provides:       littlecms-static = %{version}-%{release}

%description    static
Development files for LittleCMS.

%description static -l zh_CN.UTF-8
%{name} 的静态库。

%prep
%setup -q
pushd samples
%patch0 -p0
popd

find . -name \*.[ch] | xargs chmod -x
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT

# Convert not UTF-8 files
pushd doc
mkdir -p __temp
for f in LCMSAPI.TXT TUTORIAL.TXT ;do
cp -p $f __temp/$f
iconv -f ISO-8859-1 -t UTF-8 __temp/$f > $f
touch -r __temp/$f $f
done
rm -rf __temp
popd


%build
%configure --with-python --enable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

(cd python; ./swig_lcms)

make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf ${RPM_BUILD_ROOT}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README.1ST doc/TUTORIAL.TXT
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/LCMSAPI.TXT
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a
%{python_sitearch}/_lcms.a

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so


%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.19-10
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.19-9
- 为 Magic 3.0 重建

* Thu Nov  8 2012 Tomas Bzatek <tbzatek@redhat.com> - 1.19-7
- Fix source URL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.19-4
- Fix rhbz#675186

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov 30 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.19-1
- Update to 1.19

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 22 2009 kwizart < kwizart at gmail.com > - 1.18-2
- Add lcms-CVE-2009-0793.patch from 1.18a

* Mon Mar 23 2009 kwizart < kwizart at gmail.com > - 1.18-1
- Update to 1.18 (final)
- Remove upstreamed patches
- Disable autoreconf - patch libtool to prevent rpath issue

* Fri Mar 20 2009 kwizart < kwizart at gmail.com > - 1.18-0.1.beta2
- Update to 1.18beta2
 fix bug #487508: CVE-2009-0723 LittleCms integer overflow
 fix bug #487512: CVE-2009-0733 LittleCms lack of upper-bounds check on sizes
 fix bug #487509: CVE-2009-0581 LittleCms memory leak

* Mon Mar  2 2009 kwizart < kwizart at gmail.com > - 1.17-10
- Fix circle dependency #452352

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 kwizart < kwizart at gmail.com > - 1.17-8
- Fix autoreconf and missing auxiliary files.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.17-7
- Rebuild for Python 2.6

* Tue Oct 28 2008 kwizart < kwizart at gmail.com > - 1.17-6
- Add lcms-fix_s390_lcms_h.patch - Fix #468245

* Tue Jun 3 2008 kwizart < kwizart at gmail.com > - 1.17-5
- Fix Array indexing error in ReadCurve - #448066

* Wed Feb 13 2008 kwizart < kwizart at gmail.com > - 1.17-4
- Fix packaging bug #432568 (multilib transition).

* Mon Feb 11 2008 kwizart < kwizart at gmail.com > - 1.17-3
- Rebuild for gcc 4.3
- Move libs to mutlilibs
- Prevent timestramps change
- Convert files-not-utf8

* Wed Aug 22 2007 kwizart < kwizart at gmail.com > - 1.17-2
- Disable static for now.

* Tue Aug 21 2007 kwizart < kwizart at gmail.com > - 1.17-1
- Update to 1.17
- Ship -static for static linking

* Thu Feb  8 2007 Alexander Larsson <alexl@redhat.com> - 1.16-3.fc7
- Remove requirement on python_sitearch dir (#225981)
- Don't ship with executable .c/.h files

* Mon Feb  5 2007 Alexander Larsson <alexl@redhat.com> - 1.16-2
- Run swig during build to fix warnings in generated code
- Fix build on 64bit

* Mon Feb  5 2007 Alexander Larsson <alexl@redhat.com> - 1.16-1
- Update to 1.16
- Specfile cleanups (#225981)
- Remove static libs

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.15-2
- rebuild against python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.15-1.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.15-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.15-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 1.15-1
- Move from extras to core, update to 1.15

* Sun May 22 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.14-3
- Fix FC4 build (#114146).

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu May 20 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.14-1
- Update to 1.14.

* Thu May 20 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.13-0.fdr.1
- Updated to 1.13.

* Mon Feb 16 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.12-0.fdr.2
- Spec patch from Ville Skyttä.
- New sub-package: python-lcms.

* Sun Dec 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.12-0.fdr.1
- Updated to 1.12.
- BuildReq swig >=1.3.12.

* Sun Nov 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.11-0.fdr.3
- Fixed doc attributes.

* Sat Oct 11 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.11-0.fdr.2
- Renamed to lcms to match upstream.
- Provides: littlecms.
- Fixed doc attributes.
- Excluding empty dir %%{_libdir}/python2.2/

* Thu Oct 09 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:1.11-0.fdr.1
- Initial RPM release.
