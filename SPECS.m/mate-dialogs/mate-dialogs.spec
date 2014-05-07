Name:           mate-dialogs
Version:        1.8.0
Release:        2%{?dist}
Summary:        Displays dialog boxes from shell scripts
License:        LGPLv2+ and GPLv2+
URL:            http://mate-desktop.org

# To generate tarball
# wget http://git.mate-desktop.org/%%{name}/snapshot/%%{name}-{_internal_version}.tar.xz -O %%{name}-%%{version}.git%%{_internal_version}.tar.xz
#Source0: http://raveit65.fedorapeople.org/Mate/git-upstream/%{name}-%{version}.git%{_internal_version}.tar.xz

Source0:        http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz

BuildRequires:  gtk2-devel
BuildRequires:  mate-common
BuildRequires:  libnotify-devel
BuildRequires:  yelp-tools

%description
Displays dialog boxes from shell scripts.

%prep
%setup -q

%build
%configure --with-gtk=2.0

make %{?_smp_mflags} V=1


%install
%{make_install}

%find_lang %{name} --with-gnome --all-name


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/matedialog
%{_mandir}/man1/*
%{_datadir}/matedialog


%changelog
* Sat Apr 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- remove obsolete --disable-scrollkeeper configure flag
- add --with-gnome --all-name for find language

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Nov 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to 1.6.2 release

* Tue Oct 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.1.git59337c9
- update to latest git snapshot
- fix rhbz (#1024317)

* Wed Oct 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1 release
- gdialogs is removed
- use modern 'make install' macro
- remove needless BR rarian-compat
- remove --with-gnome from find language
- remove NOCONFIGURE=1 ./autogen.sh
- remove non-supported --disable-static configure flag

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Tue Mar 12 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-2
- Add libmatenotify-devel to BR

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- change build requires style
- fix directory ownership

* Sat Aug 11 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove unnecessary require fields, update description, make package own mate and matedialog datadirs and add V=1 to make field.

* Sun Aug 5 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
