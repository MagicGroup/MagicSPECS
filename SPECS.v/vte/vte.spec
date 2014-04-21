%define glib2_version 2.26.0
%define pango_version 1.22.0
%define gtk2_version 2.20.0

Name: vte
Version:	0.36.0
Release: 1%{?dist}
Summary: A terminal emulator
License: LGPLv2+
Group: User Interface/X
#VCS: git:git://git.gnome.org/vte
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/vte/%{majorver}/%{name}-%{version}.tar.xz

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pygtk2-devel, python-devel, ncurses-devel
BuildRequires: gettext
BuildRequires: libXt-devel
BuildRequires: intltool

# initscripts creates the utmp group
Requires: initscripts

%description
VTE is a terminal emulator widget for use with GTK+ 2.0.

%package devel
Summary: Files needed for developing applications which use vte
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel
Requires: ncurses-devel
Requires: pkgconfig
Requires: pygtk2-devel

%description devel
The vte-devel package includes the header files and developer docs
for the vte package.

Install vte-devel if you want to develop programs which will use
vte.

%prep
%setup -q

%build
PYTHON=%{_bindir}/python`%{__python} -c "import sys ; print sys.version[:3]"`
export PYTHON
%configure \
        --enable-shared \
        --enable-static \
        --with-gtk=2.0 \
        --libexecdir=%{_libdir}/%{name} \
        --without-glX \
        --disable-gtk-doc
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove the .a and .la file.
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib%{name}*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/lib%{name}*.la

# Remove static python modules and la files, which are probably useless to Python anyway.
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/gtk-2.0/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/gtk-2.0/*.a
magic_rpm_clean.sh
%find_lang vte-2.90

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f vte-2.90.lang
%defattr(-,root,root)
%doc COPYING HACKING NEWS README
%doc src/iso2022.txt
%doc doc/utmpwtmp.txt doc/boxes.txt doc/openi18n/UTF-8.txt doc/openi18n/wrap.txt
%{_libdir}/*.so.*
%dir %{_libdir}/vte
%attr(2711,root,utmp) %{_libdir}/vte/gnome-pty-helper
#%{_libdir}/python*/site-packages/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_sysconfdir}/profile.d/vte.sh
%{_bindir}/vte2_90
#%{_datadir}/pygtk/2.0/defs/vte.defs
%doc %{_datadir}/gtk-doc/html/vte-2.90

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.36.0-1
- 更新到 0.36.0

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.28.2-1
- 更新到 0.28.2

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.28.2-3
- 为 Magic 3.0 重建

* Wed Nov 21 2012 Liu Di <liudidi@gmail.com> - 0.28.2-2
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.28.2-1
- Update to 0.28.2


