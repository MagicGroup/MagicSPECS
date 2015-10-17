Name:           upx
Version:        3.91
Release:        7%{?dist}
Summary:        Ultimate Packer for eXecutables
Summary(zh_CN.UTF-8): 可执行文件压缩程序

Group:          Applications/Archiving
Group(zh_CN.UTF-8): 应用程序/归档
License:        GPLv2+ and Public Domain
URL:            http://upx.sourceforge.net/
Source0:        http://upx.sourceforge.net/download/%{name}-%{version}-src.tar.bz2
#Patch0:		upx-3.03-pefile-strictproto.patch
Patch1:		upx-3.07-use-lzma-sdk-lib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  ucl-devel >= 1.01
BuildRequires:  zlib-devel
BuildRequires:	lzma-sdk-devel

%description
UPX is a free, portable, extendable, high-performance executable
packer for several different executable formats. It achieves an
excellent compression ratio and offers very fast decompression. Your
executables suffer no memory overhead or other drawbacks.

%description -l zh_CN.UTF-8
可执行文件的压缩程序。

%prep
%setup -q -n %{name}-%{version}-src
sed -i -e 's/ -O2/ /' -e 's/ -Werror//' src/Makefile

#%patch0 -p0
%patch1 -p1 -b .use-lib

%build
export CXX="g++"
export CXXFLAGS="$RPM_OPT_FLAGS" # export, not to make so it won't trump all
UPX_LZMA_VERSION=0x465 UPX_LZMADIR=%{_includedir}/lzma465 make %{?_smp_mflags} -C src
make -C doc


%install
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 doc/upx.1   $RPM_BUILD_ROOT%{_mandir}/man1/upx.1
install -Dpm 755 src/upx.out $RPM_BUILD_ROOT%{_bindir}/upx
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc BUGS COPYING LICENSE NEWS PROJECTS README README.1ST THANKS TODO doc/*.txt
%{_bindir}/upx
%{_mandir}/man1/upx.1*


%changelog
* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 3.91-7
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.91-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Oct 16 2014 Jon Ciesla <limburgher@gmail.com> - 3.91-4
- Fix FTBFS.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 28 2013 Jon Ciesla <limburgher@gmail.com> - 3.91-1
- New upstream, BZ 1023719.
- Fix bad changelog date.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Jon Ciesla <limburgher@gmail.com> - 3.09-1
- New upstream.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Jon Ciesla <limburgher@gmail.com> - 3.08-1
- New upstream.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Tom Callaway <spot@fedoraproject.org> - 3.07-3
- use lzma-sdk system library/headers

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Jon Ciesla <limb@jcomserv.net> - 3.07-1
- New upstream.

* Fri Jan 08 2010 Jon Ciesla <limb@jcomserv.net> - 3.04-2
- LZMA fixes by John Reiser (jreiser@bitwagon.com) BZ 501636.

* Mon Nov 16 2009 Jon Ciesla <limb@jcomserv.net> - 3.04-1
- 3.04.
- Stict prototype patch upstreamed.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Jon Ciesla <limb@jcomserv.net> - 3.03-3
- Patch for stricter glibc.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 08 2008 Jon Ciesla <limb@jcomserv.net> - 3.03-1
- 3.03.

* Fri Feb 08 2008 Jon Ciesla <limb@jcomserv.net> - 3.02-2
- GCC 4.3 rebuild.

* Mon Dec 31 2007 Jon Ciesla <limb@jcomserv.net> - 3.02-1
- 3.02.

* Thu Aug 16 2007 Jon Ciesla <limb@jcomserv.net> - 3.01-2
- License tag correction.

* Mon Aug 06 2007 Jon Ciesla <limb@jcomserv.net> - 3.01-1
- 3.01.

* Sun May 13 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.00-1
- 3.00.

* Wed Apr  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 2.03-1
- 2.03.

* Wed Aug 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.02-1
- 2.02.

* Tue May 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.00-2
- BR: zlib-devel.

* Tue May 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.00-1
- 2.00.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.25-5
- Rebuild.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.25-4
- Rebuild.

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.25-3
- rebuilt

* Fri Dec 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-2
- Let rpmbuild take care of stripping binaries.
- Honor build environment settings better.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.25-0.fdr.1
- Update to 1.25.

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.24-0.fdr.3
- Add workaround for building with UCL 1.02, thanks to upstream.

* Sun Nov 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.24-0.fdr.2
- Spec cleanup.

* Sat Jul 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.24-0.fdr.1
- First build.
