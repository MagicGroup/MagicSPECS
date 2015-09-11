%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           qt-recordmydesktop
Version:        0.3.8
Release:        3%{?dist}
Summary:        KDE Desktop session recorder with audio and video
Summary(zh_CN.UTF-8): recordmydesktop 的 KDE 前端

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv2+
URL:            http://recordmydesktop.sourceforge.net/
Source0:        http://downloads.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  desktop-file-utils, gettext, PyQt4-devel
Requires:       recordmydesktop >= %{version}, PyQt4


%description
Graphical KDE frontend for the recordmydesktop desktop session recorder.

recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

%description -l zh_CN.UTF-8
recordmydesktop 的 KDE 图形前端。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

magic_rpm_clean.sh
#%find_lang qt-recordMyDesktop

desktop-file-install --vendor fedora --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
#%files -f qt-recordMyDesktop.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 0.3.8-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.3.8-2
- 为 Magic 3.0 重建

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.7.2-3
- Rebuild for Python 2.6

* Wed May 28 2008 Sindre Pedersen Bj酶rdal <sindrepb@fedoraproject.org> - 0.3.7.2-2
- New upstream release

* Wed Jan 23 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.3.7-1
- Update to latest upstream 0.3.7 to match recordmydesktop

* Sun Oct 21 2007 Sindre Pedersen Bj酶rdal <foolish@guezz.net> - 0.3.6-4
- Fix Source0 url
* Sun Oct 21 2007 Sindre Pedersen Bj酶rdal <foolish@guezz.net> - 0.3.6-2
- Add Missing PyQt4 dependency
- Fix License tag
* Sun Oct 21 2007 Roland Wolters <wolters.liste@gmx.net> - 0.3.6-1
- initially build
- adopted spec file from gtk-version


