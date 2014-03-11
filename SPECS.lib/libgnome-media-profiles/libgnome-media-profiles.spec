Name:           libgnome-media-profiles
Version:        3.0.0
Release:        5%{?dist}
Summary:        GNOME Media Profiles library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://git.gnome.org/browse/libgnome-media-profiles
Source0:        http://download.gnome.org/sources/%{name}/3.0/%{name}-%{version}.tar.bz2

BuildRequires: gtk3-devel >= 2.99.0
BuildRequires: GConf2-devel glib2-devel
Buildrequires: gstreamer-devel gstreamer-plugins-base-devel
BuildRequires: intltool
BuildRequires: gnome-doc-utils

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

Provides:	gnome-media-libs = %{version}-%{release}
Obsoletes:      gnome-media-libs <= 2.91.0-1.fc15

%description
The GNOME Media Profiles library provides prebuilt GStreamer pipelines
for applications aiming to support different sound formats.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:	gnome-media-devel = %{version}-%{release}
Obsoletes:      gnome-media-devel <= 2.91.0-1.fc15

%description    devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static --disable-schemas-install --disable-scrollkeeper
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang libgnome-media-profiles
%find_lang gnome-audio-profiles --with-gnome


%post
/sbin/ldconfig
%gconf_schema_upgrade gnome-media-profiles


%postun
/sbin/ldconfig
%gconf_schema_prepare gnome-media-profiles


%preun
%gconf_schema_remove gnome-media-profiles


%files -f libgnome-media-profiles.lang -f gnome-audio-profiles.lang
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/gnome-audio-profiles-properties
%{_sysconfdir}/gconf/schemas/gnome-media-profiles.schemas
%{_libdir}/*.so.*
%{_datadir}/libgnome-media-profiles

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgnome-media-profiles-3.0.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.0.0-5
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Yanko Kaneti <yaneti@declera.com> 3.0.0-2
- Rebuild. Should get rid of the explicit libpng requirement.

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.2-15
- Rebuild for newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Bastien Nocera <bnocera@redhat.com> 2.91.2-13
- Really rebuild against newer gtk

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.2-12
- Rebuild against newer gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.91.2-11
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-10
- Rebuild against new gtk

* Mon Nov 15 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-9
- Add distro to release number for the obsoletes because RPM's
  comparisons suck

* Fri Nov 12 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-8
- Fix wrongly versioned provides

* Fri Nov 12 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-7
- Add obsoletes for gnome-media-libs as well

* Fri Nov 12 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-6
- --disable-scrollkeeper and not BR it

* Thu Nov 11 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-5
- Add gnome-media-devel provides to devel

* Thu Nov 11 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-4
- Add gnome-media-devel obsoletes to devel

* Thu Nov 11 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-3
- Shorten the devel description.

* Thu Nov 10 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-2
- Add some BRs so that it actually builds in mock.

* Thu Nov 10 2010 Yanko Kaneti <yaneti@declera.com> 2.91.2-1
- First attempt for review.
