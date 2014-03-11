# currently we have to pull directly from upstream SVN
%global svn 98
%global checkout 20120105svn%{svn}

Summary: Several GUI (Qt) programs and plug-ins for unixODBC
Name: unixODBC-gui-qt
# There has not been a formal upstream release yet and we're not
# sure what the first formal release version number will be, so using 0
Version: 0
Release: 0.6.%{checkout}%{?dist}
Group: Applications/Databases
URL: http://sourceforge.net/projects/unixodbc-gui-qt/
# Programs are GPL, libraries are LGPL
License: GPLv3 and LGPLv3

# Source code is available only in SVN by upstream, so using own
# tarball created from the last commit. SVN repository can be found at
# https://unixodbc-gui-qt.svn.sourceforge.net/svnroot/unixodbc-gui-qt
Source: %{name}-%{checkout}.tar.bz2
Source1: ODBCCreateDataSourceQ4.desktop
Source2: ODBCManageDataSourcesQ4.desktop
Source3: ODBCTestQ4.desktop

Patch1: unixODBC-gui-qt-qstring.patch
# We'd like to have the same soname version as former unixODBC-kde had
Patch2: unixODBC-gui-qt-so-version-bump.patch

BuildRequires: qt4-devel qt-assistant-adp-devel
BuildRequires: libtool libtool-ltdl-devel
BuildRequires: unixODBC-devel
BuildRequires: desktop-file-utils

# Since unixODBC-2.3.0 does not contain GUI tools anymore, we can say
# unixODBC-gui-qt obsoletes all versions of unixODBC-kde before 2.3.0
Provides: unixODBC-kde = 2.3.0-1
Obsoletes: unixODBC-kde < 2.3.0-1

%description
unixODBC-gui-qt provides several GUI (Qt) programs and plug-ins.
  * administrator (program)
  * create data source wizard (program)
  * test (program)
  * installer (plug-in)
  * auto test (plug-in)

%prep
%setup -q -n %{name}
%patch1 -p1 -b .qstring
%patch2 -p1 -b .so-version-bump

%build
# pick up qt path
export PATH="%{_qt4_bindir}:$PATH"

make -f Makefile.svn

%configure \
	--disable-static \
	--enable-ltdllib \
	--with-gnu-ld \
	--with-qt-dir-lib="%{_qt4_libdir}" \
	--with-qt-dir-bin="%{_qt4_bindir}"

make %{?_smp_mflags}

%install
# pick up qt path
export PATH="%{_qt4_bindir}:$PATH"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps

make DESTDIR=$RPM_BUILD_ROOT install

# install *.desktop files
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE2}
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE3}

# install icons used for applications in *.desktop files
install -p -m 644 ODBCDataManagerQ4/ODBC64.xpm \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/ODBCCreateDataSourceQ4.xpm
install -p -m 644 odbcinstQ4/ODBCManageDataSources64.xpm \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/ODBCManageDataSourcesQ4.xpm
install -p -m 644 ODBCTestQ4/ODBCTestQ4-48.xpm \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/ODBCTestQ4.xpm

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%files
%doc AUTHORS COPYING ChangeLog NEWS doc GPL.txt LGPL.txt
%{_bindir}/ODBCCreateDataSourceQ4
%{_bindir}/ODBCManageDataSourcesQ4
%{_bindir}/ODBCTestQ4
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_libdir}/libgtrtstQ*so*
%{_libdir}/libodbcinstQ*so*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0-0.6.20120105svn98
- 为 Magic 3.0 重建

* Wed Feb 01 2012 Honza Horak <hhorak@redhat.com> - 0-0.5.20120105svn98
- desktop files minor fixes
  Related: #768986

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> - 0-0.4.20120105svn98
- minor specfile improvements

* Thu Jan 05 2012 Honza Horak <hhorak@redhat.com> - 0-0.3.20120105svn98
- fixed issues found by Package Review process (see #767622)

* Thu Dec 15 2011 Honza Horak <hhorak@redhat.com> - 0-0.2.20111208svn95
- add Provides: unixODBC-kde to indicate unixODBC-gui-qt fills the gap after
  GUI utils are no longer part of unixODBC

* Tue Dec 13 2011 Honza Horak <hhorak@redhat.com> - 0-0.1.20111208svn95
- initial build from svn commit 95 after detachment from unixODBC project
