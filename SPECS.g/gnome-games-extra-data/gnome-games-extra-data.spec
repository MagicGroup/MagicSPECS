
Summary: Additional data for gnome-games
Name: gnome-games-extra-data
Version: 3.2.0
Release: 2%{?dist}
License: GPL+
Group: Amusements/Games
#VCS: git:git://git.gnome.org/gnome-games-extra-data
Source: http://download.gnome.org/sources/gnome-games-extra-data/3.2/gnome-games-extra-data-%{version}.tar.xz
URL: http://www.gnome.org
BuildArch: noarch
Requires: gnome-games >= 2.18.0-3.fc7

%description
The gnome-games-extra-data package includes additional data
and themes for the games in the gnome-games package.

%prep
%setup -q

%build
%configure
make %{_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# We don't ship gnometris
rm -rf $RPM_BUILD_ROOT%{_datadir}/pixmaps/gnometris


%files
%doc AUTHORS COPYING README NEWS
%{_datadir}/gnome-games/glines/pixmaps/*
%{_datadir}/gnome-games/gnobots2/themes/*
%{_datadir}/gnome-games/iagno/pixmaps/*
%{_datadir}/gnome-games/mahjongg/pixmaps/*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.2.0-2
- 为 Magic 3.0 重建

* Wed Sep  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Apr  4 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Adam Tkac <atkac redhat com> - 2.30.0-2
- append the dist tag

* Wed Mar 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Sep 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Own some directories (#474648)

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Tweak %%summary

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Wed Mar 26 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Sat Feb  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Jul 31 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-2
- Update to 2.18.0
- Drop dist tag, since this is a pure data package

* Wed Mar 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-2
- Incorporate review feedback

* Wed Mar 28 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Initial build

