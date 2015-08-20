%if 0%{?fedora} > 12
%global with_python3 1
%endif
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global pylib_version 1.4.17

Name:           pytest
Version:	2.7.2
Release:	1%{?dist}
Summary:        Simple powerful testing with Python
Summary(zh_CN.UTF-8): Python 的简单强力的测试模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        MIT
URL:            http://pytest.org
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python-setuptools
BuildRequires:  python-py >= %{pylib_version}
Requires:       python-py >= %{pylib_version}
%if 0%{?rhel} > 6 || 0%{?fedora}
BuildRequires:  python-sphinx
%else
BuildRequires:  python-sphinx10
%endif # fedora
BuildRequires:  python-docutils
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-py >= %{pylib_version}
%endif # with_python3
# pytest was separated from pylib at that point
Conflicts:      python-py < 1.4.0

# used by the testsuite, if present:
%if 0%{?fedora}
# if pexpect is present, the testsuite fails on F19 due to
# http://bugs.python.org/issue17998
#BuildRequires:  python-pexpect
BuildRequires:  python-mock
BuildRequires:  python-twisted-core
%if 0%{?with_python3}
#BuildRequires:  python3-pexpect
BuildRequires:  python3-mock
%endif # with_python3
%endif # fedora


%description
py.test provides simple, yet powerful testing for Python.

%description -l zh_CN.UTF-8
Python 的简单强力的测试模块。

%if 0%{?with_python3}
%package -n python3-pytest
Summary:        Simple powerful testing with Python
Summary(zh_CN.UTF-8): Python3 的简单强力的测试模块
Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
Requires:       python3-setuptools
Requires:       python3-py >= %{pylib_version}


%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.

%description -n python3-pytest -l zh_CN.UTF-8
Python3 的简单强力的测试模块。
%endif # with_python3


%prep
%setup -q

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{__python} setup.py build

%if 0%{?rhel} > 6 || 0%{?fedora}
for l in doc/* ; do
  make -C $l html PYTHONPATH=$(pwd)
done
%else
for l in doc/* ; do
  make -C $l html SPHINXBUILD=sphinx-1.0-build PYTHONPATH=$(pwd)
done
%endif # fedora

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# remove shebangs from all scripts
find %{buildroot}%{python3_sitelib} -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' {} \;

popd
%endif # with_python3

mkdir -p _htmldocs/html
for l in doc/* ; do
  # remove hidden file
  rm ${l}/_build/html/.buildinfo
  mv ${l}/_build/html _htmldocs/html/${l##doc/}
done

rst2html README.rst > README.html

# use 2.X per default
pushd %{buildroot}%{_bindir}
ln -snf py.test-2.* py.test
popd
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python_sitelib} \
  %{buildroot}%{_bindir}/py.test -r s testing
%if 0%{?with_python3}
pushd %{py3dir}
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
  %{buildroot}%{_bindir}/py.test-3.* -r s testing
popd
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README.html
%doc _htmldocs/html
%{_bindir}/py.test
%{_bindir}/py.test-2.*
%{python_sitelib}/*


%if 0%{?with_python3}
%files -n python3-pytest
%defattr(-,root,root,-)
%doc CHANGELOG LICENSE README.html
%doc _htmldocs/html
%{_bindir}/py.test-3.*
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 2.7.2-1
- 更新到 2.7.2

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 2.4.2-3
- 为 Magic 3.0 重建

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-2
- Only run tests from the 'testing' subdir in %%check.

* Sat Oct  5 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.2-1
- Update to 2.4.2.
- Add buildroot's bindir to PATH while running the testsuite.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-3
- Disable tests using pexpect for now, fails on F19.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-2
- Use python-sphinx for rhel > 6 (rhbz#973318).
- Update BR to use python-pexpect instead of pexpect.

* Sat May 25 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.5-1
- Update to 2.3.5.
- Docutils needed now to build README.html.
- Add some BR optionally used by the testsuite.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.4-1
- Update to 2.3.4.

* Sun Oct 28 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.2-1
- Update to 2.3.2.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Re-enable some tests, ignore others.
- Docs are available in English and Japanese now.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-4
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.
- Disable failing tests for Python3.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.2.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.4-1
- Update to 2.2.4.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.3-1
- Update to 2.2.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1.

* Tue Dec 13 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.0-1
- Update to 2.2.0.

* Wed Oct 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.3-1
- Update to 2.1.3.

* Tue Sep 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-2
- Fix: python3 dependencies.

* Sun Aug 28 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-2
- Update Requires and BuildRequires tags.

* Tue Aug  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.0-1
- Update to 2.1.0.

* Mon May 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.3-1
- Update to 2.0.3.

* Thu Mar 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.2-1
- Update to 2.0.2.

* Sun Jan 16 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.0.0-1
- New package.
