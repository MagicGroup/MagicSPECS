Name:          oath-toolkit
Version: 2.6.1
Release: 2%{?dist}
License:       GPLv3+
Group:         System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary:       One-time password components
Summary(zh_CN.UTF-8): 一次性密码组件
BuildRequires: xmlsec1-devel, pam-devel, gtk-doc, libtool, libtool-ltdl-devel
Source:        http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:           http://www.nongnu.org/oath-toolkit/
# Escape leading single quotes in man pages which are misinterpreted as macros,
# patch sent upstream, upstream ticket #108312
Patch0:        oath-toolkit-2.0.2-man-fix.patch

%description
The OATH Toolkit provide components for building one-time password
authentication systems. It contains shared libraries, command line tools and a
PAM module. Supported technologies include the event-based HOTP algorithm
(RFC4226) and the time-based TOTP algorithm (RFC6238). OATH stands for Open
AuTHentication, which is the organization that specify the algorithms. For
managing secret key files, the Portable Symmetric Key Container (PSKC) format
described in RFC6030 is supported.

%description -l zh_CN.UTF-8
一次性密码组件。

%package -n liboath
Summary:          Library for OATH handling
Summary(zh_CN.UTF-8): 处理 OATH 的库
Group:            Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:          LGPLv2+
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n liboath
OATH stands for Open AuTHentication, which is the organization that
specify the algorithms. Supported technologies include the event-based
HOTP algorithm (RFC4226) and the time-based TOTP algorithm (RFC6238).

%description -n liboath -l zh_CN.UTF-8
处理 OATH 的库。

%package -n liboath-devel
Summary:  Development files for liboath
Summary(zh_CN.UTF-8): liboath 的开发包
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:  LGPLv2+
Requires: liboath%{?_isa} = %{version}-%{release}

%description -n liboath-devel
Development files for liboath.

%description -n liboath-devel -l zh_CN.UTF-8
liboath 的开发包。

%package -n liboath-doc
Summary:   Documentation files for liboath
Group:     Development/Libraries
License:   LGPLv2+
Requires:  liboath = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n liboath-doc
Documentation files for liboath.

%package -n libpskc
Summary:          Library for PSKC handling
Group:            Development/Libraries
License:          LGPLv2+
Requires:         xml-common
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# https://fedorahosted.org/fpc/ticket/174
Provides:         bundled(gnulib)

%description -n libpskc
Library for managing secret key files, the Portable Symmetric Key
Container (PSKC) format described in RFC6030 is supported.

%package -n libpskc-devel
Summary:  Development files for libpskc
Group:    Development/Libraries
License:  LGPLv2+
Requires: libpskc%{?_isa} = %{version}-%{release}

%description -n libpskc-devel
Development files for libpskc.

%package -n libpskc-doc
Summary:   Documentation files for libpskc
Group:     Development/Libraries
License:   LGPLv2+
Requires:  libpskc = %{version}-%{release}
Requires:  gtk-doc
BuildArch: noarch

%description -n libpskc-doc
Documentation files for libpskc.

%package -n oathtool
Summary:  A command line tool for generating and validating OTPs
License:  GPLv3+
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description -n oathtool
A command line tool for generating and validating OTPs.

%package -n pskctool
Summary:  A command line tool for manipulating PSKC data
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

%description -n pskctool
A command line tool for manipulating PSKC data.

%package -n pam_oath
Summary:  A PAM module for pluggable login authentication for OATH
Group:    Development/Libraries
Requires: pam

%description -n pam_oath
A PAM module for pluggable login authentication for OATH.

%prep
%setup -q
%patch0 -p1 -b .man-fix

%build
%configure --with-pam-dir=%{_libdir}/security

# Kill rpaths and link with --as-needed
for d in liboath libpskc oathtool pam_oath pskctool
do
  sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' $d/libtool
  sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' $d/libtool
  sed -i 's| -shared | -Wl,--as-needed\0|g' $d/libtool
done

make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

# Remove static objects and libtool files
rm -f %{buildroot}%{_libdir}/*.{a,la}
rm -f %{buildroot}%{_libdir}/security/*.la

# Make /etc/liboath directory
mkdir -p -m 0600 %{buildroot}%{_sysconfdir}/liboath

%post -n liboath -p /sbin/ldconfig

%postun -n liboath -p /sbin/ldconfig

%post -n libpskc -p /sbin/ldconfig

%postun -n libpskc -p /sbin/ldconfig

%files -n liboath
%doc liboath/COPYING
%attr(0600, root, root) %dir %{_sysconfdir}/liboath
%{_libdir}/liboath.so.*

%files -n liboath-devel
%{_includedir}/liboath
%{_libdir}/liboath.so
%{_libdir}/pkgconfig/liboath.pc

%files -n liboath-doc
%{_mandir}/man3/oath*
%{_datadir}/gtk-doc/html/liboath/*

%files -n libpskc
%doc libpskc/README
%{_libdir}/libpskc.so.*
%{_datadir}/xml/pskc

%files -n libpskc-devel
%{_includedir}/pskc
%{_libdir}/libpskc.so
%{_libdir}/pkgconfig/libpskc.pc

%files -n libpskc-doc
%{_mandir}/man3/pskc*
%{_datadir}/gtk-doc/html/libpskc/*

%files -n oathtool
%doc oathtool/COPYING
%{_bindir}/oathtool
%{_mandir}/man1/oathtool.*

%files -n pskctool
%{_bindir}/pskctool
%{_mandir}/man1/pskctool.*

%files -n pam_oath
%doc pam_oath/README pam_oath/COPYING
%{_libdir}/security/pam_oath.so

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 2.6.1-2
- 更新到 2.6.1

* Tue Mar 03 2015 Liu Di <liudidi@gmail.com> - 2.4.1-1
- 更新到 2.4.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.0-1
- New version
  Resolves: rhbz#987378

* Wed Jul 10 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2.0-1
- New version
  Resolves: rhbz#982986

* Wed Jun  5 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-3
- Fixed requirements according to reviewer comments
- Linked with --as-needed
- Fixed man pages (by man-fix patch)

* Mon Apr  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-2
- Added /etc/liboath directory to hold configuration / user lists

* Sun Apr 07 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-1
- Initial version
