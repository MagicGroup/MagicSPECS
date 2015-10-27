Summary:	Render a planetary image into an X window
Name:		xplanet
Version:	1.3.0
Release:	3%{?dist}

License:	GPLv2+
Group:		Amusements/Graphics
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL:		http://%{name}.sourceforge.net

BuildRequires:	expat-devel
BuildRequires:	glib2-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXt-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libungif-devel
BuildRequires:	libtiff-devel
BuildRequires:	netpbm-devel
BuildRequires:	pango-devel
Requires:	gnu-free-mono-fonts

%description
Xplanet is similar to Xearth, where an image of the earth is rendered
into an X window.  Azimuthal, Mercator, Mollweide, orthographic, or
rectangular projections can be displayed as well as a window with a
globe the user can rotate interactively.  The other terrestrial
planets may also be displayed. The Xplanet home page has links to
locations with map files.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags} -k

%install
CPPROG="cp -p" make DESTDIR=%{buildroot} install

ln -sf ../fonts/gnu-free/FreeMonoBold.ttf \
	%{buildroot}%{_datadir}/%{name}/FreeMonoBold.ttf

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/xplanet

%changelog
* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.3.0-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 为 Magic 3.0 重建

* Fri Mar 30 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.3.0-1
- 1.3.0

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for c++ ABI breakage

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.2.2-3
- F-17: rebuild against gcc47

* Wed Nov  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.2.2-2
- Rebuild

* Fri Feb 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.2.2-1
- 1.2.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.1-2
- F-12: Mass rebuild

* Thu Apr 23 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.1-1
- 1.2.1

* Wed Mar 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-7
- GNU FreeFont naming change

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-6
- F-11: Mass rebuild

* Thu Feb  5 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-5
- Patch to compile with g++44

* Sun Dec 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-4
- Remove xplanet private ttf file, use system one

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Fri Jan  4 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-3
- Some misc fixes for g++43

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-2.1.dist.2
- Mass rebuild (buildID or binutils issue)

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-2.1.dist.1
- License update

* Mon Oct  2 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-2.1
- rebuild against newest gcc(-4.1.1-27 or -28)

* Fri Sep 22 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-2
- bump release

* Sat Sep 16 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.0-1
- 1.2.0
- Keep timestamps

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.1-7
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun May 11 2003 Juha Ylitalo <jylitalo@iki.fi> - 0:1.0.1-0.fdr.5
- added %%defattr so that we wouldn't get big list of user temp1 does not exist.
- added XFree86-devel into BuildRequires, since fedora build seems to lack
  dependencies to libX11 and libXext (from XFree86-libs)

* Thu May 01 2003 Juha Ylitalo <jylitalo@iki.fi> - 0:1.0.1-0.fdr.4
- appearantly removing INSTALL from %%files section was all that was needed...

* Thu May 01 2003 Juha Ylitalo <jylitalo@iki.fi> - 0:1.0.1-0.fdr.2
- fixed Group in SPEC file (to Amusements/Graphics)
- added AUTHORS, NEWS, README.config and TODO into %%files %%doc list.
- removed INSTALL from %%files
- and other minor changes based on bugzilla.fedora.us #109.

* Tue Apr 29 2003 Juha Ylitalo <jylitalo@iki.fi> - 0:1.0.1-0.fdr.1
- fixed release to match Fedora guidelines.
- ./configure to %%configure and bunch of other find-replace operations.
- added missing BuildRequires.

* Tue Apr 01 2003 Juha Ylitalo <jylitalo@iki.fi> - 0:1.0.1-1.fdr.1
- upgrade from 0.94 to 1.0.1
- fedora related changed to Hari Nair <hari@alumni.caltech.edu>'s original spec
- added patch to make my 0xf6 etc. finnish characters to show in markers.
