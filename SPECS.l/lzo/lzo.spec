Name:           lzo
Version:	2.08
Release:        1%{?dist}
Summary:        Data compression library with very fast (de)compression
Summary(zh_CN.UTF-8): 非常快速的压缩/解压库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
Patch0:         lzo-2.06-configure.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.

%description -l zh_CN.UTF-8
非常快速的压缩/解压库。解压不需要内存。如果调慢压缩时间可以获得更高
的压缩率，但解压仍然一样的快速。

%package minilzo
Summary:        Mini version of lzo for apps which don't need the full version
Summary(zh_CN.UTF-8): 不需要完全版本的 lzo 的程序使用的迷你版本
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.

%description minilzo -l zh_CN.UTF-8
不需要完全版本的 lzo 的程序使用的迷你版本。

%package devel
Summary:        Development files for the lzo library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-minilzo = %{version}-%{release}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch0 -p1 -z .configure
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%configure --disable-dependency-tracking --disable-static --enable-shared
make %{?_smp_mflags}
# build minilzo too (bz 439979)
gcc %{optflags} -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/lzo

#Remove doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/lzo
magic_rpm_clean.sh

%check
make check test


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post minilzo -p /sbin/ldconfig

%postun minilzo -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING THANKS NEWS
%{_libdir}/liblzo2.so.*

%files minilzo
%defattr(-,root,root,-)
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so


%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 2.08-1
- 更新到 2.08

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.06-2
- 为 Magic 3.0 重建

* Wed Sep 14 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.06-1
- Upgrade to latest upstream
- Apply patch from Nicolas Chauvet

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May  1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.03-1
- New upstream release
- Changed the license to GPLv2+

* Wed Apr  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-5
- Fix configure failure with -Werror-implicit-function-declaration in CFLAGS
- Add a minilzo subpackage which contains a shared version of minilzo, to be
  used by all applications which ship with their own copy of it (bz 439979)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.02-4
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-3
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-2
- FE6 Rebuild

* Wed Jul 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-1
- New upstream release 2.02, soname change!

* Mon Jul 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.08-7
- Taking over as maintainer since Anvil has other priorities
- Add a patch to fix asm detection on i386 (bug 145882, 145893). Thanks to
  Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe> for the initial patch.
- Removed unused build dependency on nasm
- Remove static lib
- Cleanup %%doc a bit

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.08-6.fc5
- Rebuild for new gcc

* Tue Jan 17 2006 Dams <anvil[AT]livna.org> - 1.08-5.fc5
- Bumped release for gcc 4.1 rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.08-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.08-0.fdr.2
- Typo un devel description
- Added post and postun scriptlets
- Added URL in Source0

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.
