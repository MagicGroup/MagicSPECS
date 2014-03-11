Name:           seed
Version:        3.2.0
Release:        4%{?dist}.2
Summary:        GNOME JavaScript interpreter

Group:          Development/Languages
License:        LGPLv3+
URL:            http://live.gnome.org/Seed
Source0:        http://ftp.gnome.org/pub/gnome/sources/seed/3.1/seed-%{version}.tar.xz
# Seed.js multilib fix
Patch0:         seed-3.0.0-multilib.patch

BuildRequires:  intltool
BuildRequires:  mpfr-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(gnome-js-common)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(webkitgtk-3.0)
BuildRequires:  gtk-doc

Requires:       gnome-js-common

%description
Seed is a library and interpreter, dynamically bridging (through
GObjectIntrospection) the WebKit JavaScriptCore engine, with the GNOME
platform. Seed serves as something which enables you to write
standalone applications in JavaScript, or easily enable your
application to be extensible in JavaScript.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
The %{name}-doc package contains documentation for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .multilib

# add lib64 to dlsearch_path_spec
sed -i.libdir_syssearch -e \
  '/sys_lib_dlsearch_path_spec/s|/lib /usr/lib |/lib /lib64 /usr/lib /usr/lib64 |' \
  configure
sed -i.cflags -e \
  's|^\([ \t][ \t]*\)CFLAGS=\"[^\$].*$|\1true|' \
  configure

# remove unneeded shebang
(cd extensions &&
    touch -r repl.js{,.timestamp} &&
    sed -i '1,2d' repl.js &&
    touch -r repl.js{.timestamp,} &&
    rm repl.js.timestamp)


%build
%configure \
%if 0%{?fedora} > 14 || 0%{?rhel} > 6
  --with-webkit=3.0
%else
  --with-webkit=1.0
%endif
make V=1 %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

# grab developer docs
mv $RPM_BUILD_ROOT%{_docdir}/seed devdocs
# remove files already bundled with main package
rm devdocs/{AUTHORS,COPYING,INSTALL,README}
magic_rpm_clean.sh

%check
# currently tests the installed version of seed, and requires X
#make check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/seed
%{_libdir}/*.so.*
%{_libdir}/seed-gtk3
%{_datadir}/seed-gtk3
%{_datadir}/man/man1/seed.1.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/seed-gtk3
%{_libdir}/pkgconfig/seed.pc
%{_libdir}/*.so

%files doc
%defattr(-,root,root,-)
%doc devdocs/*
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/seed


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.2.0-4.2
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.2.0-1.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 3.2.0-1.1
- rebuild with new gmp

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Sun Aug  7 2011 Michel Salim <salimma@fedoraproject.org> - 3.1.1-2
- Multilib fix: Seed.js now searches both lib64 and lib directories
- Documentation subpackage no longer depends on gtk-doc (# 707571)

* Sun Jul 31 2011 Michel Salim <salimma@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Sun Apr  3 2011 Christopher Aillon <caillon@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.91-7
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.91-5
- Rebuild against newer gtk

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 2.31.91-4
- Rebuild against newer gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-3
- Rebuild against newer gtk

* Fri Nov  5 2010 Michel Salim <salimma@fedoraproject.org> - 2.31.91-2
- Only build against GTK+ 3.0 on Fedora > 14

* Wed Sep 29 2010 Colin Walters <walters@verbum.org> - 2.31.91-1
- New upstream version

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.31.1-3
- Rebuild against new gobject-introspection

* Mon Jul  5 2010 Michel Salim <salimma@fedoraproject.org> - 2.31.1-2
- Rebuild for webkitgtk soname change

* Tue Jun 22 2010 Michel Salim <salimma@fedoraproject.org> - 2.31.1-1
- Update to 2.31.1

* Fri Jun 18 2010 Michel Salim <salimma@fedoraproject.org> - 2.30.0-2
- Incorporate review recommendations (bz #600638)
- Remove unneeded shebang in repl.js
- Make -doc noarch

* Mon Mar 29 2010 Michel Salim <salimma@fedoraproject.org> - 2.30.0-1
- Initial package
