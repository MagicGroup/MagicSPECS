%global pypi_name alabaster
%global srcname sphinx-theme-%{pypi_name}

Name:           python-%{srcname}
Version:        0.7.6
Release:        4%{?dist}
Summary:        Configurable sidebar-enabled Sphinx theme

License:        BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
This theme is a modified "Kr" Sphinx theme from @kennethreitz (especially as
used in his Requests project), which was itself originally based on @mitsuhiko's
theme used for Flask & related projects.


%package -n python2-%{srcname}
Summary:        Configurable sidebar-enabled Sphinx theme
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
This theme is a modified "Kr" Sphinx theme from @kennethreitz (especially as
used in his Requests project), which was itself originally based on @mitsuhiko's
theme used for Flask & related projects.


%package -n     python3-%{srcname}
Summary:        Configurable sidebar-enabled Sphinx theme
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
This theme is a modified "Kr" Sphinx theme from @kennethreitz (especially as
used in his Requests project), which was itself originally based on @mitsuhiko's
theme used for Flask & related projects.


%prep
%setup -qn %{pypi_name}-%{version}

# Remove bundled eggs
rm -rf %{pypi_name}.egg-info


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info/
%{python2_sitelib}/%{pypi_name}/

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/%{pypi_name}/


%changelog
* Fri Jul 31 2015 Julien Enseme <jujens@jujens.eu> - 0.7.6-4
- Use %%py2_build, %%py3build, %%py2_install and %%py2_install
- Make a python2 subpackage

* Thu Jul 30 2015 Julien Enselme <jujens@jujens.eu> - 0.7.6-3
- Add provides for python2-sphinx-theme-alabaster
- Remove usage of python2 and python3 dirs

* Fri Jul 24 2015 Julien Enselme <jujens@jujens.eu> - 0.7.6-2
- Remove %%py3dir macro
- Add CFLAGS in %%build

* Sat Jul 18 2015 Julien Enselme <jujens@jujens.eu> - 0.7.6-1
- Initial packaging
