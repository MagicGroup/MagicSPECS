Summary: Free client libraries and binaries for the NX protocol
Name: freenx-client
Version: 0.9
Release: 15%{?dist}
License: GPLv2+
Group: Applications/Internet
URL: http://freenx.berlios.de/
Source0: http://download.berlios.de/freenx/%{name}-%{version}.tar.bz2
Source1: qtnx.desktop
Patch0: freenx-client-0.9-fixes.patch
Patch1: freenx-client-0.9-includes.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf >= 2.59c, automake >= 1.10, libtool
BuildRequires: gcc-c++
# temporary until we split nx
#BuildRequires: %{_pkglibdir}/libXcomp.so.3
#Requires: nxssh, nxproxy
BuildRequires: dbus-devel
BuildRequires: doxygen
BuildRequires: qt4-devel
BuildRequires: desktop-file-utils
Requires: nxcl, qtnx

%description
NX is an exciting new technology for remote display. It provides near
local speed application responsiveness over high latency, low
bandwidth links.

FreeNX-client contains client libraries and executables for connecting
to an NX server.

%package -n nxcl
Summary: A library for building NX clients
Group: Applications/Internet

%description -n nxcl
Based on nxclientlib by George Wright, but with all dependencies on Qt
removed and the Qt build system replaced with GNU autotools.

A binary, called nxcl - the "nxcl dbus daemon" links to libnxcl and
can negotiate an nx connection.

%package -n nxcl-devel
Summary: Development files for building against the nxcl package
Group: Development/Libraries
Requires: nxcl, pkgconfig

%description -n nxcl-devel
This package provides the files necessary for development against
nxcl. Use this package if you need to build a package depending on
nxcl at build time, or if you want to do your own development
against nxcl.


%package -n qtnx
Summary: A Qt-based NX client linking to nxcl
Group: System Environment/Libraries
Requires: %{_bindir}/nxssh, %{_bindir}/nxproxy

%description -n qtnx
This is an update of the experimental QtNX client which was based on the
now deprecated NXClientLib backend library. This is an experimental port
to Seb James' nxcl library.

%prep
%setup -q
%patch0 -p1 -b .fixes
%patch1 -p0 -b .includes
cat >> qtnx/qtnx.pro << EOF
QMAKE_CXXFLAGS += -I`pwd`/nxcl/lib
LIBS += -L`pwd`/nxcl/lib -lnxcl
EOF

%build
cd nxcl
autoreconf -is
%configure --disable-static
make
cd ../qtnx
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
PATH=`pkg-config --variable=bindir Qt`:$PATH
qmake
make

%install
rm -rf %{buildroot}
make -C nxcl install DESTDIR=%{buildroot} docdir=%{_defaultdocdir}/nxcl-%{version}/nxcl
install -p -m 0755 qtnx/qtnx %{buildroot}%{_bindir}/
desktop-file-install --vendor="freenx"                    \
  --dir=%{buildroot}%{_datadir}/applications              \
  %{SOURCE1}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

%files -n nxcl
%defattr(-,root,root,-)
%doc nxcl/README
%{_bindir}/libtest
%{_bindir}/notQttest
%{_bindir}/nxcl
%{_bindir}/nxcmd
%{_libdir}/libnxcl.so.*

%files -n nxcl-devel
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/nxcl-%{version}
%{_includedir}/nxcl
%{_libdir}/libnxcl.so
%exclude %{_libdir}/libnxcl.la
%{_libdir}/pkgconfig/nxcl.pc

%files -n qtnx
%defattr(-,root,root,-)
%doc qtnx/README
%{_bindir}/qtnx
%{_datadir}/applications/*qtnx.desktop

%changelog
* Tue Jul 31 2012 Jon Ciesla <limburgher@gmail.com> - 0.9-15
- Fix FTBFS.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-13
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-9
- Split package into several subpackages.
- Add some patches from CentOS (multiple-id-key & mode 0660 for key).
- Use some patches from up to svn 545 (dated 2008-07-10).

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-8
- qt4-devel is a more precise dependency than qt-devel.

* Thu Apr 10 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-7
- Fix description.
- Remove devel files and embedded *-devel Provides:.
- Create a desktop file for qtnx.

* Sat Mar 29 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.9-6
- Split off client part into freenx-client.

* Mon Dec 31 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.1-4
- Apply Jeffrey J. Kosowsky's patches to enable multimedia and
  file/print sharing support (Fedora bug #216802).
- Silence %%post output, when openssh's server has never been started
  before (Fedora bug #235592).
- Add dependency on which (Fedora bug #250343).

* Mon Dec 10 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-3
- Fix syntax error in logrotate file, BZ 418221.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-2
- Added logrotate, BZ 379761.

* Mon Nov 19 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.1-1
- Update to 0.7.1, many bugfixes, BZ 364751, 373771.

* Sun Sep 23 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.7.0-2
- Do not try to set up KDE_PRINTRC if ENABLE_KDE_CUPS is not 1, deal better
  with errors when it is (#290351).

* Thu Sep 6 2007 Jon Ciesla <limb@jcomserv.net> - 0.7.0-1
- CM = Christian Mandery mail@chrismandery.de,  BZ 252976
- Version bump to 0.7.0 upstream release (CM)
- Fixed download URL (didn't work, Berlios changed layout). (CM)
- Changed license field from GPL to GPLv2 in RPM. (CM)
- Fixed release.

* Mon Feb 19 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.6.0-9
- Update to 0.6.0.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.4.

* Sat Jul 30 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.2.

* Sat Jul  9 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.4.1.

* Tue Mar 22 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.1
- Updated to 0.3.1 release

* Tue Mar 08 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.3.0
- Updated to 0.3.0 release
- Removed home directory patch as it is now default

* Mon Feb 14 2005 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.8
- Updated to 0.2.8 release
- Fixes some security issues
- Added geom-fix patch for windows client resuming issues

* Thu Dec 02 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.7
- Fixed package removal not removing the var session directories

* Tue Nov 23 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.7
- Updated to 0.2.7 release
- fixes some stability issues with 0.2.6

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.6
- Fixed a problem with key backup upon removal

* Fri Nov 12 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.6
- Updated to 0.2.6 release
- Changed setup to have nx user account added as a system account.
- Changed nx home directory to /var/lib/nxserver/nxhome

* Thu Oct 14 2004 Rick Stout <zipsonic[AT]gmail.com> - 0:0.2.5
- updated package to 0.2.5 release
- still applying patch for netcat and useradd

* Fri Oct 08 2004 Rick Stout <zipsonic[AT]gmail.com> - 3:0.2.4
- Added nxsetup functionality to the rpm
- patched nxsetup (fnxncuseradd) script for occasional path error.
- Added patch (fnxncuseradd) to resolve newer client connections (netcat -> nc)
- Changed name to be more friendly (lowercase)
- Added known dependencies

* Thu Sep 30 2004 Rick Stout <zipsonic[AT]gmail.com> - 2:0.2.4
- Patch (fnxpermatch) to fix permissions with key generation

* Wed Sep 29 2004 Rick Stout <zipsonic[AT]gmail.com> - 1:0.2.4
- Initial Fedora RPM release.
- Updated SuSE package for Fedora
