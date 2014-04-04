
%define _with_gcrypt --with-gcrypt

Summary: Base libraries for GGZ gaming zone
Summary(zh_CN.UTF-8): GGZ 游戏的基本库
Name:    ggz-base-libs
Version: 0.99.5
Release: 7%{?dist}

License: LGPLv2+ and GPLv2+
Group:   System Environment/Libraries
Group(zh_CN.UTF): 系统环境/库
URL: http://www.ggzgamingzone.org/
#Source0: http://ftp.belnet.be/packages/ggzgamingzone/ggz/%{version}/ggz-base-libs-snapshot-%{version}.tar.gz
Source0: http://mirrors.ibiblio.org/pub/mirrors/ggzgamingzone/ggz/snapshots/ggz-base-libs-snapshot-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: libggz < 1:0.99.5
Provides:  libggz = 1:%{version}-%{release}

Obsoletes: ggz-client-libs < 1:0.99.5
Provides:  ggz-client-libs = 1:%{version}-%{release}

Source1: ggz.modules
# see http://fedoraproject.org/wiki/PackagingDrafts/GGZ
Source2: macros.ggz

BuildRequires: expat-devel
%{?_with_gcrypt:BuildRequires: libgcrypt-devel >= 1.4}
BuildRequires: gettext
# --with-tls broken, FIXME
#BuildRequires: gnutls-devel
BuildRequires: pkgconfig


%description
GGZ (which is a recursive acronym for GGZ Gaming Zone) develops libraries,
games and game-related applications for client-server online gaming. Player
rankings, game spectators, AI players and a chat bot are part of this effort.

%description -l zh_CN.UTF-8
GGZ 游戏的基本库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Obsoletes: libggz-devel < 1:0.99.5
Obsoletes: ggz-client-libs-devel < 1:0.99.5
Provides: libggz-devel = 1:%{version}-%{release}
Provides: ggz-client-libs-devel = 1:%{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
# %{_sysconfdir}/rpm ownership
Requires: rpm
%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-snapshot-%{version}

%if 0
# some auto*/libtool love to quash rpaths
rm -f m4/libtool.m4 m4/lt*
libtoolize -f --automake
aclocal -Im4
autoreconf -i -f
%else
# avoid lib64 rpaths, quick-n-dirty
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif
%endif


%build
%configure \
  --disable-debug \
  --disable-static \
  %{?_with_gcrypt}

## tls support disabled, for now, configure is broken wrt to these options
#  --with-tls=GnuTLS 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# GGZCONFDIR stuff
install -D -m644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/ggz.modules
mkdir -p %{buildroot}%{_sysconfdir}/ggz.modules.d
# GGZDATADIR
mkdir -p %{buildroot}%{_datadir}/ggz
# GGZGAMEDIR
mkdir -p %{buildroot}%{_libdir}/ggz
# RPM macros
install -D -m644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.ggz
magic_rpm_clean.sh
%find_lang ggzcore_snapshot-%{version}
%find_lang ggz-config
cat ggz*.lang >> all.lang

# unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig 


%clean
rm -rf %{buildroot}


%files -f all.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %{_sysconfdir}/ggz.modules
%dir %{_sysconfdir}/ggz.modules.d
# GPLv2+
%{_bindir}/ggz-config
%dir %{_datadir}/ggz
%dir %{_libdir}/ggz
%{_libdir}/libggzmod.so.4*
%{_mandir}/man5/ggz.modules.5*
# LGPLv2+
%{_libdir}/libggz.so.2*
%{_libdir}/libggzcore.so.9*
%{_mandir}/man6/ggz*
%{_mandir}/man7/ggz*
%{_sysconfdir}/xdg/menus/applications-merged/ggz.merge.menu
%{_sysconfdir}/xdg/menus/ggz.menu
%{_datadir}/desktop-directories/ggz*.directory

%files devel
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.ggz
# GPLv2+
%{_includedir}/ggzmod.h
%{_libdir}/libggzmod.so
%{_libdir}/pkgconfig/ggzmod.pc
%{_mandir}/man3/ggzmod_h.3*
# LGPLv2+
%{_includedir}/ggz.h
%{_includedir}/ggz_*.h
%{_libdir}/libggz.so
%{_libdir}/pkgconfig/libggz.pc
%{_mandir}/man3/ggz*
%{_includedir}/ggzcore.h
%{_libdir}/libggzcore.so
%{_libdir}/pkgconfig/ggzcore.pc
%{_mandir}/man3/ggzcore_h.3*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.99.5-7
- 为 Magic 3.0 重建

* Wed Nov 30 2011 Liu Di <liudidi@gmail.com> - 0.99.5-6
- 为 Magic 3.0 重建

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Rex Dieter <rdieter@fedoraproject.org> 0.99.5-4
- own %%{_sysconfdir}/ggz.modules.d
- kill rpaths (again)

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> 0.99.5-3
- conflict with ggz-client-libs, include epoch in Obsoletes/Provides: 
  libggz ggz-client-libs (#491638)

* Tue Mar 10 2009 Rex Dieter <rdieter@fedoraproject.org> 0.99.5-2
- drop --with-tls (busted), fixes f11+ build

* Fri Feb 06 2009 Rex Dieter <rdieter@fedoraproject.org> 0.99.5-1
- ggz-base-libs-snapshot-0.99.5
- Obsoletes/Provides: libggz,ggz-client-libs

* Sun Aug 24 2008 Rex Dieter <rdieter@fedoraproject.org> 0.99.4-1
- ggz-client-libs-snapshot-0.99.4

* Sun Feb 17 2008 Rex Dieter <rdieter@fedoraproject.org> 0.0.14.1-1
- ggz 0.0.14.1

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 0.0.14-6
- include %%_sysconfdir/rpm/macros.ggz

* Wed Feb 06 2008 Rex Dieter <rdieter@fedoraproject.org> 0.0.14-5
- %%config(noreplace) %%_sysconfdir/ggz.modules (#431726)
- own %%_datadir/ggz, %%_libdir/ggz

* Sat Nov 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.0.14-4
- --disable-ggzwrap (for now, until multilib, licensing is sorted out)
- move ggz-config to main pkg (runtime management of ggz modules)
- clarify GPL vs. LGPL bits
- drop BR: automake libtool

* Fri Nov 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.0.14-3
- try (no)rpath trick #2: modify configure

* Thu Nov 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.0.14-2
- libtoolize to avoid rpaths
- -devel +%%defattr

* Thu Sep 27 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.0.14-1
- cleanup

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 0.0.12-1.2
- Rebuild for Fedora Core 5.

* Sat Dec 03 2005 Dries Verachtert <dries@ulyssis.org> - 0.0.12-1
- Initial package.
