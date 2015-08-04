%{!?scl:%global pkg_name %{name}}

%global pa_version 0.11.12
%global features FedoraFeatures
%global repos repositories

Name:           preupgrade-assistant
Version:        0.11.12
Release:        6%{?dist}
Summary:        Preupgrade assistant performs assessment of the system
License:        GPLv3+
URL:            https://github.com/phracek/preupgrade-assistant
Source0:        https://github.com/phracek/%{name}/archive/%{pa_version}.tar.gz
Source1:        macros.preupgrade-assistant
Source2:        check.ini
Source3:        check.sh
Source4:        solution.txt
Source5:        repositories.ini
Source6:        repositories.py
Source7:        repositories.txt
Patch0:         preupgrade-assistant-do-not-ship-ui.patch
Patch1:         preupgrade-assistant-reports.patch
Patch2:         preupgrade-assistant-html.patch
Patch3:         preupgrade-assistant-print.patch
Patch4:         preupgrade-assistant-exception.patch
BuildArch:      noarch

BuildRequires:  rpm-devel
%if %{?_with_check:1}%{!?_with_check:0}
BuildRequires:  perl-XML-XPath
%endif
BuildRequires:  openscap-engine-sce >= 0:1.0.8-1
BuildRequires:  openscap-utils >= 0:1.0.8-1
BuildRequires:  openscap >= 0:1.0.8-1
Requires:       openscap >= 0:1.0.8-1
Requires:       openscap-engine-sce >= 0:1.0.8-1
Requires:       openscap-utils >= 0:1.0.8-1
Requires:       coreutils grep gawk
Requires:       sed findutils bash
%if 0%{?fedora} == 22
BuildRequires:  pykickstart
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-requests
BuildRequires:  rpm-python
Requires:       python-setuptools
Requires:       python-six
Requires:       python-requests
Requires:       rpm-python
Requires:       pykickstart
%else
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-six
BuildRequires:  python3-requests
BuildRequires:  rpm-python3
BuildRequires:  python3-kickstart
Requires:       python3-kickstart
Requires:       python3-setuptools
Requires:       python-six
Requires:       python3-requests
Requires:       rpm-python3
%endif

%description
Preupgrade assistant performs assessment of the system from
the "upgradeability" point of view. Such analysis includes check for removed
packages, packages replaced by partially incompatible packages, changes in
libraries, users and groups and various services. Report of this analysis
can help the admin with the inplace upgrade - by identification of potential
troubles and by mitigating some of the incompatibilities. Data gathered
by preupgrade assistant can be used for the "cloning" of the system - new,
clean installation of the system, as close as possible to the old Fedora setup.
In addition, it provides some postupgrade scripts which are supposed to finish
migration after the installation of Fedora system.

%package devel
Summary:        Devel package for building contents
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description devel
Contains macros needed for building preupgrade-assistant contents
and scripts for generating contents.

%package features
Summary:        Set of contents for upgrade to the highest version
Requires:       %{name} = %{version}-%{release}
BuildRequires:  %{name}-devel
BuildArch:      noarch

%description features
Contains a set of features available in the next Fedora release.
The set is defined by Project Management.

%package repositories
Summary:        Contents which provides repositories for kickstart generation
Requires:       %{name} = %{version}-%{release}
BuildRequires:  %{name}-devel
BuildArch:      noarch

%description repositories
Contains content with repositories which are needed
for kickstart generation

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .not-ui
%patch1 -p1 -b .reports
%patch2 -p1 -b .html_patch
%patch3 -p1 -b .print
%patch4 -p1 -b .exception

rm -rf preup_ui
rm -rf ui-conf

mkdir -p %{preupgrade_name}/%{features}
cp -a %{SOURCE2} %{SOURCE3} %{SOURCE4} %{preupgrade_name}/%{features}/
mkdir -p %{preupgrade_name}/%{repos}
cp -a %{SOURCE5} %{SOURCE6} %{SOURCE7} %{preupgrade_name}/%{repos}/



%build
%if 0%{?fedora} == 22
%{__python2} setup.py build
%else
%{__python3} setup.py build
%endif

%{preupgrade_build} %{preupgrade_name}/%{features}/
%{preupgrade_build} %{preupgrade_name}/%{repos}/

%check
%if 0%{?fedora} == 22
%{__python2} setup.py test
%else
%{__python3} setup.py test
%endif

%install

#Preupgrade snd Premigrate tuff
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/preupgrade/{xsl,common,postupgrade.d,kickstart}

mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/sectool-sce/
mkdir -p -m 755 $RPM_BUILD_ROOT%{_docdir}/preupgrade

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/preupgrade
install -d -m 755 $RPM_BUILD_ROOT%{_localstatedir}/log/preupgrade

mkdir -p -m 755 $RPM_BUILD_ROOT%{preupgrade_dir}/%{features}
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{preupgrade_dir}/%{features}/check.sh
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{preupgrade_dir}/%{features}/solution.txt
install -p -m 644 %{preupgrade_name}-%{preupg_results}/%{features}/group.xml \
    $RPM_BUILD_ROOT%{preupgrade_dir}/%{features}/group.xml
mkdir -p -m 755 $RPM_BUILD_ROOT%{preupgrade_dir}/%{repos}
install -p -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{preupgrade_dir}/%{repos}/repositories.py
install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{preupgrade_dir}/%{repos}/repositories.txt
install -p -m 644 %{preupgrade_name}-%{preupg_results}/%{repos}/group.xml \
    $RPM_BUILD_ROOT%{preupgrade_dir}/%{repos}/group.xml

%{__install} -p -m 644 -D %SOURCE1 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.preupgrade-assistant

%if 0%{?fedora} == 22
%{__python2} setup.py install --skip-build --root=$RPM_BUILD_ROOT
%else
%{__python3} setup.py install --skip-build --root=$RPM_BUILD_ROOT
%endif

%global egg_name %(echo %{name} | sed s/-/_/)

%{__install} -p -m 644 -D man/preupg.1 $RPM_BUILD_ROOT%{_mandir}/man1/preupg.1


%if 0%{?fedora} == 22
rm -rf  ${RPM_BUILD_ROOT}%{python2_sitelib}/preup_ui/
%else
rm -rf  ${RPM_BUILD_ROOT}%{python3_sitelib}/preup_ui/
%endif
rm -f   ${RPM_BUILD_ROOT}%{_bindir}/preup_ui_manage
rm -rf  ${RPM_BUILD_ROOT}%{_datadir}/preupgrade/kickstart
rm -rf  ${RPM_BUILD_ROOT}%{_datadir}/premigrate
rm -rf  ${RPM_BUILD_ROOT}%{_datadir}/preupgrade/xsl
rm -f ${RPM_BUILD_ROOT}%{_bindir}/premigrate

%files
%license LICENSE
%{_bindir}/preupg
%if 0%{?fedora} == 22
%dir %{python2_sitelib}/preup
%{python2_sitelib}/preup/*
%{python2_sitelib}/%{egg_name}*.egg-info
%else
%dir %{python3_sitelib}/preup
%{python3_sitelib}/preup/*
%{python3_sitelib}/%{egg_name}*.egg-info
%endif
# Preupgrade stuff
%dir %{_datadir}/preupgrade
%{_datadir}/preupgrade/common
%{_datadir}/preupgrade/common.sh
%{_datadir}/preupgrade/postupgrade.d
%{_datadir}/preupgrade/README.kickstart
%{_datadir}/preupgrade/README
%doc README
%{_localstatedir}/log/preupgrade
%{_mandir}/man1/*
%if 0%{?fedora} == 22
%dir %{python2_sitelib}/preuputils
%{python2_sitelib}/preuputils/*
%else
%dir %{python3_sitelib}/preuputils
%{python3_sitelib}/preuputils/*
%endif

%files devel
%{_bindir}/preupg-create-group-xml
%{_bindir}/preupg-xccdf-compose
%{_rpmconfigdir}/macros.d/macros.preupgrade-assistant

%files features
%dir %{preupgrade_dir}/%{features}/
%{preupgrade_dir}/%{features}/*

%files repositories
%dir %{preupgrade_dir}/%{repos}/
%{preupgrade_dir}/%{repos}/*

%changelog
* Tue Jun 16 2015 Petr Hracek <phracek@redhat.com> - 0.11.12-6
- content for repositories (#1225812)

* Fri May 29 2015 Petr Hracek <phracek@redhat.com> - 0.11.12-5
- Fix for exception case in Python 3

* Tue May 26 2015 Petr Hracek <phracek@redhat.com> - 0.11.12-4
- Fix print issue #1224892

* Wed May 20 2015 Petr Stodulka <pstodulk@redhat.com> - 0.11.12-3
- fixed wrong substitution for solution texts

* Tue May 19 2015 Petr Stodulka <pstodulk@redhat.com> - 0.11.12-2
- added patch for updating solution.txt caused by splitting reports 

* Fri May 15 2015 Petr Hracek <phracek@redhat.com> - 0.11.12-1
- Rebase to new upstream version 0.11.12

* Fri Apr 10 2015 Petr Stodulka <pstodulk@redhat.com> - 0.11.10-1
- Rebase to new upstream version 0.11.10
- modified patch0

* Mon Mar 09 2015 Petr Hracek <phracek@redhat.com> 0.11.7-1
- Initial rpm
