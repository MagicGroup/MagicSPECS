%global with_python3 1

%global srcname Flask
%global srcversion 0.10.1

Name:           python-flask
Version:        0.10.1
Release:        8%{?dist}
Epoch:          1
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
Summary(zh_CN.UTF-8): 基于 Werkzeug, Jinja2 的 Python 微框架

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://flask.pocoo.org/
Source0:        http://pypi.python.org/packages/source/F/Flask/%{srcname}-%{srcversion}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python-setuptools python-werkzeug python-sphinx
Requires:       python-werkzeug

BuildRequires:  python-jinja2
BuildRequires:  python-itsdangerous
Requires:       python-jinja2
Requires:       python-itsdangerous

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.

%description -l zh_CN.UTF-8
基于 Werkzeug, Jinja2 的 Python 微框架。

%package doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description doc
Documentation and examples for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%if 0%{?with_python3}
%package -n python3-flask
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions
Summary(zh_CN.UTF-8): 基于 Werkzeug, Jinja2 的 Python 微框架
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-jinja2
BuildRequires:  python3-werkzeug
BuildRequires:  python3-sphinx
BuildRequires:  python3-itsdangerous
Requires:       python3-jinja2
Requires:       python3-werkzeug
Requires:       python3-itsdangerous

%description -n python3-flask
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.

%description -n python3-flask -l zh_CN.UTF-8
基于 Werkzeug, Jinja2 的 Python 微框架。

%package -n python3-flask-doc
Summary:        Documentation for python3-flask
Summary(zh_CN.UTF-8): python3-flask 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       python3-flask = %{epoch}:%{version}-%{release}

%description -n python3-flask-doc
Documentation and examples for python3-flask.
%description -n python3-flask-doc -l zh_CN.UTF-8
python3-flask 的文档。
%endif


%prep
%setup -q -n %{srcname}-%{srcversion}
%{__sed} -i "/platforms/ a\    requires=['Jinja2 (>=2.4)']," setup.py

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif


%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=%{buildroot}%{python_sitelib}
%{__python} setup.py develop --install-dir %{buildroot}%{python_sitelib}
make -C docs html

rm -rf %{buildroot}%{python_sitelib}/site.py
rm -rf %{buildroot}%{python_sitelib}/site.py[co]
rm -rf %{buildroot}%{python_sitelib}/easy-install.pth
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%{__python3} setup.py develop --install-dir %{buildroot}%{python3_sitelib}
make -C docs html

rm -rf %{buildroot}%{python3_sitelib}/site.py
rm -rf %{buildroot}%{python3_sitelib}/site.py[co]
rm -rf %{buildroot}%{python3_sitelib}/easy-install.pth
rm -rf %{buildroot}%{python3_sitelib}/__pycache__/site.cpython-3?.pyc
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc
popd
%endif
magic_rpm_clean.sh

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.egg-link
%{python_sitelib}/flask

%files doc
%doc docs/_build/html examples

%if 0%{?with_python3}
%files -n python3-flask
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/*.egg-link
%{python3_sitelib}/flask

%files -n python3-flask-doc
%doc docs/_build/html examples
%endif


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:0.10.1-8
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:0.10.1-7
- 为 Magic 3.0 重建

* Thu Sep 03 2015 Liu Di <liudidi@gmail.com> - 1:0.10.1-6
- 为 Magic 3.0 重建

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 1:0.10.1-5
- 为 Magic 3.0 重建

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Minor fix to rhel macro logic

* Mon Jul 29 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:0.10.1-3
- fix wrong requires on sphinx (RHBZ #989361)

* Sat Jul 20 2013 Ricky Elrod <codeblock@fedoraproject.org> - 1:0.10.1-2
- Nuke a Python3 specific file owned by python3-setuptools.

* Sat Jun 15 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:0.10.1-1
- upstream 0.10.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-5
- Add epoch to subpackage Requires.

* Wed Aug 8 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-4
- Fix changelog messup.

* Wed Aug 8 2012 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-3
- Unified spec for EL6 and Fedora

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.0-1
- upstream 0.9
- spec cleanups

* Sun Jul  1 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.1-1
- upstream 0.8.1 (minor bugfixes)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.0-1
- upstream 0.8

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.7.2-2
- don't own easy-install.pth

* Fri Jul 22 2011 Steve Milner <smilner@fedoraproject.org> - 0.7.2-1
- update for upstream release

* Thu Feb 24 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-2
- fix rpmlint spelling warning
- BR python2-devel rather than python-devel
- run test suite in check

* Tue Feb 22 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-1
- Initial package
