Summary: Palm Sync Library
Summary(zh_CN.UTF-8):  Palm 同步库
Name:    libmal
# NOTE: this isn't the latest version, but is the last version known to 
# work with kdepim-3.5.x
Version: 0.44.1
Release: 4%{?dist}
License: MPL	
Url: 	 http://jasonday.home.att.net/code/libmal/ 
Source0: http://jasonday.home.att.net/code/libmal/libmal-%{version}.tar.gz 
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

Patch1: libmal-0.44-64bit.patch
# pilot-link-0.12 fixes
Patch2: libmal-0.31-pi12.patch

BuildRequires: pilot-link-devel 

%description
A convenience library of the object files contained in Tom Whittaker's 
malsync distribution, along with a few wrapper functions.

%description -l zh_CN.UTF-8
一个方便的包含于 Tom Whittaker 的 malsync 套件的
对象文件库，同时包含一些包装函数。

%package devel
Summary: Header and library files for %{name}
Summary(zh_CN.UTF-8): %{name} 的头文件和库文件
Group:   Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Requires: %{name} = %{version}-%{release}
%description devel
Header and library files for %{name}

%description devel -l zh_CN.UTF-8
%{name} 的头文件和库文件



%prep
%setup -q 

%patch1 -p1 -b .64bits

%build
%configure --disable-static

make %{?_smp_mflags} 


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

## Unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}


%files
%defattr(-,root,root,-)
%doc ChangeLog README
#empties
#doc AUTHORS NEWS TODO
%{_bindir}/malsync
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/*


%changelog
* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 0.44.1-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.44.1-3
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 0.44.1-2
- 为 Magic 3.0 重建

* Mon Jun 25 2007 kde <athena_star {at} 163 {dot} com> - 0.31-1mgc
- port to magic linux

* Wed Nov 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-5
- respin against new pilot-link

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-4
- fc6 respin

* Thu Apr 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-3 
- respin for pilot-link

* Wed Mar 22 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-2
- capitalize summary
- drop empty %%doc's: AUTHORS NEWS TODO

* Mon Oct 31 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-1
- cleanup for Extras

* Tue Jun 14 2005 Rex Dieter 0.31-0.1
- pilot-link-0.12 fixes

* Thu Dec 16 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0.31-0.fdr.3
- fix 64 builds (for finding pilot-link libs)

* Wed Jul 21 2004 Rex Dieter <rexdieter at sf.net> 0.31-0.fdr.2
- nuke .la file(s).
- --disable-static

* Fri Oct 17 2003 Rex Dieter <rexdieter at sf.net> 0.31-0.fdr.1
- first try

