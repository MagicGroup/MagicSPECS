Name:           libmatheval
Version: 1.1.11
Release:        3%{?dist}
Summary:        Library for parsing and evaluating symbolic expressions input as text
Summary(zh_CN.UTF-8): 用户于解析和计算符号表达式输入文本的库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv3+
URL:            http://www.gnu.org/software/libmatheval/
Source0:        http://ftp.gnu.org/gnu/libmatheval/libmatheval-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran, compat-guile18-devel, bison, flex, flex-static, texinfo


%description
GNU libmatheval is a library (callable from C and Fortran) to parse
and evaluate symbolic expressions input as text.  It supports
expressions in any number of variables of arbitrary names, decimal and
symbolic constants, basic unary and binary operators, and elementary
mathematical functions.  In addition to parsing and evaluation,
libmatheval can also compute symbolic derivatives and output
expressions to strings.

%description -l zh_CN.UTF-8
用户于解析和计算符号表达式输入文本的库。

%package devel
Summary:        Development files for libmatheval
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info
Requires:       pkgconfig

%description devel
This package contains the development files for libmatheval.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
export GUILE=/usr/bin/guile1.8
export GUILE_CONFIG=/usr/bin/guile1.8-config
export GUILE_TOOLS=/usr/bin/guile1.8-tools
%configure F77=gfortran --disable-static
make %{?_smp_mflags}

%check
make check ||:


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc NEWS 
%{_includedir}/*
%{_libdir}/*.so
%{_infodir}/libmatheval.info*
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 1.1.11-2
- 为 Magic 3.0 重建

* Fri Aug 16 2013 Jon Ciesla <limburgher@gmail.com> - 1.1.11-1
- 1.1.10, BZ 997815.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.10-1
- 1.1.10, BZ 882169.

* Tue Sep 25 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.9-1
- 1.1.9, BZ 860367.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 31 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 1.1.8-1
- Update to 1.1.8
- Added dependency on flex-static

* Thu Jun 23 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 1.1.5-4
- Info page fixed by upstream. Closes Red Hat Bugzilla bug #465112.

* Fri May 23 2008 Jon Stanley <jonstanley@gmail.com> - 1.1.5-3
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.5-2
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 1.1.5-1
- new upstream 1.1.5

* Sun Mar 18 2007 Ed Hill <ed@eh3.com> - 1.1.4-1
- new upstream 1.1.4

* Sat Sep 23 2006  <ed@eh3.com> - 1.1.3-4
- add BR: texinfo

* Sat Sep 23 2006  <ed@eh3.com> - 1.1.3-3
- disable static libs and add check

* Thu Sep 21 2006  <ed@eh3.com> - 1.1.3-2
- add info dir patch

* Thu Sep 21 2006  <ed@eh3.com> - 1.1.3-1
- initial package creation

