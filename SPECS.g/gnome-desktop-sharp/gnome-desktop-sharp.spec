Name:           gnome-desktop-sharp
Version:        2.26.0
Release:        19%{?dist}
Summary:        .NET language binding for mono
Summary(zh_CN.UTF-8): mono 的 .NET 语言绑定

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2
URL:            http://www.mono-project.com/GtkSharp
Source0:        http://ftp.gnome.org/pub/gnome/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Patch1:         %{name}-lib-target.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mono-devel, gtk2-devel
BuildRequires:  librsvg2-devel, vte-devel
# gnome-panel bindings temporary disabled
# BuildRequires: gnome-panel-devel
BuildRequires:  libwnck-devel, gtksourceview2-devel, libgnomeprintui22-devel
BuildRequires:  gnome-sharp-devel
BuildRequires:  gnome-desktop-devel
BuildRequires:  gtk-sharp2-gapi >= 2.12.0
BuildRequires:  gtk-sharp2-devel >= 2.12.0

Provides:       gtksourceview2-sharp = 2:%{version}-%{release}
Obsoletes:      gtksourceview2-sharp < 2:2.20.1-2

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x


%description
GnomeDesktop is a .NET language binding for assorted
GNOME libraries from the desktop release.

%description -l zh_CN.UTF-8 
GNOME 桌面的 .NET 语言绑定。

这是 GNOME 2 版本，已不再更新。

%package         devel
Summary:         Developing files for gnome-Desktop-sharp
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:           Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:        %{name} = %{version}-%{release}
Requires:        pkgconfig

Provides:        gtksourceview2-sharp-devel = 2:%{version}-%{release}
Obsoletes:       gtksourceview2-sharp-devel < 2:2.20.1-2

%description     devel
Package %{name}-devel provides development files for writing
%{name} applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p1 -b .target
sed -i -e 's!@libdir@!${exec_prefix}/lib/!g' gtksourceview/gtksourceview2-sharp.pc.in

# Fix permission
chmod 0644 HACKING

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove libttol archive
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog AUTHORS README
%{_libdir}/*.so
%{_prefix}/lib/mono/gac/gnomedesktop-sharp
#%{_prefix}/lib/mono/gac/gnome-panel-sharp
%{_prefix}/lib/mono/gac/gnome-print-sharp
%{_prefix}/lib/mono/gac/gtksourceview2-sharp
%{_prefix}/lib/mono/gac/rsvg2-sharp
#%{_prefix}/lib/mono/gac/vte-sharp
%{_prefix}/lib/mono/gac/wnck-sharp
%{_prefix}/lib/mono/gnomedesktop-sharp-2.20
#%{_prefix}/lib/mono/gnome-panel-sharp-2.24
%{_prefix}/lib/mono/gnome-print-sharp-2.18
%{_prefix}/lib/mono/gtksourceview2-sharp-2.0
%{_prefix}/lib/mono/rsvg2-sharp-2.0
#%{_prefix}/lib/mono/vte-sharp-0.16
%{_prefix}/lib/mono/wnck-sharp-2.20
%{_datadir}/gnomedesktop-sharp
#%{_datadir}/gnome-panel-sharp
%{_datadir}/gnome-print-sharp
%{_datadir}/gtksourceview2-sharp
%{_datadir}/rsvg2-sharp
#%{_datadir}/vte-sharp
%{_datadir}/wnck-sharp

%files           devel
%defattr(-,root,root,-)
%doc HACKING
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.26.0-19
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 2.26.0-18
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 2.26.0-17
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 2.26.0-16
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 2.26.0-15
- 为 Magic 3.0 重建

* Sun Oct 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.26.0-14
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Thu Feb 10 2011 Christian Krause <chkr@fedoraproject.org> - 2.26.0-13
- Disable gnome-panel bindings

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 2.26.0-11
- updated the supported arch list

* Mon Dec 20 2010 Christian Krause <chkr@fedoraproject.org> - 2.26.0-10
- Rebuilt in rawhide (FTBFS BZ 660867)
- Disable gtkhtml3 support as directed in BZ 660867, comment #9

* Sun Oct 31 2010 Christian Krause <chkr@fedoraproject.org> - 2.26.0-9
- Rebuild again to create correct requires/provides capabilities

* Sat Oct 09 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.26.0-8
- Rebuild

* Thu Jun 10 2010 Christian Krause <chkr@fedoraproject.org> - 2.26.0-7
- Rebuilt in rawhide (FTBFS BZ 600015)

* Thu Feb 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 2.26.0-6
- Fix libgnome-desktop target soname (BZ 563361)

* Mon Oct 26 2009 Dennis Gilmore <dennis@ausil.us> - 2.26.0-5
- Exclude sparc64

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> - 2.26.0-3
- Add support for ppc64

* Wed Apr 22 2009 Denis Leroy <denis@poolshark.org> - 2.26.0-2
- Rebuilt without nautilus-cd-burner (obsoleted)

* Mon Apr 06 2009 Xavier Lamien <lxtnow@gmail.com> - 2.26.0-1
- Update release.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.24.0-3
- and BR: libgnomeprintui22-devel

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.24.0-2
- add gnome-sharp-devel as BuildRequires

* Thu Oct 16 2008 Dan Winship <dwinship@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Sat Jul 05 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.20.1-2
- Obsolete standalone package gtksourceview2-sharp.

* Sat Jul 05 2008 Xavier Lamien <lxtno[at]gmail.com> - 2.20.1-1
- Initial RPM Release.
