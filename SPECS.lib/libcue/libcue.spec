Name:		libcue
Version: 1.4.0
Release:	5%{?dist}
Summary:	Cue sheet parser library
Summary(zh_CN.UTF-8): cue 表解析库

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# Files libcue/rem.{c,h} contains a BSD header
License:	GPLv2 and BSD
URL:		http://libcue.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
Libcue is intended for parsing a so-called cue sheet from a char string or
a file pointer. For handling of the parsed data a convenient API is available.

%description -l zh_CN.UTF-8
CUE 文件解析库。

%package devel
Summary:	Development files
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig


%description	devel
Development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libcue.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.*
%doc AUTHORS COPYING NEWS


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 1.4.0-5
- 更新到 1.4.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 16 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-2
- Changed %%description a bit
- Corrected license field
- Fixed Source0 value
- Fixed Group tag for main package

* Mon Nov  9 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-1
- Initial package for Fedora

