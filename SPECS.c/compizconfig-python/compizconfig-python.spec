%global  basever 0.8.8

Name:           compizconfig-python
Version:        0.8.4
Release:        11%{?dist}
Epoch:          1
Summary:        Python bindings for the Compiz Configuration System
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.compiz.org
Source0:        http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
# libdrm is not available on these arches
ExcludeArch:    s390 s390x ppc64

Patch0:         compizconfig-python-aarch64.patch
Patch1:         compizconfig-python_automake-1.13.patch

BuildRequires:  libcompizconfig-devel >= %{basever}
BuildRequires:  Pyrex
BuildRequires:  glib2-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

# prevent rpm's auto-generated provides mechanism to include private
# libraries
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup
}

%description
The Compiz Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
though plugins and themes contributed by the community giving a
rich desktop experience.

This package contains bindings to configure Compiz's
plugins and the composite window manager.

%prep
%setup -q
%patch0 -p1 -b .aarch64
%patch1 -p1 -b .automake

autoreconf -f -i

%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.a" -o -name "*.la" | xargs rm -f


%files
%doc COPYING
%{python_sitearch}/compizconfig.so
%exclude %{_libdir}/pkgconfig/compizconfig-python.pc


%changelog
* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.4-11
- 为 Magic 3.0 重建

* Wed May 07 2014 Liu Di <liudidi@gmail.com> - 1:0.8.4-10
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-8
- fix build for aarch64
- add requires autoconf, automake and libtool
- add autorefonf command
- fix automake-1.13 build deprecations

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.4-6
- build fedora
- remove python_sitelib stuff
- add filter setup
- add basever

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-5
- add Epoch tag
- fix source url

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-4
- improve spec file

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.4-3
- build for mate

* Sat Jul 31 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.8.4-3
- rebuild for broken deps

