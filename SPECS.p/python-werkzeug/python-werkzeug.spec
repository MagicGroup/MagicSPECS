%global with_python3 1

%global srcname werkzeug

Name:           python-werkzeug
Version:	0.10.4
Release:	3%{?dist}
Summary:        The Swiss Army knife of Python web development 
Summary(zh_CN.UTF-8): Python 网页开发使用的瑞士军刀

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://werkzeug.pocoo.org/
#Source0:        http://pypi.python.org/packages/source/W/Werkzeug/%{srcname}-%{version}.tar.gz
# pypi 的源码不全。
Source0:	https://github.com/mitsuhiko/werkzeug/archive/%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

%description
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).

%description -l zh_CN.UTF-8
Python 网页开发使用的瑞士军刀。

%package doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation and examples for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%if 0%{?with_python3}
%package -n python3-werkzeug
Summary:        The Swiss Army knife of Python web development
Summary(zh_CN.UTF-8): Python 网页开发使用的瑞士军刀
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx

%description -n python3-werkzeug
Werkzeug
========

Werkzeug started as simple collection of various utilities for WSGI
applications and has become one of the most advanced WSGI utility
modules.  It includes a powerful debugger, full featured request and
response objects, HTTP utilities to handle entity tags, cache control
headers, HTTP dates, cookie handling, file uploads, a powerful URL
routing system and a bunch of community contributed addon modules.

Werkzeug is unicode aware and doesn't enforce a specific template
engine, database adapter or anything else.  It doesn't even enforce
a specific way of handling requests and leaves all that up to the
developer. It's most useful for end user applications which should work
on as many server environments as possible (such as blogs, wikis,
bulletin boards, etc.).

%description -n python3-werkzeug -l zh_CN.UTF-8
Python 网页开发使用的瑞士军刀。

%package -n python3-werkzeug-doc
Summary:        Documentation for python3-werkzeug
Summary(zh_CN.UTF-8): python3-werkzeug 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
Requires:       python3-werkzeug = %{version}-%{release}

%description -n python3-werkzeug-doc
Documentation and examples for python3-werkzeug.
%description -n python3-werkzeug-doc -l zh_CN.UTF-8
python3-werkzeug 的文档。
%endif


%prep
%setup -q -n %{srcname}-%{version}
%{__sed} -i 's/\r//' LICENSE

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif


%build
%{__python} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
find examples/ -name '*.py' -executable | xargs chmod -x
find examples/ -name '*.png' -executable | xargs chmod -x
pushd docs
make html
popd
popd
%endif


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -rf docs/_build/html/.buildinfo
%{__rm} -rf examples/cupoftee/db.pyc
popd
%endif
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE 
%{python_sitelib}/*

%files doc
%defattr(-,root,root,-)
%doc docs/_build/html examples

%if 0%{?with_python3}
%files -n python3-werkzeug
%defattr(-,root,root,-)
%doc AUTHORS LICENSE
%{python3_sitelib}/*

%files -n python3-werkzeug-doc
%defattr(-,root,root,-)
%doc docs/_build/html examples
%endif


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.10.4-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.10.4-2
- 为 Magic 3.0 重建

* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.10.4-1
- 更新到 0.10.4

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 0.9.6-2
- 为 Magic 3.0 重建

* Fri Jul 18 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.6-1
- Upstream 0.9.6
- Fixes RHBZ #1105819

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug 26 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.4-1
- Upstream 0.9.4

* Thu Jul 25 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.3-1
- Upstream 0.9.3

* Tue Jul 23 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9.2-1
- Upstream 0.9.2 release.

* Sat Jun 15 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.1-1
- upstream 0.9.1
- add python3 flavor

* Fri Jun 14 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.9-1
- Upstream 0.9.0 release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.3-1
- upstream 0.8.3 (fixes XSS security issues)

* Wed Jan 25 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 0.8.2-1
- upstream 0.8.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.2-1
- Updating because upstream release of Werkzeug 0.6.2

* Fri Mar 05 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6-1
- Updating because upstream release of Werkzeug 0.6

* Tue Aug 25 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.5.1-1
- Initial package
