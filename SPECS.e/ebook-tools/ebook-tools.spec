Name:		ebook-tools
Version:	0.2.2
Release:	1%{?dist}
Summary:	Tools for accessing and converting various ebook file formats
Summary(zh_CN.UTF-8): 访问和转换多种电子书格式的工具

Group:		Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
License:	MIT
URL:		http://sourceforge.net/projects/ebook-tools/

Source0:	http://downloads.sourceforge.net/ebook-tools/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# support libzip pkgconfig
Patch51:        ebook-tools-0.2.1-libzip_pkgconfig.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libzip)

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
Tools for accessing and converting various ebook file formats.

%description -l zh_CN.UTF-8
访问和转换多种电子书格式的工具。

%package devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package libs
Summary:	Libraries for %{name}
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description libs
The %{name}-libs package contains libraries to be used by 
%{name} and others.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%prep
%setup -q
%patch51 -p1 -b .libzip_pkgconfig


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd
make %{_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform} 

#remove because it doesnt work without clit
rm -f %{buildroot}%{_bindir}/lit2epub
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/einfo

%files	devel
%defattr(-,root,root,-)
%{_libdir}/libepub.so
%{_includedir}/epub*.h

%files	libs
%defattr(-,root,root,-)
%doc README LICENSE
%{_libdir}/libepub.so.0*

%changelog
* Fri Oct 18 2013 John5342 <john5342 at, fedoraproject.org> 0.2.2-1
- New upstream release (fixes rhbz:1014443)
- Drop rmhardcoded (-DLIB_SUFFIX now supported directly)

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 0.2.1-5
- rebuild for new libzip

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.2.1-1
- ebook-tools-0.2.1
- pkgconfig-style deps
- patch to support libzip pkgconfig dirs 

* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.2.0-4
- rebuild for new libzip

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.2.0-1
- ebook-tools-0.2.0
- %%files: track lib soname
- tighten subpkg deps with %%_isa

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 John5342 <john5342 at, fedoraproject.org> 0.1.1-3
- Actually remove lit2epub this time

* Mon Dec 15 2008 John5342 <john5342 at, fedoraproject.org> 0.1.1-2
- Removed lit2epub as it doesnt work without clit

* Mon Dec 15 2008 John5342 <john5342 at, fedoraproject.org> 0.1.1-1
- Initial package
