%global avahi_version   0.6
%global soup_version    2.3
%global gtk2_version    2.10
%global glib2_version   2.15.1
%global gnutls_version  1.4
%global uuid_version    1.36

Name:           libepc
Version:	0.4.4
Release:        3%{?dist}
Summary:        Easy Publish and Consume library
Summary(zh_CN.UTF-8): 简易发布和使用库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://live.gnome.org/libepc/
Source0:        http://download.gnome.org/sources/%{name}/0.4/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libuuid-devel >= %{uuid_version}
BuildRequires:  libsoup-devel >= %{soup_version}
BuildRequires:  avahi-ui-devel >= %{avahi_version}
BuildRequires:  gnutls-devel >= %{gnutls_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  perl(XML::Parser)
BuildRequires:  intltool


%description
A library to easily publish and consume values on networks

%description -l zh_CN.UTF-8
在网络上发布和使用值的简易库。

%package        ui
Summary:        Widgets for %{name}
Summary(zh_CN.UTF-8): %{name} 的部件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    ui
The %{name}-ui package contains widget for use with %{name}.

%description ui -l zh_CN.UTF-8
%{name} 的部件。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui%{?_isa} = %{version}-%{release}
Requires:       libuuid-devel >= %{uuid_version}
Requires:       avahi-ui-devel%{?_isa} >= %{avahi_version}
Requires:       libsoup-devel%{?_isa} >= %{soup_version}
Requires:       gnutls-devel%{?_isa} >= %{gnutls_version}
Requires:       gtk2-devel%{?_isa} >= %{gtk2_version}
Requires:       glib2-devel%{?_isa} >= %{glib2_version}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
%configure --enable-static=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%post ui -p /sbin/ldconfig


%postun ui -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/%{name}-1.0.so.*


%files ui
%defattr(-,root,root,-)
%{_libdir}/%{name}-ui-1.0.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-ui-1.0/
%{_includedir}/%{name}-1.0/
%{_libdir}/%{name}-1.0.so
%{_libdir}/%{name}-ui-1.0.so
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_libdir}/pkgconfig/%{name}-ui-1.0.pc
%{_datadir}/gtk-doc/html/%{name}-1.0/


%changelog
* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 0.4.4-3
- 更新到 0.4.4

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.0-3
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.0-2
- Rebuild for new libpng

* Fri Aug 05 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 0.4.0-1
- upstream 0.4.0
- reenable compilation with %%{?_smp_mflags}
- spec cleanup

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 24 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.3.11-1
- Update to 0.3.11.

* Tue Sep 29 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-3
- Add BR on libuuid-devel, and drop BR on e2fsprogs-devel.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun  5 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9.

* Fri Oct 24 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8.
- Drop build patch.  Fixed upstream.

* Sat Sep 20 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.5-3
- Add patch to fix building from source.

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> - 0.3.5-2
- rebuild with new gnutls

* Tue Apr 22 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.5-1
- Update to 0.3.5.

* Thu Feb 14 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-3
- Rebuild for new libsoup.

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-2
- Rebuild for gcc-4.3.

* Tue Jan 29 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.4-1
- Update to 0.3.4.
- Add BR on perl-xml-parser & gettext.
- Bump min version of libsoup.

* Tue Jan 15 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3.

* Tue Dec 18 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1.
- drop pk-config patch. fixed upstream.

* Sat Dec  8 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.0-3
- Remove rpath.
- Add requires for gtk2-devel to -devel.

* Sat Dec  8 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.0-2
- Merge ui-devel into devel.
- Add patch to fix .pc files.
- Add requires for gnutls-devel to -devel.
- keep timestamp on installed files.

* Tue Dec  4 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.3.0-1
- Intial Fedora spec.
