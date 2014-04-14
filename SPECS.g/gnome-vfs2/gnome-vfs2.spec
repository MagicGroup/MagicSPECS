%define po_package gnome-vfs-2.0

# don't use HAL from F-16 on
%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%bcond_with hal
%else
%bcond_without hal
%endif

Summary: The GNOME virtual file-system libraries
Summary(zh_CN.UTF-8): GNOME 虚拟文件系统库
Name: gnome-vfs2
Version: 2.24.4
Release: 16%{?dist}
License: LGPLv2+ and GPLv2+
# the daemon and the library are LGPLv2+
# the modules are LGPLv2+ and GPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
#VCS: git:git://git.gnome.org/gnome-vfs
Source0: http://download.gnome.org/sources/gnome-vfs/2.24/gnome-vfs-%{version}.tar.bz2
URL: http://www.gnome.org/
Requires(post): GConf2 
Requires(pre): GConf2 
Requires(preun): GConf2 
BuildRequires: GConf2-devel 
BuildRequires: libxml2-devel, zlib-devel
BuildRequires: glib2-devel 
BuildRequires: popt, bzip2-devel, ORBit2-devel, openjade
BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: autoconf
BuildRequires: gtk-doc 
BuildRequires: perl-XML-Parser 
BuildRequires: libsmbclient-devel 
BuildRequires: openssl-devel gamin-devel
BuildRequires: krb5-devel
BuildRequires: pkgconfig(avahi-client) pkgconfig(avahi-glib)
%if %{with hal}
BuildRequires: hal-devel
%endif
BuildRequires: dbus-devel 
BuildRequires: dbus-glib-devel 
BuildRequires: gettext
BuildRequires: libacl-devel
BuildRequires: keyutils-libs-devel
# For gvfs-open
Requires: gvfs

Patch3: gnome-vfs-2.9.90-modules-conf.patch

# remove gnome-mime-data dependency
Patch4: gnome-vfs-2.24.1-disable-gnome-mime-data.patch

# CVE-2009-2473 neon, gnome-vfs2 embedded neon: billion laughs DoS attack
# https://bugzilla.redhat.com/show_bug.cgi?id=518215
Patch5: gnome-vfs-2.24.3-CVE-2009-2473.patch

# send to upstream
Patch101:	gnome-vfs-2.8.2-schema_about_for_upstream.patch

# Default
Patch104:	gnome-vfs-2.8.2-browser_default.patch

# Applied upstream.
# Patch201: gnome-vfs-2.8.1-console-mount-opt.patch

# RH bug #197868
Patch6: gnome-vfs-2.15.91-mailto-command.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=333041
# https://bugzilla.redhat.com/show_bug.cgi?id=335241
Patch300: gnome-vfs-2.20.0-ignore-certain-mountpoints.patch


# backported from upstream

# gnome-vfs-daemon exits on dbus, and constantly restarted causing dbus/hal to hog CPU
# https://bugzilla.redhat.com/show_bug.cgi?id=486286
Patch404: gnome-vfs-2.24.xx-utf8-mounts.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=435653
Patch405: 0001-Add-default-media-application-schema.patch

# from upstream
Patch7: gnome-vfs-2.24.5-file-method-chmod-flags.patch

# fix compilation against new glib2
Patch8: gnome-vfs-2.24.4-enable-deprecated.patch


%description
GNOME VFS is the GNOME virtual file system. It is the foundation of
the Nautilus file manager. It provides a modular architecture and
ships with several modules that implement support for file systems,
http, ftp, and others. It provides a URI-based API, backend
supporting asynchronous file operations, a MIME type manipulation
library, and other features.

%description -l zh_CN.UTF-8
GNOME 虚拟文件系统库。

%package devel
Summary: Libraries and include files for developing GNOME VFS applications
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries for writing
GNOME VFS modules and applications that use the GNOME VFS APIs.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package smb
Summary: Windows fileshare support for gnome-vfs
Summary(zh_CN.UTF-8): %{name} 的 Windows 文件共享支持
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:   %{name} = %{version}-%{release}
Requires: libsmbclient

%description smb
This package provides support for reading and writing files on windows
shares (SMB) to applications using GNOME VFS.

%description smb -l zh_CN.UTF-8
%{name} 的 Windows 文件共享支持。

%prep
%setup -q -n gnome-vfs-%{version} 

%patch3 -p1 -b .modules-conf
%patch4 -p1 -b .mime-data
%patch5 -p1 -b .CVE-2009-2473

%patch6 -p1 -b .mailto-command
%patch7 -p1 -b .file-method-chmod-flags
%patch8 -p1 -b .enable-deprecated

# send to upstream
%patch101 -p1 -b .schema_about

%patch104 -p1 -b .browser_default

%patch300 -p1 -b .ignore-certain-mount-points

%patch404 -p1 -b .utf8-mounts

%patch405 -p1 -b .default-media

# for patch 10 and 4
libtoolize --force  || :
aclocal  || :
autoheader  || :
automake --add-missing || :
autoconf  || :

%build
if pkg-config openssl ; then
	CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
	LDFLAGS=`pkg-config --libs-only-L openssl`; export LDFLAGS
fi

CFLAGS="%optflags -fno-strict-aliasing" %configure \
    --with-samba-includes=/usr/include/samba-4.0 \
    --disable-gtk-doc \
%if %{with hal}
    --enable-hal \
%endif
    --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

# strip unneeded translations from .mo files
# ideally intltool (ha!) would do that for us
# http://bugzilla.gnome.org/show_bug.cgi?id=474987
cd po
grep -v ".*[.]desktop[.]in[.]in$\|.*[.]server[.]in[.]in$" POTFILES.in > POTFILES.keep
mv POTFILES.keep POTFILES.in
intltool-update --pot
PO_FAKE_DATE="2009-08-03 18:00+0200"   # fake this to be equal in every build
PO_FAKE_DATE_EXPR='\(.*POT-Creation-Date: *\)\(.*\)\(\\n.*\)'
sed --in-place "s/${PO_FAKE_DATE_EXPR}/\1${PO_FAKE_DATE}\3/" %{po_package}.pot
for p in *.po; do
  msgmerge $p %{po_package}.pot > $p.out
  msgfmt -o `basename $p .po`.gmo $p.out
done


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{po_package}


%post
/sbin/ldconfig
%gconf_schema_upgrade system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%pre
%gconf_schema_prepare system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%preun
%gconf_schema_remove system_http_proxy system_dns_sd system_smb desktop_gnome_url_handlers desktop_default_applications

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-, root, root, -)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%dir %{_sysconfdir}/gnome-vfs-2.0
%dir %{_sysconfdir}/gnome-vfs-2.0/modules
%config %{_sysconfdir}/gnome-vfs-2.0/modules/*.conf
%exclude %{_sysconfdir}/gnome-vfs-2.0/modules/smb-module.conf
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%exclude %{_libdir}/gnome-vfs-2.0/modules/libsmb.so
%{_libdir}/gnome-vfs-2.0/modules
%dir %{_libdir}/gnome-vfs-2.0
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/dbus-1/services/gnome-vfs-daemon.service

%files devel
%defattr(-, root, root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_libdir}/gnome-vfs-2.0/include
%{_includedir}/*
%{_datadir}/gtk-doc/html/gnome-vfs-2.0

%files smb
%defattr(-, root, root,-)
%{_libdir}/gnome-vfs-2.0/modules/libsmb.so
%config %{_sysconfdir}/gnome-vfs-2.0/modules/smb-module.conf

%changelog
* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 2.24.4-16
- 为 Magic 3.0 重建

* Sat Apr 12 2014 Liu Di <liudidi@gmail.com> - 2.24.4-15
- 为 Magic 3.0 重建


