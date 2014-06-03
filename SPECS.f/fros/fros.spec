Name:           fros
Version:        1.0
Release:        5%{?dist}
Summary:        Universal screencasting frontend with pluggable support for various backends

%global commit 988d73aea77ad0da5731983f6d45385db440e568
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/mozeq/fros
# this url is wrong, because github doesn't offer a space for downloadable archives :(
Source:         https://github.com/mozeq/fros/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Universal screencasting frontend with pluggable support for various backends.
The goal is to provide an unified access to as many screencasting backends as
possible while still keeping the same user interface so the user experience
while across various desktops and screencasting programs is seamless.

%package recordmydesktop
Summary: fros plugin for screencasting using recordmydesktop as a backend
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description recordmydesktop
fros plugin for screencasting using recordmydesktop as a backend

%package gnome
Summary: fros plugin for screencasting using Gnome3 integrated screencaster
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description gnome
fros plugin for screencasting using Gnome3 integrated screencaster

%prep
%setup -qn %{name}-%{commit}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python} setup.py test


%files
%doc README COPYING
%dir %{python_sitelib}/pyfros
%{python_sitelib}/pyfros/*.py*
%dir %{python_sitelib}/pyfros/plugins
%{python_sitelib}/pyfros/plugins/__init__.*
%{python_sitelib}/pyfros/plugins/const.*
# fros-1.0-py2.7.egg-info
%dir %{python_sitelib}/%{name}-%{version}-py2.7.egg-info
%{python_sitelib}/%{name}-%{version}-py2.7.egg-info/*
%{_bindir}/fros
%{_mandir}/man1/%{name}.1*

%files recordmydesktop
%{python_sitelib}/pyfros/plugins/*recordmydesktop.*

%files gnome
%{python_sitelib}/pyfros/plugins/*gnome.*

%changelog
* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Tue Aug  6 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-4
-  check if X is available rhbz#920206
- Resolves: #920206

* Tue Aug  6 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-3
- fixed exception when no plugin is installed rhbz#993619

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Jiri Moskovcak <jmoskovc@redhat.com> 1.0-1
- initial rpm
