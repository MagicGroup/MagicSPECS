%global with_py3 1

%global pkgname sphinx_rtd_theme

Name:           python-%{pkgname}
Version:        0.1.8
Release:        4%{?dist}
Summary:        Sphinx theme for readthedocs.org
Summary(zh_CN.UTF-8): readthedocs.org 的 Sphinx 主题

License:        MIT
URL:            https://github.com/snide/sphinx_rtd_theme
Source0:        https://pypi.python.org/packages/source/s/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

%if 0%{?with_py3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

Requires:       font(fontawesome)
Requires:       font(lato)

%description
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.
%description -l zh_CN.UTF-8
readthedocs.org 的 Sphinx 主题。

%if 0%{?with_py3}
%package -n python3-%{pkgname}
Summary:        Sphinx theme for readthedocs.org
Summary(zh_CN.UTF-8): readthedocs.org 的 Sphinx 主题
Requires:       font(fontawesome)
Requires:       font(lato)

%description -n python3-%{pkgname}
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.
%description -n python3-%{pkgname} -l zh_CN.UTF-8
readthedocs.org 的 Sphinx 主题
%endif

%prep
%setup -q -c

# Prepare for python3 build
cp -a %{pkgname}-%{version} python3-%{pkgname}-%{version}

%build
# Python 2 build
pushd %{pkgname}-%{version}
%{__python2} setup.py build
popd

%if 0%{?with_py3}
# Python 3 build
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py build
popd
%endif

%install
# Python 2 install
pushd %{pkgname}-%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
popd

# Don't use the bundled fonts
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/*.{svg,woff}
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/fontawesome*.ttf
rm %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/Lato*.ttf
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Bold.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Regular.ttf \
      %{buildroot}/%{python2_sitelib}/%{pkgname}/static/fonts/

%if 0%{?with_py3}
# Python 3 install
pushd python3-%{pkgname}-%{version}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd

# Don't use the bundled fonte
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/*.{svg,woff}
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/fontawesome*.ttf
rm %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/Lato*.ttf
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.svg \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/fontawesome/fontawesome-webfont.woff \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Bold.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
ln -s %{_datadir}/fonts/lato/Lato-Regular.ttf \
      %{buildroot}/%{python3_sitelib}/%{pkgname}/static/fonts/
%endif
magic_rpm_clean.sh
 
%files
%doc %{pkgname}-%{version}/README.rst
%license %{pkgname}-%{version}/LICENSE
%{python2_sitelib}/%{pkgname}*
 
%if 0%{?with_py3}
%files -n python3-%{pkgname}
%doc python3-%{pkgname}-%{version}/README.rst
%license python3-%{pkgname}-%{version}/LICENSE
%{python3_sitelib}/%{pkgname}*
%endif

%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.1.8-4
- 为 Magic 3.0 重建

* Wed Sep 02 2015 Liu Di <liudidi@gmail.com> - 0.1.8-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Jerry James <loganjerry@gmail.com> - 0.1.8-1
- New upstream version
- Unbundle the Lato fonts

* Wed Mar 11 2015 Jerry James <loganjerry@gmail.com> - 0.1.7-1
- New upstream version

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 0.1.6-2
- Use license macro

* Thu Jul  3 2014 Jerry James <loganjerry@gmail.com> - 0.1.6-1
- Initial RPM
