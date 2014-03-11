%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-sqlite2
Version:        2.3.5
Release:        5%{?dist}
Epoch:          1
Summary:        DB-API 2.0 interface for SQLite 3.x

Group:          Development/Languages
License:        zlib/libpng
URL:            http://pysqlite.org/
Source0:        http://initd.org/pub/software/pysqlite/releases/2.3/%{version}/pysqlite-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dos2unix
BuildRequires:  python-devel
BuildRequires:  sqlite-devel >= 3.3.3

Requires:       sqlite >= 3.3.3

%description
pysqlite is an interface to the SQLite 3.x embedded relational database
engine. It is almost fully compliant with the Python database API version
2.0 also exposes the unique features of SQLite.


%prep
%setup -q -n pysqlite-%{version}
sed -i -e '
/\/usr\/include/d
/\/usr\/lib/d' setup.cfg


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 \
        --skip-build \
        --root %{buildroot}

%{__rm} -rf %{buildroot}%{_prefix}/pysqlite2-doc
dos2unix doc/code/*


%check
# workaround for a strange bug (thanks to Ville Skyttä!)
cd doc
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} -c \
        "from pysqlite2.test import test; test()"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE doc/code doc/usage-guide.txt
%dir %{python_sitearch}/pysqlite2
%{python_sitearch}/pysqlite2/__init__.py
%{python_sitearch}/pysqlite2/__init__.pyc
%{python_sitearch}/pysqlite2/__init__.pyo
%{python_sitearch}/pysqlite2/dbapi2.py
%{python_sitearch}/pysqlite2/dbapi2.pyc
%{python_sitearch}/pysqlite2/dbapi2.pyo
%{python_sitearch}/pysqlite2/_sqlite.so
%dir %{python_sitearch}/pysqlite2/test
%{python_sitearch}/pysqlite2/test/__init__.py
%{python_sitearch}/pysqlite2/test/__init__.pyc
%{python_sitearch}/pysqlite2/test/__init__.pyo
%{python_sitearch}/pysqlite2/test/dbapi.py
%{python_sitearch}/pysqlite2/test/dbapi.pyc
%{python_sitearch}/pysqlite2/test/dbapi.pyo
%{python_sitearch}/pysqlite2/test/factory.py
%{python_sitearch}/pysqlite2/test/factory.pyc
%{python_sitearch}/pysqlite2/test/factory.pyo
%{python_sitearch}/pysqlite2/test/hooks.py
%{python_sitearch}/pysqlite2/test/hooks.pyc
%{python_sitearch}/pysqlite2/test/hooks.pyo
%{python_sitearch}/pysqlite2/test/regression.py
%{python_sitearch}/pysqlite2/test/regression.pyc
%{python_sitearch}/pysqlite2/test/regression.pyo
%{python_sitearch}/pysqlite2/test/transactions.py
%{python_sitearch}/pysqlite2/test/transactions.pyc
%{python_sitearch}/pysqlite2/test/transactions.pyo
%{python_sitearch}/pysqlite2/test/types.py
%{python_sitearch}/pysqlite2/test/types.pyc
%{python_sitearch}/pysqlite2/test/types.pyo
%{python_sitearch}/pysqlite2/test/userfunctions.py
%{python_sitearch}/pysqlite2/test/userfunctions.pyc
%{python_sitearch}/pysqlite2/test/userfunctions.pyo
%{python_sitearch}/pysqlite-%{version}-py?.?.egg-info


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:2.3.5-5
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:2.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Xavier Lamien <lxtnow@gmail.com> - 1:2.3.5-1
- Update release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:2.3.3-5
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:2.3.3-4
- Rebuild for Python 2.6

* Fri Feb 29 2008 Xavier Lamien <lxtnow[at]gmail.com> - 1:2.3.3-3
- Added -egg-info file.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:2.3.3-2
- Autorebuild for GCC 4.3

* Tue Mar 13 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.3.3-1
- Update to 2.3.3 (#231848)

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1:2.3.2-3
- Rebuild for new Python

* Fri Sep  8 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.3.2-2
- Don't %%ghost *.pyo files (#205425)
- Fix mixed-use-of-spaces-and-tabs rpmlint warning

* Sun Jul  2 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.3.2-1
- Update to 2.3.2

* Wed Jun 21 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.3.1-1
- Update to 2.3.1

* Tue Jun 13 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.3.0-1
- Update to 2.3.0
- Change e-mail address in ChangeLog

* Thu Apr 20 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.2.2-1
- Update to 2.2.2

* Wed Apr 19 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.2.1-1
- Update to 2.2.1

* Fri Apr 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.2.0-1
- Update to 2.2.0

* Tue Feb 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.1.3-4
- Rebuild for Fedora Extras 5

* Sun Feb  5 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 1:2.1.3-3
- python-sqlite2 in FC-4 was downgraded -> Epoch had to be bumped.
  We need to do the same in development branch

* Thu Feb  2 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.1.3-2
- Run tests in %%check section

* Thu Feb  2 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.1.3-1
- Update to 2.1.3

* Tue Jan 17 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.1.0-1
- Update to 2.1.0

* Sat Jan 14 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.0.5-2
- Fix missing BR: sqlite-devel (Chris Chabot, #176653)

* Wed Dec 28 2005 Dawid Gajownik <gajownik[AT]gmail.com> - 2.0.5-1
- Initial RPM release.

