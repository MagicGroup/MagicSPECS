%global shortname srtp
%global cvsver 20101004cvs
%define git 1
%define vcsdate 20140623

Name:		lib%{shortname}
Version:	1.4.4
Release:	7.%{vcsdate}git%{?dist}
Summary:	An implementation of the Secure Real-time Transport Protocol (SRTP)
Summary(zh_CN.UTF-8): 安全实时传输协议（SRTP）的实现
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	BSD
URL:		http://srtp.sourceforge.net
# Upstream 1.4.4 tarball is a bit dated, need to use cvs
# cvs -d:pserver:anonymous@srtp.cvs.sourceforge.net:/cvsroot/srtp co -P srtp
# tar cvfj srtp-1.4.4-20101004cvs.tar.bz2 srtp/
Source0:	%{shortname}-git%{vcsdate}.tar.xz
# Pkgconfig goodness
Source1:	libsrtp.pc
Source2:	make_libsrtp_git_package.sh
# Seriously. Who doesn't do shared libs these days?
# And how does Chromium always manage to find these projects and use them?
Patch0:		libsrtp-1.4.4-shared.patch
Patch1:   1003_fix_mips_namespace_collision.patch


%description
This package provides an implementation of the Secure Real-time
Transport Protocol (SRTP), the Universal Security Transform (UST), and
a supporting cryptographic kernel. 

%description -l zh_CN.UTF-8 
安全实时传输协议（SRTP）的实现。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{shortname}-git%{vcsdate}
#%patch0 -p1 -b .shared
%patch1 -p1 -b .mips

# Fix end-of-line encoding
sed -i 's/\r//g' doc/draft-irtf-cfrg-icm-00.txt

%build
export CFLAGS="%{optflags} -fPIC"
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
pushd %{buildroot}%{_libdir}
ln -sf libsrtp.so.1.4.5 libsrtp.so
ln -sf libsrtp.so.1.4.5 libsrtp.so.1
popd

# Install the pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
# Fill in the variables
sed -i "s|@PREFIX@|%{_prefix}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@LIBDIR@|%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@INCLUDEDIR@|%{_includedir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README TODO VERSION doc/*.txt doc/*.pdf
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/
%{_libdir}/pkgconfig/libsrtp.pc
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 1.4.4-7.20140623git
- 为 Magic 3.0 重建

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 1.4.4-6.20140623git
- 更新到 20140623 日期的仓库源码

* Mon Jun 23 2014 Liu Di <liudidi@gmail.com> - 1.4.4-5.20101004git
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.4.4-4.20101004cvs
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Liu Di <liudidi@gmail.com> - 1.4.4-3.20101004cvs
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.4-1.20101004cvs
- initial package
