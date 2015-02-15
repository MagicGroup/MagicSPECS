Name:	keybinder
Version:	0.3.0
Release:	5%{?dist}
Summary:	A library for registering global keyboard shortcuts
Group:	Development/Libraries
License:	MIT
URL:	http://kaizer.se/wiki/keybinder/
Source0:	http://kaizer.se/publicfiles/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gtk2-devel
BuildRequires:	python-devel
BuildRequires:	pygtk2-devel
BuildRequires:	pygobject2-devel


%description
keybinder is a library for registering global keyboard shortcuts. 
Keybinder works with GTK-based applications using the X Window System.

The library contains:
- A C library, libkeybinder
- Python bindings, python-keybinder
- An examples directory with programs in C, Lua, Python and Vala.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the development files for %{name}.


%package -n python-%{name}
Group:		Development/Libraries
License:	GPLv2+
Summary:	Keybinder python bindings
Requires:	%{name} = %{version}-%{release}
Requires:	pygtk2 pygobject2

%filter_provides_in %{python_sitearch}.*\.so$
%filter_setup

%description -n python-%{name}
This package contains python bindings for keybinder.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --disable-static --enable-python --disable-lua
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}/%{_libdir}/libkeybinder.la
rm -rf %{buildroot}/%{_libdir}/lua/5.1/keybinder.la
rm -rf %{python_sitearch}/%{name}/_keybinder.la

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libkeybinder.so.* 
%doc NEWS AUTHORS README

%files devel
%defattr(-,root,root)
%{_includedir}/keybinder.h
%{_libdir}/pkgconfig/keybinder.pc
%{_libdir}/libkeybinder.so 
%{_datadir}/gtk-doc
%{_datadir}/gtk-doc/html/%{name}

%files -n python-%{name}
%defattr(-,root,root)
%{python_sitearch}/%{name}
%doc COPYING

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Johannes Lips <hannes@fedoraproject.org> - 0.3.0-4
- disabled the lua bindings to make it buildable again

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Johannes Lips <hannes@fedoraproject.org> - 0.3.0-1
- update to version 0.3.0
- added the gtk-doc file to the devel package

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.2-7
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Johannes Lips <Johannes.Lips googlemail com> 0.2.2-5
- moved the pkgconfig into the devel subpackagae

* Mon Nov 01 2010 Johannes Lips <Johannes.Lips googlemail com> 0.2.2-4
- added the %%{release} tag to the Requires section of the subpackages

* Sun Oct 17 2010 Johannes Lips <Johannes.Lips googlemail com> 0.2.2-3
- removed the *.la file from python subpackage
- added the GPLv2+ license tag for the python subpackage
- fixed ownership of the lua-directory

* Sat Oct 16 2010 Johannes Lips <Johannes.Lips googlemail com> 0.2.2-2
- added an additional lua subpackage
- added the MIT license
- fixed issues with files in the wrong subpackage
- added a filter macro in the python subpackage
- added a %%postun section

* Thu Oct 07 2010 Johannes Lips <Johannes.Lips googlemail com> 0.2.2-1
- initial fedora spec
