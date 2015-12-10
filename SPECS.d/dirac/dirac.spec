Name:           dirac
Version:        1.0.2
Release:        10%{?dist}
Summary:        Dirac is an open source video codec 
Summary(zh_CN.UTF-8): 一个开源的视频编码

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MPLv1.1
URL:            http://diracvideo.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         dirac-1.0.2-backports.patch
Patch1:         0001-Fix-uninitialised-memory-read-that-causes-the-encode.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cppunit-devel
BuildRequires:  doxygen
BuildRequires:  graphviz-devel
BuildRequires:  tetex-latex
BuildRequires:  tetex
BuildRequires:  dvipdfm

%description
Dirac is an open source video codec. It uses a traditional hybrid video codec
architecture, but with the wavelet transform instead of the usual block 
transforms.  Motion compensation uses overlapped blocks to reduce block 
artefacts that would upset the transform coding stage.

%description -l zh_CN.UTF-8
一个开源的视频编码。

%package libs
Summary:        Libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
This package contains libraries for %{name}.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-libs = %{version}-%{release} 
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package docs
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档

%description docs
This package contains documentation files for %{name}.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q
%patch0 -p0
%patch1 -p1
install -pm 644 README README.Dirac
install -pm 644 util/instrumentation/README README.instrumentation
# fix permission mode for sources.
find doc unit_tests util libdirac_encoder libdirac_byteio -type f -name \* -exec chmod 644 {} \;

#Remove -Werror
sed -i 's/-Werror//g' configure.ac configure


%build
%configure \
  --program-prefix=dirac_ \
  --program-transform-name=s,dirac_dirac_,dirac_, \
  --enable-overlay \
  --disable-static \
%ifarch x86_64 \
  --enable-mmx=yes \
%else \
  --enable-mmx=no \
%endif

# remove rpath from libtool (may be unneeded)
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} 


%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Move doc in docdir macro
mv $RPM_BUILD_ROOT%{_datadir}/doc/dirac __doc

# Transform-name fix
mv $RPM_BUILD_ROOT%{_bindir}/dirac_create_dirac_testfile.pl \
	$RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl
sed -i -e 's|"RGBtoYUV"|"dirac_RGBtoYUV"|g' $RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl
sed -i -e 's|/home/guest/dirac-0.5.0/util/conversion|%{_bindir}|' $RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl


%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README.Dirac TODO
%doc README.instrumentation
%{_bindir}/create_dirac_testfile.pl                   
%{_bindir}/dirac_*                             

%files devel
%defattr(-,root,root,-)
%{_includedir}/dirac/
%{_libdir}/pkgconfig/dirac.pc
%{_libdir}/libdirac_*.so

%files docs
%defattr(-,root,root,-)
%doc __doc/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libdirac_decoder.so.*
%{_libdir}/libdirac_encoder.so.*


%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.0.2-10
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.0.2-9
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.0.2-8
- 为 Magic 3.0 重建

* Fri Feb 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-6
- Backport Fix-uninitialised-memory-read
- Disable -Werror - solve FTBFS with gcc46

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-4
- Backport fix for gcc 4.5.0 - rhbz#660822

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 kwizart < kwizart at gmail.com > - 1.0.2-1
- Update to 1.0.2

* Sun Sep 28 2008 kwizart < kwizart at gmail.com > - 1.0.0-1
- Update to 1.0.0

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10.0-2
- fix conditional comparison

* Sat Jun 21 2008 kwizart < kwizart at gmail.com > - 0.10.0-1
- Update to 0.10.0

* Sat Feb  9 2008 kwizart < kwizart at gmail.com > - 0.9.1-2
- Rebuild for gcc43

* Mon Jan 28 2008 kwizart < kwizart at gmail.com > - 0.9.1-1
- Update to 0.9.1

* Fri Jan  4 2008 kwizart < kwizart at gmail.com > - 0.8.0-3
- Fix gcc43

* Wed Oct 10 2007 kwizart < kwizart at gmail.com > - 0.8.0-2
- Fix perms

* Wed Oct 10 2007 kwizart < kwizart at gmail.com > - 0.8.0-1
- Update to 0.8.0

* Sun Aug 26 2007 kwizart < kwizart at gmail.com > - 0.7.0-2
- Rebuild for BuildID

* Tue Jun 15 2007 kwizart < kwizart at gmail.com > - 0.7.0-1
- Update to 0.7.0

* Sun Mar 25 2007 kwizart < kwizart at gmail.com > - 0.6.0-9.20070325cvs
- Update to cvs 20070325
- Remove -Werror for CXXFLAGS and decoder
- Fix perms and wrongs end of line encoding

* Sun Mar 25 2007 kwizart < kwizart at gmail.com > - 0.6.0-8.20070108cvs
- Fix mmx only for x86_64
- Fix ldconfig libs

* Sat Mar 24 2007 kwizart < kwizart at gmail.com > - 0.6.0-7.20070108cvs
- Cleaned comment
- Enabled dirac-libs for multi-libs
- Enabled mmx on 64 bit
- Fix Perl script create_dirac_testfile.pl

* Sat Jan 20 2007 kwizart < kwizart at gmail.com > - 0.6.0-6.20070108cvs
- Change cvs order in release
- Change package name libdirac -> dirac
- Drop redundant BR
- Move doc in docdir

* Mon Jan  8 2007 kwizart < kwizart at gmail.com > - 0.6.0-5.cvs20070108
- Update to cvs 20070108 because of a dirac-snapshot corrections.
- Disabled encoder qt4-gui 
(no more provided in the rebuilded package - will reenable later if needed!)

* Fri Jan  5 2007 kwizart < kwizart at gmail.com > - 0.6.0-4.cvs20070105
- Update diract-snapshoot.sh
- Update to cvs 20070105
- Remove BR valgrind (is only requires for test-suite)
- Try to Fix compile Flags
- Exclude static seems better
- Tweak the right FLAGs (drop debug and mmx)

* Thu Jan  4 2007 kwizart < kwizart at gmail.com > - 0.6.0-3.cvs20070104
- Fix BR required and found by mock
- Disable static
- Update doxygen -u before generate doc.
- Bootstrap during snapshot

* Thu Jan  4 2007 kwizart < kwizart at gmail.com > - 0.6.0-2.cvs20070104
- Update to Release 0.6.0 with cvs 20070104
- Enable dirac-qt4 gui

* Wed Dec 12 2006 kwizart < kwizart at gmail.com > - 0.6.0-1
- Intitial release.
