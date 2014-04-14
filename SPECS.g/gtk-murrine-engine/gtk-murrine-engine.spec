Summary: Murrine GTK2 engine
Summary(zh_CN.UTF-8): Murrine GTK2 引擎
Name: gtk-murrine-engine
Version: 0.98.2
Release: 5%{?dist}
License: LGPLv2 or LGPLv3
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.cimitan.com/murrine/
Source0: http://ftp.gnome.org/pub/GNOME/sources/murrine/0.98/murrine-%{version}.tar.xz
Source10: http://cimi.netsons.org/media/download_gallery/MurrinaFancyCandy.tar.bz2
Source11: http://cimi.netsons.org/media/download_gallery/MurrinaVerdeOlivo.tar.bz2
Source12: http://cimi.netsons.org/media/download_gallery/MurrinaAquaIsh.tar.bz2
Source13: http://cimi.netsons.org/media/download_gallery/MurrinaGilouche.tar.bz2
Source14: http://cimi.netsons.org/media/download_gallery/MurrinaLoveGray.tar.bz2
Source15: http://cimi.netsons.org/media/download_gallery/MurrineThemePack.tar.bz2
BuildRequires: gtk2-devel intltool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Murrine Engine is a Gtk2 theme engine, using the Cairo vector graphics
library. It comes by default with a modern glassy look, inspired by
Venetian glass artworks, and is extremely customizable.

%description -l zh_CN.UTF-8
这是一个 GTK2 主题引擎，使用 Cairo 向量图形库。它有玻璃外观，并高度可定制。

%prep
%setup -q -n murrine-%{version}

%build
%configure --enable-animation --enable-animationrtl
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/themes
(cd $RPM_BUILD_ROOT/%{_datadir}/themes;
bzcat %{SOURCE10} | tar -xvf -;
bzcat %{SOURCE11} | tar -xvf -;
bzcat %{SOURCE12} | tar -xvf -;
bzcat %{SOURCE13} | tar -xvf -;
bzcat %{SOURCE14} | tar -xvf -;
bzcat %{SOURCE15} | tar -xvf -;
)

#remove .la files
find $RPM_BUILD_ROOT -name *.la | xargs rm -f || true
#fix permission
find $RPM_BUILD_ROOT/%{_datadir}/themes -type f | xargs chmod 0644 || true
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING.2.1 NEWS
%{_libdir}/gtk-2.0/*/engines/*
%{_datadir}/gtk-engines
%{_datadir}/themes/*

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.98.2-5
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.98.2-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Martin Sourada <mso@fedoraproject.org> - 0.98.2-1
- Update to new upstream release (bugfix release)
- Fix build with newer glib

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.98.1.1-3
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Martin Sourada <mso@fedoraproject.org> - 0.98.1.1-1
- Update to 0.98.1.1
- License change to LGPLv2.1 and LGPLv3

* Wed Sep 29 2010 jkeating - 0.98.0-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Martin Sourada <mso@fedoraproject.org> - 0.98.0-1
- Update to 0.98.0

* Thu Nov 12 2009 Martin Sourada <mso@fedoraproject.org> - 0.90.3-3
- Don't own %%{_datadir}/themes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Michel Salim <salimma@fedoraproject.org> - 0.90.3-1
- Update to 0.90.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.53.1-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.53.1-2
- Autorebuild for GCC 4.3

* Sun May 20 2007 Leo Shidai Liu <sdl.web@gmail.com> 0.53.1-1
- 0.53.1

* Thu Apr  5 2007 Leo, Shidai Liu <sdl.web@gmail.com> 0.52-1
- 0.52

* Thu Mar 15 2007 Leo, Shidai Liu <sdl.web@gmail.com> 0.51-2
- fix last change

* Thu Mar 15 2007 Leo, Shidai Liu <sdl.web@gmail.com> 0.51-1
- 0.51

* Fri Jan 12 2007 Shidai Liu, Leo <sdl.web@gmail.com> 0.41-1
- 0.41

* Wed Jan 10 2007 Shidai Liu, Leo <sdl.web@gmail.com> 0.40.1-1
- 0.40.1

* Fri Nov 24 2006 Shidai Liu, Leo <sdl.web@gmail.com> 0.31-4
- Correct changelog entries to include release number

* Tue Nov 21 2006 Shidai Liu, Leo <sdl.web@gmail.com> 0.31-3
- remove themes from gnome-look
- remove CREDITS patch
- add all themes from upstream

* Thu Nov 16 2006 Shidai Liu, Leo <sdl.web@gmail.com> 0.31-2
- 0.31

* Sun Nov 12 2006 Shidai Liu, Leo <sdl.web@gmail.com> 0.30.2-1
- Add three gtk2 themes

* Tue Sep 19 2006 Shidai Liu, Leo <sdl.web@gmail.com> 
- Initial build.

