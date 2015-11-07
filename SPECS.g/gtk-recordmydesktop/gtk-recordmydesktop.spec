%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           gtk-recordmydesktop
Version:        0.3.8
Release:        5%{?dist}
Summary:        GUI Desktop session recorder with audio and video
Summary(zh_CN.UTF-8): recordmydesktop 的 Gtk 前端

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
License:        GPLv2+
URL:            http://recordmydesktop.iovar.org
Source0:        http://dl.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel, pygtk2-devel	 
BuildRequires:  desktop-file-utils, gettext
Requires:       recordmydesktop >= %{version}


%description
Graphical frontend for the recordmydesktop desktop session recorder.

recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

As such, the program is separated in two parts; a simple command line tool that
performs the basic tasks of capturing and encoding and an interface that 
exposes the program functionality in a usable way.

%description -l zh_CN.UTF-8
recordmydesktop 的 Gtk 图形前端。

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

magic_rpm_clean.sh
#%find_lang gtk-recordMyDesktop

desktop-file-install --vendor fedora --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT

%files
#%files -f gtk-recordMyDesktop.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.3.8-5
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.3.8-4
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.3.8-3
- 为 Magic 3.0 重建

* Fri Dec 09 2011 Liu Di <liudidi@gmail.com> - 0.3.8-2
- 为 Magic 3.0 重建


