Name:           mozo
Version:        1.12.0
Release:        2%{?dist}
Summary:        MATE Desktop menu editor
License:        LGPLv2+
URL:            http://mate-desktop.org
# source is from gtk3 branch at http://git.mate-desktop.org/mozo/?h=gtk3
Source0:        https://raveit65.fedorapeople.org/Mate/SOURCE/%{name}-gtk3-%{version}.tar.xz

# rhbz (#1202674)
# https://github.com/infirit/mozo/commit/acf2f98
Patch0:         mozo_Use-Gtk-selection-mode.patch

BuildRequires:  desktop-file-utils
BuildRequires:  mate-common 
BuildRequires:  mate-menus-devel
BuildRequires:  pygobject3-devel
BuildRequires:  python2-devel

Requires:       mate-menus

Provides: mate-menu-editor = %{version}-%{release}
Obsoletes: mate-menu-editor < %{version}-%{release}

BuildArch:  noarch

%description
MATE Desktop menu editor

%prep
%setup -qn %{name}-gtk3-%{version}
#NOCONFIGURE=1 ./autogen.sh

# disable for gtk3
# %patch0 -p1 -b .selection-mode

%build
%configure

make %{?_smp_mflags} V=1

%install
%{make_install}

desktop-file-install                                  \
        --dir=%{buildroot}%{_datadir}/applications    \
%{buildroot}%{_datadir}/applications/mozo.desktop

%find_lang %{name} --with-gnome --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/mozo
%{_datadir}/icons/hicolor/*x*/apps/mozo.png
%{_datadir}/mozo/
%{_datadir}/applications/mozo.desktop
%{_mandir}/man1/mozo.1.*
%{python_sitelib}/Mozo/


%changelog
* Wed Feb 03 2016 Liu Di <liudidi@gmail.com> - 1.12.0-2
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release
- build against gtk3

* Fri Jul 24 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-2
- try fix rhbz (#1202674)

* Fri Jul 24 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Thu Feb 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-2
- use mozo.1.* instead of mozo.1.gz
- update obsoletes

* Tue Feb 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-1
- rename to mozo
- update to 1.7.0 release
- use modern 'make install' macro
- update file section
- remove needless finding static libs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.0-2
- Update as per package review

* Sat Feb 23 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.5.0-1
- Initial build

* Sat Nov 10 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
