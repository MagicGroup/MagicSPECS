Name:           qca2
Version:	2.1.0
Release:	1%{?dist}

Summary:        Qt Cryptographic Architecture
Summary(zh_CN.UTF-8): Qt 加密算法库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://delta.affinix.com/qca
Source0:        http://delta.affinix.com/download/qca/2.0/qca-%{version}.tar.bz2
# Allow gcc to compile qca
Patch0:         qca-2.0.3-gcc47.patch

BuildRequires:  qt4-devel

%description
Taking a hint from the similarly-named Java Cryptography Architecture,
QCA aims to provide a straightforward and cross-platform crypto API,
using Qt datatypes and conventions. QCA separates the API from the
implementation, using plugins known as Providers. The advantage of this
model is to allow applications to avoid linking to or explicitly depending
on any particular cryptographic library. This allows one to easily change
or upgrade crypto implementations without even needing to recompile the
application!

%description -l zh_CN.UTF-8
Qt 加密算法库。

%package        devel
Summary:        Qt Cryptographic Architecture development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This packages contains the development files for QCA

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n qca-%{version}
%patch0 -p1

%build
unset QTDIR
./configure \
  --prefix=%{_prefix} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --datadir=%{_datadir} \
  --no-separate-debug-info \
  --verbose

sed -i -e /strip/d Makefile
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_bindir}/qcatool2
%{_libdir}/*.so.*
%{_mandir}/*/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/QtCrypto
%{_libdir}/*.so
%{_libdir}/pkgconfig/qca2.pc
%{_libdir}/libqca.prl
%{_libdir}/qt4/mkspecs/features/crypto.prf


%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 2.1.0-1
- 更新到 2.1.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 07 2012 Sven Lankes <sven@lank.es> - 2.0.3-3
- Fix build with gcc 4.7.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Sven Lankes <sven@lank.es> - 2.0.3-1
- new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 05 2009 Sven Lankes <sven@lank.es> - 2.0.2-1
- new upstream release - qt 4.5-compat-fixes

* Wed Apr 08 2009 Sven Lankes <sven@lank.es> - 2.0.1-1
- new upstream release
- removed 64bit patch - now upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 30 2008 Dennis Gilmore <dennis@ausil.us> - 2.0.0-3
- crypto.prf is in libdir not datadir

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.0-2
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-1
- version 2.0.0 final

* Sun Oct 21 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.4.beta7
- fix build on x86_64

* Sun Oct 21 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.3.beta7
- missing BR: openssl

* Thu Sep 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.2.beta7
- review from bug 289681 (thanks Rex)

* Sun Sep 09 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.0.0-0.1.beta7
- initial package 
