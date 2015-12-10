%define     real_version    1.8beta5
Name:       tsocks
Version:    1.8
Release:    0.13.beta5%{?dist}
Summary:    Library for catching network connections, redirecting them on a SOCKS server
Summary(zh_CN.UTF-8): 把网络连接重定向到 SOCKS 代理服务器的库
Group:      System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:    GPLv2+
URL:        http://tsocks.sourceforge.net/
Source0:    http://downloads.sourceforge.net/%{name}/%{name}-%{real_version}.tar.gz
Patch0:     tsocks_remove_static_lib.patch
Patch1:     tsocks_fix_lib_path.patch
Patch2:     tsocks_script_validation_error.patch
Patch3:     tsocks_documentation_update.patch
Patch4:     tsocks-1.8-soname.patch
Patch5:     tsocks_fix_man_typo.patch
Patch6:     tsocks_include_missing_tools.patch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
tsocks is designed for use in machines which are firewalled from the
Internet. It avoids the need to recompile applications like lynx or
telnet so they can use SOCKS to reach the Internet. It behaves much
like the SOCKSified TCP/IP stacks seen on other platforms.

tsocks is a library to allow transparent SOCKS proxying. It wraps the
normal connect() function. When a connection is attempted, it consults
the configuration file (which is defined at configure time but defaults
to /etc/tsocks.conf) and determines if the IP address specified is local.
If it is not, the library redirects the connection to a SOCKS server
specified in the configuration file. It then negotiates that connection
with the SOCKS server and passes the connection back to the calling
program.

%description -l zh_CN.UTF-8
把网络连接重定向到 SOCKS 代理服务器的库。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING FAQ TODO tsocks.conf.simple.example tsocks.conf.complex.example
%{_mandir}/man?/*
%{_bindir}/*
%{_libdir}/libtsocks*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.8-0.13.beta5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.8-0.12.beta5
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 1.8-0.11.beta5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.8-0.10.beta5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.9.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Jean-Francois Saucier <jsaucier@gmail.com> - 1.8-0.8.beta5
- Fix a typo in the man page
- Include the missing tools inspectsocks and validateconf

* Thu Feb 17 2011 Rex Dieter <rdieter@fedoraproject.org> 1.8-0.7.beta5
- avoid odd rpm dep mismatches by explictly specifying a soname for libtsocks

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.6.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  6 2010 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 1.8-0.5.beta5
- Fix the library path problem more cleanly
- Fix bash script validation to handle the no argument case
- Change patch name to reflect guidelines
- Fix documentation to reflect patch modifications
- Remove INSTALL from packaged files

* Mon Dec 14 2009 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 1.8-0.4.beta5
- Fix the library path problem on x86_64 and ppc64
- Elaborate the summary and description fields

* Sat Dec  5 2009 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 1.8-0.3.beta5
- Fix as per the recommendations on bug #543566

* Thu Dec  3 2009 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 1.8-0.2.beta5
- Fix Source0 URL as per the guidelines

* Tue Dec  1 2009 Jean-Francois Saucier <jfsaucier@infoglobe.ca> - 1.8-0.1.beta5
- Initial build for Fedora
