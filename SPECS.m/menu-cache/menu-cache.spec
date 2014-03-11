Name:           menu-cache
Version:        0.4.1
Release:        1%{?dist}
Summary:        Caching mechanism for freedesktop.org compliant menus

Group:          System Environment/Libraries
License:        LGPLv2+ and GPLv2+
URL:            http://lxde.org
#VCS: git:git://lxde.git.sourceforge.net/gitroot/lxde/menu-cache
Source0:        http://downloads.sourceforge.net/lxde/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel >= 2.16.0

%description
Menu-cache is a caching mechanism for freedesktop.org compliant menus to 
speed up parsing of the menu entries. It is currently used by some of 
components of the LXDE desktop environment such as LXPanel or LXLauncher.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
# remove rpath in menu-cache-gen
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
#FIXME: add ChangeLog and NEWS if there is content
%doc AUTHORS COPYING README
%{_libexecdir}/menu-cache-gen
%{_libexecdir}/menu-cached
%{_libdir}/libmenu-cache.so.*
#%{_mandir}/man*/*.gz


%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/menu-cache/
%{_includedir}/menu-cache/*.h
%{_libdir}/libmenu-cache.so
%{_libdir}/pkgconfig/libmenu-cache.pc


%changelog
* Sun Nov 25 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.4.1-1
- Update to 0.4.1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.3-2
- No longer require redhat-menus

* Sun Jun 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3 (#827783)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Sun Feb 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Tue Nov 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.6-1
- Update to 0.2.6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.5-1
- Update to 0.2.5

* Mon Apr 20 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.4-1
- Update to 0.2.4

* Tue Mar 31 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3

* Wed Dec 10 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2

* Tue Dec 09 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0
- Split into base and devel package

* Sun Dec 07 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.3-1
- Initial Fedora package
