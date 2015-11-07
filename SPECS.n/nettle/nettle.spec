Name:           nettle
Version: 3.1.1
Release: 2%{?dist}
Summary:        A low-level cryptographic library
Summary(zh_CN.UTF-8): 低级的密码库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        LGPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
#Source0:	%{name}-%{version}-hobbled.tar.gz
Source0:        https://ftp.gnu.org/gnu/nettle/%{name}-%{version}.tar.gz

BuildRequires:  gmp-devel m4 texinfo-tex texlive-dvips ghostscript

Requires(post): info
Requires(preun): info


%package devel
Summary:        Development headers for a low-level cryptographic library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%description -l zh_CN.UTF-8
低级的密码库。

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains the files needed for developing 
applications with nettle.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure

%build
%configure --enable-shared
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -p -m 644 nettle.info $RPM_BUILD_ROOT%{_infodir}/
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.*
magic_rpm_clean.sh

%check
make check

%files
%doc AUTHORS ChangeLog NEWS README TODO
%{_infodir}/nettle.info.gz
%{_bindir}/nettle-lfib-stream
%{_bindir}/pkcs1-conv
%{_bindir}/sexp-conv
%{_bindir}/nettle-hash
%{_libdir}/libnettle.so.*
%{_libdir}/libhogweed.so.*


%files devel
%doc descore.README nettle.html nettle.pdf COPYING.LIB
%{_includedir}/nettle
%{_libdir}/libnettle.so
%{_libdir}/libhogweed.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig



%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.1.1-2
- 更新到 3.1.1

* Wed Jan 28 2015 Liu Di <liudidi@gmail.com> - 3.0-1
- 更新到 3.0

* Fri Jan 10 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-3
- Corrected bug number in previous comment.

* Fri Dec 13 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-2
- Added patch nettle-tmpalloc.patch to solve #1051455

* Mon Nov 25 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> - 2.7.1-1
- Updated to nettle 2.7.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb  6 2013 Tomáš Mráz <tmraz@redhat.com> - 2.6-2
- nettle includes use gmp.h

* Tue Feb  5 2013 Tomáš Mráz <tmraz@redhat.com> - 2.6-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-3
- Remove explicit buildroot handling and defattr.

* Wed Jul 04 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-2
- Review feedback

* Mon Jun 18 2012 David Woodhouse <dwmw2@infradead.org> - 2.4-1
- Revive package (GnuTLS needs it), disable static, update to current release 2.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 10 2008 Ian Weller <ianweller@gmail.com> 1.15-5
- Moved static lib to -static

* Mon Mar 24 2008 Ian Weller <ianweller@gmail.com> 1.15-4
- Added libraries and ldconfig

* Mon Feb 18 2008 Ian Weller <ianweller@gmail.com> 1.15-3
- Added provides -static to -devel

* Sun Feb 17 2008 Ian Weller <ianweller@gmail.com> 1.15-2
- Removed redundant requires
- Removed redundant documentation between packages
- Fixed license tag
- Fixed -devel description
- Added the static library back to -devel
- Added make clean

* Fri Feb 08 2008 Ian Weller <ianweller@gmail.com> 1.15-1
- First package build.
