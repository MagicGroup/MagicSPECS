%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           python-tempita
Version:        0.5.1
Release:        6%{?dist}
Summary:        A very small text templating language

Group:          Development/Languages
License:        MIT
URL:            http://pythonpaste.org/tempita/
Source0:        http://pypi.python.org/packages/source/T/Tempita/Tempita-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
%if 0%{?fedora} < 13
BuildRequires:  python-setuptools-devel
%else
BuildRequires:  python-setuptools
%endif
BuildRequires:  python-nose

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif # if with_python3

%description
Tempita is a small templating language for text substitution.

%if 0%{?with_python3}
%package -n python3-tempita
Summary:        A very small text templating language
Group:          Development/Languages
# Without one of these there's no aes implementation which means there's no way to
# have encrypted cookies.  This is a reduction in features over the python2 version.
# Currently there's no working python3 port for either:
# http://allmydata.org/trac/pycryptopp/ticket/35
# http://lists.dlitz.net/pipermail/pycrypto/2010q2/000253.html
#%if 0%{?fedora}
#Requires: python3-pycryptopp
#%else
#Requires: python3-crypto
#%endif

%description -n python3-tempita
Tempita is a small templating language for text substitution.
%endif # with_python3


%prep
%setup -q -n Tempita-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3

%clean
%{__rm} -rf %{buildroot}


%check
nosetests


%files
%defattr(-,root,root,-)
%{python_sitelib}/tempita/
%{python_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-tempita
%defattr(-,root,root,-)
%{python3_sitelib}/tempita/
%{python3_sitelib}/*.egg-info
%endif

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.1-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.5.1-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Ricky Zhou <ricky@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.4-6
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Tue Aug  3 2010 Kyle VanderBeek <kylev@kylev.com> - 0.4-5
- Add python3-tempita subpackage.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jun 26 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4-3
- Cosmetic fixes -- BR python-setuptools instead of python-setuptools-devel
- Conditionalize python_sitelib definition
- trailing slash for directory in %%files

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.4-1
- Upstream released a new version.

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.3-3
- Change define to global.
- Remove old >= 8 conditional.
- Remove unnecessary BuildRequires on python-devel.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.3-1
- Upstream released a new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-4
- Rebuild for Python 2.6

* Mon Jul 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.2-2
- Add %%check section.

* Sat Jun 14 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.2-1
- Initial RPM Package.
