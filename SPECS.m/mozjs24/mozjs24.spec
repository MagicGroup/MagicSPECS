Summary:	JavaScript interpreter and libraries
Summary(zh_CN.UTF-8): Java 脚本解释器和库
Name:		mozjs24
Version:	24.2.0
Release:	5%{?dist}
License:	MPLv2.0
Group:		Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2
BuildRequires:	pkgconfig(nspr)
BuildRequires:	readline-devel
BuildRequires:	/usr/bin/zip
BuildRequires:	/usr/bin/python

Patch0:		js17-build-fixes.patch
Patch1:		mozjs24-0001-Add-AArch64-support.patch
Patch2:		mozjs24-hardening-flags.patch
Patch3:		mozjs24-perl522.patch

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
super set of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%description -l zh_CN.UTF-8
Java 脚本解释器和库。

%package devel
Summary: Header files, libraries and development documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n mozjs-%{version}
# Delete bundled sources
rm js/src/editline -rf
rm js/src/ctypes/libffi -rf
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod a+x configure

%build
%configure \
  --disable-static \
  --with-system-nspr \
  --enable-threadsafe \
  --enable-readline \
  --enable-xterm-updates
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# For some reason the headers and pkg-config file are executable
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;
chmod a-x  %{buildroot}%{_libdir}/pkgconfig/*.pc
# Upstream does not honor --disable-static yet
rm -f %{buildroot}%{_libdir}/*.a
# This is also statically linked; once that is fixed that we could
# consider shipping it.
rm -f %{buildroot}%{_bindir}/js24

# However, delete js-config since everything should use
# the pkg-config file.
rm -f %{buildroot}%{_bindir}/js24-config
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE README
%{_libdir}/*.so

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mozjs-24

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 24.2.0-5
- 为 Magic 3.0 重建

* Tue Dec 02 2014 Liu Di <liudidi@gmail.com> - 24.2.0-4
- 为 Magic 3.0 重建

* Wed Jan 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 24.2.0-3
- Add patch to fix FTBFS on aarch64

* Fri Jan 10 2014 Debarshi Ray <rishi@fedoraproject.org> 24.2.0-2
- Fix a spelling mistake

* Thu Jan 09 2014 Debarshi Ray <rishi@fedoraproject.org> 24.2.0-1
- Initial spec
