Name:           unique3
Version:        3.0.2
Release:        7%{?dist}
Summary:        Single instance support for applications
Summary(zh_CN.UTF-8): 应用程序的单一实例

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.gnome.org/~ebassi/source/
Source0:        http://download.gnome.org/sources/libunique/3.0/libunique-%{version}.tar.xz

BuildRequires:  gnome-doc-utils >= 0.3.2
BuildRequires:  libtool
BuildRequires:  glib2-devel >= 2.25.0
BuildRequires:  gtk3-devel >= 2.99.3
BuildRequires:  gtk-doc >= 1.11

BuildRequires: automake autoconf libtool

%description
Unique is a library for writing single instance applications, that is
applications that are run once and every further call to the same binary
either exits immediately or sends a command to the running instance.

This version of unique works with GTK+ 3.

%description -l zh_CN.UTF-8
应用程序的单一实例。

%package devel
Summary: Libraries and headers for unique3
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel
Requires: gtk3-devel

%description devel
Headers and libraries for unique3.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libunique-%{?version}

autoreconf -i -f

%build
%configure --enable-gtk-doc --disable-static --enable-introspection=no
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc
%{_includedir}/unique-3.0/
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 3.0.2-7
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 3.0.2-6
- 为 Magic 3.0 重建

* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 3.0.2-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.0.2-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 3.0.2-2
- Rebuild for new libpng

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-4
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-2
- Rebuild against newer gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-4
- Rebuild against newer gtk

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-3
- Rebuild against newer gtk3

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-2
- Co-own /usr/share/gtk-doc (#604415)

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-1
- Initial packaging
