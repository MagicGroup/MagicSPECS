%global with_python3 1

%global srcname snowballstemmer

Name:           python-%{srcname}
Version:	1.2.0
Release:	2%{?dist}
Summary:        This package provides 16 stemmer algorithms
Summary(zh_CN.UTF-8): 词干分析器算法

License:        BSD and Python and Unicode
URL:            https://github.com/kjd/snowballstemmer
Source0:        https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # with_python3

%description
This package provides 16 stemmer algorithms (15 + Poerter English
stemmer) generated from Snowball algorithms. It includes following
language algorithms: Danish, Dutch, English (Standard, Porter),
Finnish, French, German, Hungarian, Italian, Norwegian, Portuguese,
Romanian, Russian, Spanish, Swedish, Turkish. This is a pure Python
stemming library. If PyStemmer is available, this module uses it to
accelerate.

%description -l zh_CN.UTF-8
词干分析器算法。

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        This package provides 16 stemmer algorithms
Summary(zh_CN.UTF-8): 词干分析器算法

%description -n python3-%{srcname}
This package provides 16 stemmer algorithms (15 + Poerter English
stemmer) generated from Snowball algorithms. It includes following
language algorithms: Danish, Dutch, English (Standard, Porter),
Finnish, French, German, Hungarian, Italian, Norwegian, Portuguese,
Romanian, Russian, Spanish, Swedish, Turkish. This is a pure Python
stemming library. If PyStemmer is available, this module uses it to
accelerate.
%description -n python3-%{srcname} -l zh_CN.UTF-8
词干分析器算法。
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3



%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/snowballstemmer/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/snowballstemmer/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
# Set LANG when building with python 3 due to
# https://github.com/kjd/snowballstemmer/pull/4
LANG=en_US.UTF-8 %{__python3} setup.py test
popd
%endif # with_python3


%files
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%endif # with_python3

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.2.0-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 1.2.0-1
- 更新到 1.2.0
