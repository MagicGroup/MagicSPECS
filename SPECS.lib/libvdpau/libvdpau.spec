Name:           libvdpau
Version:        0.4.1
Release:        6%{?dist}
Summary:        Wrapper library for the Video Decode and Presentation API

Group:          System Environment/Libraries
License:        MIT
URL:            http://freedesktop.org/wiki/Software/VDPAU
Source0:        http://people.freedesktop.org/~aplattner/vdpau/libvdpau-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool

%{?!_without_docs:
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  texlive-latex
}

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  xorg-x11-proto-devel


%description
VDPAU is the Video Decode and Presentation API for UNIX. 
It provides an interface to video decode acceleration and presentation
hardware present in modern GPUs.

%{?!_without_docs:
%package        docs
Summary:        Documentation for %{name}
Group:          Documentation

%description    docs
The %{name}-docs package contains documentation for %{name}.
}

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
autoreconf -vif


%build
%configure --disable-static \
 %{?_without_docs:--disable-documentation }

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_trace.so*

%{?!_without_docs:
%files docs
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}
}

%files devel
%defattr(-,root,root,-)
%{_includedir}/vdpau/
%{_libdir}/libvdpau.so
%{_libdir}/pkgconfig/vdpau.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.1-6
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 0.4.1-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.1-3
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.4.1-1
- Update to 0.4.1

* Sat Mar 13 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.4-1
- Update to 0.4

* Sun Nov 22 2009 kwizart < kwizart at gmail.com > - 0.3-1
- Update to 0.3
- Create docs sub-package
- Allow --without docs conditional

* Thu Sep 17 2009 kwizart < kwizart at gmail.com > - 0.2-1
- Update to 0.2
- Disable ExclusiveArch

* Mon Sep  7 2009 kwizart < kwizart at gmail.com > - 0.1-0.6.20090904git
- Update to gitdate 20090904git

* Wed Sep  2 2009 kwizart < kwizart at gmail.com > - 0.1-0.5git20090902
- Update to gitdate 20090902 with merged patches

* Mon Jun 15 2009 kwizart < kwizart at gmail.com > - 0.1-0.3git20090318
- Add missing -ldl at link time

* Fri Mar 22 2009 kwizart < kwizart at gmail.com > - 0.1-0.2git20090318
- Backport fix thread_2

* Fri Mar  6 2009 kwizart < kwizart at gmail.com > - 0.1-0.1git20090318
- Initial spec file

