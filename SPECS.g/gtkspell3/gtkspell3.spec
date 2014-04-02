Name:           gtkspell3
Version:        3.0.4
Release:        1%{?dist}
Summary:        On-the-fly spell checking for GtkTextView widgets

License:        GPLv2+
URL:            http://gtkspell.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gtkspell/gtkspell3-%{version}.tar.gz

BuildRequires:  enchant-devel
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  vala-devel
BuildRequires:  vala-tools
BuildRequires:  iso-codes-devel

Requires:       iso-codes

%description
GtkSpell provides word-processor-style highlighting and replacement of
misspelled words in a GtkTextView widget as you type. Right-clicking a
misspelled word pops up a menu of suggested replacements.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-vala < 3.0.2-2

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use GtkSpell API version 3.0.

%prep
%setup -q

%build
%configure --disable-static --enable-vala
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang gtkspell3

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f gtkspell3.lang
%doc AUTHORS COPYING README
%{_libdir}/girepository-1.0/GtkSpell-3.0.typelib
%{_libdir}/libgtkspell3-3.so.*

%files devel
%doc %{_datadir}/gtk-doc/
%{_includedir}/gtkspell-3.0/
%{_libdir}/libgtkspell3-3.so
%{_libdir}/pkgconfig/gtkspell3-3.0.pc
%{_datadir}/gir-1.0/GtkSpell-3.0.gir
%{_datadir}/vala/vapi/gtkspell3-3.0.vapi
%{_datadir}/vala/vapi/gtkspell3-3.0.deps

%changelog
* Thu Sep 26 2013 Sandro Mani <manisandro@gmail.com> - 3.0.4-1
- Update to 3.0.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Sandro Mani <manisandro@gmail.com> - 3.0.3-2
- Add iso-codes requires and iso-codes-devel BR

* Tue Jun 04 2013 Sandro Mani <manisandro@gmail.com> - 3.0.3-1
- Update to 3.0.3

* Thu Mar 07 2013 Sandro Mani <manisandro@gmail.com> - 3.0.2-2
- Merge -vala into -devel package

* Wed Mar 06 2013 Sandro Mani <manisandro@gmail.com> - 3.0.2-1
- Update to 3.0.2
- Adds vala bindings

* Sat Feb 09 2013 Sandro Mani <manisandro@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Thu Nov 15 2012 Kalev Lember <kalevlember@gmail.com> - 3.0.0-1
- Initial gtkspell3 packaging, based on Fedora's gtkspell package
