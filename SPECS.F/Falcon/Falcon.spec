%global host     www.falconpl.org
# latest bugfix release does not come with updated docs
# remove once the releases are synced again
%global docver   %{version}

Name:            Falcon
Version:         0.9.6.8
Release:         2%{?dist}
Summary:         The Falcon Programming Language
Summary(it):     Il linguaggio di programmazione Falcon

License:        GPLv2+
Group:          Development/Languages
URL:            http://%{host}/
Source0:        http://%{host}/project_dl/_official_rel/%{name}-%{version}.tgz
Source1:        http://%{host}/project_dl/_official_rel/%{name}-docs-%{docver}.tgz
# Patches from Git for Falcon's mongo modules
Patch0:         Falcon-0.9.6.8-mongo-cmake-linux-x64.patch
Patch1:         Falcon-0.9.6.8-mongo-stdint.patch

%if 0%{?rhel} <= 5
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
%endif

BuildRequires:  cmake pcre-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel

%description
The Falcon Programming Language is an embeddable scripting language
aiming to empower even simple applications with a powerful,
flexible, extensible and highly configurable scripting engine.

Falcon is also a standalone multiplatform scripting language that
aims to be both simple and powerful.

%description -l it
Il Falcon è un linguaggio di programmazione embeddabile che intende
fornire nuove potenzialità anche a semplici applicazioni, fornendo
loro un potente, flessibie, estendibile e configurabile motore
di scripting.

Falcon è anche uno scripting languge completo e multipiattaforma,
semplice e potente.

%package   devel
Summary:   Development files for %{name}
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}
Requires:  cmake

%description devel
The Falcon Programming Language is an embeddable scripting language
aiming to empower even simple applications with a powerful,
flexible, extensible and highly configurable scripting engine.

Falcon is also a standalone multiplatform scripting language that
aims to be both simple and powerful.

This package contains development files for %{name}. This is not
necessary for using the %{name} interpreter.

%package   doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
The Falcon Programming Language is an embeddable scripting language
aiming to empower even simple applications with a powerful,
flexible, extensible and highly configurable scripting engine.

Falcon is also a standalone multiplatform scripting language that
aims to be both simple and powerful.

This package contains HTML documentation for %{name}.


%prep
%setup -q -a1
%patch0 -p1 -b .mongo-cmake-linux-x64
%patch1 -p1 -b .mongo-stdint
mkdir largedocs
mv %{docver}-html largedocs


%build
%cmake . \
       -DFALCON_SHARE_DIR=share/doc/Falcon-%{version} -DMYSQL_LIB_DIR=%{_libdir}/mysql
#-DFALCON_LIB_DIR=%{_lib} \
#       -DFALCON_CMAKE_DIR=%{_lib}/falcon/cmake \

make VERBOSE=1 %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc %{_datadir}/doc/Falcon-%{version}
%exclude %{_bindir}/falcon-conf
%exclude %{_bindir}/falconeer.fal
%exclude %{_bindir}/faltest
%{_bindir}/*
%exclude %{_mandir}/man1/falcon-conf*
%exclude %{_mandir}/man1/falconeer.fal*
%exclude %{_mandir}/man1/faltest*
%{_libdir}/falcon
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/falcon-conf
%{_bindir}/falconeer.fal
%{_bindir}/faltest
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/cmake/faldoc
%{_mandir}/man1/falcon-conf*
%{_mandir}/man1/falconeer.fal*
%{_mandir}/man1/faltest*

%files doc
%defattr(-,root,root,-)
%doc largedocs/*


%changelog
* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar  6 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.6.8-1
- Update to 0.9.6.8

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.6-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.6.6-1
- Update to 0.9.6.6

* Wed Sep 23 2009 Michel Salim <salimma@fedoraproject.org> - 0.9.4.2-1
- Update to 0.9.4.2
- Package documentation files

* Tue Aug 25 2009 Michel Salim <salimma@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Michel Salim <salimma@fedoraproject.org> - 0.8.14.2-1
- Update to 0.8.14.2

* Mon Jun  9 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.8.10-3
- Revert r401 patch; does not fix cmake-2.6 problem on Rawhide
  Reverting to manually using 'make install' in individual subdirectories

* Mon Jun  9 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.8.10-2
- Merge in cmake fixes from core/trunk r401
- Patch core/CMakeLists.txt to default to /usr, as it appears that the
  requested prefix is not properly used
- Fix incorrect #! interpreter in falconeer.fal

* Sat Jun  7 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.8.10-1
- Update to 0.8.10

* Wed May 21 2008 Michel Salim <salimma@fedoraproject.org> - 0.8.8-3
- Use correct libdir for module path

* Thu Apr 24 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.8.8-2
- Updated license
- Changed source URL to one that includes license grant

* Fri Jan 25 2008 Michel Salim <michel.sylvan@gmail.com> - 0.8.8-1
- Initial Fedora package
  Based on initial spec by Giancarlo Niccolai <gc@falconpl.org>
