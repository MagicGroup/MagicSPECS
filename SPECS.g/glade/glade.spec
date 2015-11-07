Name:           glade
Version:	3.19.0
Release:        3%{?dist}
Summary:        User Interface Designer for GTK+ and GNOME
Summary(zh_CN.UTF-8): GTK+ 和 GNOME 的用户界面设计器

# - /usr/bin/glade is GPLv2+
# - /usr/bin/glade-previewer is LGPLv2+
# - libgladeui-2.so, libgladegtk.so, and libgladepython.so all combine
#   GPLv2+ and LGPLv2+ code, so the resulting binaries are GPLv2+
License:        GPLv2+ and LGPLv2+
URL:            http://glade.gnome.org/
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glade/%{majorver}/glade-%{version}.tar.xz

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libxml2-devel
BuildRequires:  pygobject3-devel
BuildRequires:  python2-devel

Requires:       %{name}-libs = %{version}-%{release}
# The gtk3 version of glade was packaged under the name of 'glade3' for a
# while. However, following upstream naming, 'glade3' package is now the gtk2
# version and 'glade' package is the gtk3 one. The obsoletes are here to
# provide seamless upgrade path from the gtk3 based 'glade3'.
Obsoletes:      glade3 < 1:3.11.0-3

%description
Glade is a RAD tool to enable quick and easy development of user interfaces for
the GTK+ toolkit and the GNOME desktop environment.

The user interfaces designed in Glade are saved as XML, which can be used in
numerous programming languages including C, C++, C#, Vala, Java, Perl, Python,
and others.

%description -l zh_CN.UTF-8
这是一个快速开发工具，它可以快速的开发 GTK+ 和 GNOME 的用户界面。
开发出的界面保存为 XML，可以让包括 C,C++, C#, Vala, Java, Perl, 
Python 等在内的语言使用。

%package libs
Summary:        Widget library for Glade UI designer
Summary(zh_CN.UTF-8): %{name} 的运行库
Obsoletes:      glade3-libgladeui < 1:3.11.0-3

%description    libs
The %{name}-libs package consists of the widgets that compose the Glade GUI as
a separate library to ease the integration of Glade into other applications.

%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%package devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}-libs = %{version}-%{release}
Obsoletes:      glade3-libgladeui-devel < 1:3.11.0-3

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use Glade widget library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --disable-static

# Omit unused direct shared library dependencies.
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}


%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -delete

# Remove rpaths.
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/glade*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/glade/modules/*.so
magic_rpm_clean.sh
%find_lang glade --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/glade.desktop


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files -f glade.lang
%doc AUTHORS COPYING* NEWS README
%{_bindir}/glade
%{_bindir}/glade-previewer
%{_datadir}/applications/glade.desktop
%{_datadir}/icons/hicolor/*/apps/glade.png

%files libs
%doc COPYING*
%{_libdir}/girepository-1.0/Gladeui-2.0.typelib
%dir %{_libdir}/glade/
%dir %{_libdir}/glade/modules/
%{_libdir}/glade/modules/libgladegtk.so
%{_libdir}/glade/modules/libgladepython.so
%{_libdir}/libgladeui-2.so.*
%{_datadir}/glade/
%{_datadir}/appdata/glade.appdata.xml
%{_mandir}/man1/glade-previewer.1*
%{_mandir}/man1/glade.1*

%files devel
%{_includedir}/libgladeui-2.0/
%{_libdir}/libgladeui-2.so
%{_libdir}/pkgconfig/gladeui-2.0.pc
%{_datadir}/gir-1.0/Gladeui-2.0.gir
%doc %{_datadir}/gtk-doc/

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.19.0-3
- 更新到 3.19.0

* Wed Apr 09 2014 Liu Di <liudidi@gmail.com> - 3.18.1-2
- 更新到 3.18.1

* Tue Apr 08 2014 Liu Di <liudidi@gmail.com> - 3.14.3-2
- 更新到 3.14.3

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.14.1-2
- 为 Magic 3.0 重建

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0
- Remove the unrecognized --disable-scrollkeeper option

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.13.0-1
- Update to 3.13.0

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Thu Apr 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-3
- Update the spec file comments about licensing and simplify the License tag
- Install the typelib in -libs subpackage

* Fri Apr 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Review fixes (#806093)
- Use find_lang --with-gnome for including help files
- Include license files also in the main package in addition to -libs

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.11.0-1
- Initial packaging based on Fedora glade3
- Rename the package to glade; added obsoletes for upgrade path
- Spec clean up for review
