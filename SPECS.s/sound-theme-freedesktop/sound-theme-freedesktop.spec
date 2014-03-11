Name: sound-theme-freedesktop
Version: 0.7
Release: 5%{?dist}
Summary: freedesktop.org sound theme
Group: User Interface/Desktops
Source0: http://people.freedesktop.org/~mccann/dist/sound-theme-freedesktop-%{version}.tar.bz2
# For details on the licenses used, see CREDITS
License: GPLv2+ and LGPLv2+ and CC-BY-SA and CC-BY
Url: http://www.freedesktop.org/wiki/Specifications/sound-theme-spec
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: gettext
BuildRequires: intltool >= 0.40
Requires(post): /bin/touch
Requires(postun): /bin/touch

Obsoletes: gnome-audio <= 2.22.2
Obsoletes: gnome-audio-extra <= 2.22.2

%description
The default freedesktop.org sound theme following the XDG theming
specification.  (http://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%postun
/bin/touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%files
%defattr(-,root,root)
%doc README
%dir %{_datadir}/sounds/freedesktop
%dir %{_datadir}/sounds/freedesktop/stereo
%{_datadir}/sounds/freedesktop/index.theme
%{_datadir}/sounds/freedesktop/stereo/*.oga

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.7-5
- 为 Magic 3.0 重建

* Wed Feb 08 2012 Liu Di <liudidi@gmail.com> - 0.7-4
- 为 Magic 3.0 重建

