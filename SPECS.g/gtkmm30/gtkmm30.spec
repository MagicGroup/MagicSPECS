%global apiver 3.0
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gtkmm30
Version:        3.8.0
Release:        1%{?dist}
Summary:        C++ interface for the GTK+ library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtkmm/%{release_version}/gtkmm-%{version}.tar.xz

BuildRequires:  atkmm-devel
BuildRequires:  cairomm-devel
BuildRequires:  glibmm24-devel
BuildRequires:  gtk3-devel
BuildRequires:  pangomm-devel

%description
gtkmm is the official C++ interface for the popular GUI library GTK+.
Highlights include type safe callbacks, and a comprehensive set of
widgets that are easily extensible via inheritance.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        API documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm24-doc

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n gtkmm-%{version}

# Copy demos before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a demos/ _docs/


%build
%configure --disable-static

# fix lib64 rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# avoid unused direct dependencies
sed -i 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
make check %{?_smp_mflags}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/gtkmm-%{apiver}/
%{_includedir}/gdkmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/gtkmm-%{apiver}/
%{_libdir}/gdkmm-%{apiver}/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_docdir}/gtkmm-%{apiver}/
%doc %{_datadir}/devhelp/
%doc _docs/*


%changelog
* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.12-1
- Update to 3.7.12

* Mon Feb 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.10-1
- Update to 3.7.10

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Thu Sep 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.13-1
- Update to 3.5.13

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.12-1
- Update to 3.5.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Tue Jun 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Wed Apr 11 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.18-1
- Update to 3.3.18

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.16-1
- Update to 3.3.16
- Remove manual Requires from -devel subpackage; these are automatically
  generated with rpm pkgconfig depgen

* Tue Feb 07 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.14-1
- Update to 3.3.14

* Sun Jan 22 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.3.2-1
- upstream 3.3.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 16 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.90-1
- Update to 3.1.90

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.18-1
- Update to 3.1.18

* Wed Aug 31 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.16-1
- Update to 3.1.16

* Thu Jul 28 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.10-1
- Update to 3.1.10

* Sat Jul 09 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.8-1
- Update to 3.1.8
- Use the xz compressed tarballs
- Clean up the spec file for modern rpmbuild

* Mon May 09 2011 Kalev Lember <kalev@smartlink.ee> - 3.0.1-1
- Update to 3.0.1

* Wed Apr 06 2011 Kalev Lember <kalev@smartlink.ee> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.8-1
- Update to 2.99.8
- Dropped BR mm-common which is no longer needed for tarball builds

* Fri Mar 18 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.6-1
- Update to 2.99.6
- BuildRequire mm-common for doctools which are no longer in glibmm24-devel.

* Tue Mar 01 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.5-2
- Spec cleanup
- Ship the source code for demos in -doc
- Require base package from -doc subpackage
- Actually co-own /usr/share/devhelp/ directory

* Sun Feb 27 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.99.5-1
- Update to 2.99.5

* Sun Feb 27 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.99.3-4
- fix documentation handling

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-3
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.3-1
- Update to 2.99.3

* Thu Jan 13 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.1-1
- Update to 2.99.1

* Fri Dec 03 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.5.1-1
- Update to 2.91.5.1

* Tue Nov 02 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.3-1
- Update to 2.91.3

* Mon Nov 01 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.2-1
- Update to 2.91.2
- Removed no-application.patch as we now have new enough glibmm

* Sun Oct 03 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.90.7-1
- 2.90.7
- no more "application" support in glib

* Wed Sep 29 2010 jkeating - 2.90.5-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.5-2
- Co-own /usr/share/gtk-doc/ directory (#604169)

* Wed Jul 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.5-1
- Update to 2.90.5

* Wed Jul 07 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-3
- Avoid putting built demos in /usr/share (#608326)
- Moved demos to -doc package

* Tue Jul 06 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-2
- Review fixes (#608326)
- Fixed lib64 rpaths
- Added %%check section
- Use %%define instead of %%global to set release_version macro, as the latter
  seems to confuse rpmlint
- Replaced hardcoded /usr/share with %%_datadir macro
- Updated description

* Mon Jul 05 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-1
- Update to 2.90.4.0

* Sat Jun 26 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.3.1-1
- Initial gtkmm30 spec based on gtkmm24 spec
