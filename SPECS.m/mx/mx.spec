%define pybasever %{nil}
%define without_pybasever 1
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define _unpackaged_files_terminate_build	0

Summary:  A collection of Python software tools
Summary(zh_CN.UTF-8): Python 软件工具集合
Name: mx%{pybasever}
Version: 3.2.5
Release: 4%{?dist}
URL: http://www.lemburg.com/files/python/eGenix-mx-Extensions.html
Source0: http://www.lemburg.com/python/egenix-mx-base-%{version}.tar.gz
#Patch1: mx-3.1.1-lib64.patch
License: Python
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires: Distutils
BuildRequires: python-devel > 2.3
%if %{?without_pybasever}
Provides: mx2 = %{version}-%{release}
Obsoletes: mx2 <= %{version}-%{release}
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
The mx extensions for Python are a collection of Python software tools
which enhance Python's usability in many areas.

%description -l zh_CN.UTF-8
Python 软件工具集合。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
Development files for %{name}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n egenix-mx-base-%{version}
#%patch1 -p1 -b .lib64

%build
# alter /usr/local/bin/python
for file in mx/DateTime/Examples/Y2000.py mx/Misc/OrderedMapping.py \
    mx/TextTools/Examples/pytag.py mx/TextTools/Examples/Loop.py \
    mx/TextTools/Examples/Python.py mx/DateTime/Examples/AtomicClock.py \
    mx/TextTools/Examples/mysplit.py mx/TextTools/Examples/HTML.py \
    mx/DateTime/Examples/alarm.py mx/TextTools/Examples/RegExp.py \
    mx/TextTools/Examples/altRTF.py mx/TextTools/Examples/Words.py \
    mx/TextTools/Examples/RTF.py mx/Misc/FileLock.py ; do
    sed -i -e 's!/usr/local/bin/python!%{_bindir}/python!' ${file}
done

# These just have test cases and aren't meant to be run
for file in mx/Log.py mx/BeeBase/FileLock.py mx/Misc/OrderedMapping.py \
    mx/Misc/FileLock.py ; do
    sed -i -e '/^#!.*python\b/d' ${file}
done


CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --skip-build --root=%{buildroot} 

pushd %{buildroot}%{python_sitearch}
for I in `find . -name '*.h'`; do
    mkdir -p %{buildroot}%{_includedir}/`dirname $I`
    mv $I %{buildroot}%{_includedir}/`dirname $I`
done
popd

# Examples, tests, benchmarks
BASEDIR=%{buildroot}%{python_sitearch}
mkdir examples
mv ${BASEDIR}/mx/TextTools/mxTextTools/testkj.py examples/
mv ${BASEDIR}/mx/Stack/stackbench.py examples/
mv ${BASEDIR}/mx/Queue/queuebench.py examples/
mv ${BASEDIR}/mx/DateTime/mxDateTime/test.py examples/
# This is a utility.  If it's deemed useful to the general public it should
# be installed in %{_bindir} instead of examples
mv ${BASEDIR}/mx/BeeBase/showBeeDict.py examples/

# These files are documentation, and are in a bad location
mkdir docs
mv -f ${BASEDIR}/mx/{LICENSE,COPYRIGHT} docs/
rm -rf ${BASEDIR}/mx/Doc
DESTDIR=`pwd`/docs
pushd ${BASEDIR}/mx
cp -r --parents */Doc/* ${DESTDIR}/
cp -r --parents */Examples/* ${DESTDIR}/
popd
rm -rf ${BASEDIR}/mx/*/Doc/
rm -rf ${BASEDIR}/mx/*/Examples
rm -rf docs/*/Examples/*.pyc
rm -rf docs/*/Examples/*.pyo
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc README docs/*
%{python_sitearch}/mx
%{python_sitearch}/egenix_mx_base*.egg-info

%files devel
%defattr(-,root,root,-)
%{_includedir}/mx/

%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 3.2.5-4
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 3.2.5-3
- 为 Magic 3.0 重建

* Sat Jan 03 2015 Liu Di <liudidi@gmail.com> - 3.2.5-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.2.1-2
- 为 Magic 3.0 重建

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 3.2.1-1
- Upstream v3.2.1

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 3.2.0-1
- Upstream v3.2.0
- Removed long year patch, now in upstream
- Support for Python 2.3 dropped

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.1.1-3
- Rebuild for Python 2.6

* Mon Sep 15 2008 Toshio Kuratomi <toshio@fedoraproject.org> 3.1.1-2
- Restore debug package
- Clean up the python site-packages handling
- Clean up handling of documentation, examples, scripts

* Mon Sep 15 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 3.1.1-1
- bump to newest release
- patch fixes
- spec file fixes
- branch new devel sub package
- fixes to permissions
- removed debug-package (empty)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.0.6-3
- rebuild against python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-2.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 14 2005 Mihai Ibanescu <misa@redhat.com> 2.0.6-2
- Rebuilt

* Wed Feb 02 2005 Elliot Lee <sopwith@redhat.com> 2.0.6-1
- Rebuild with python 2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Nov 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.0.5
- recompile with python 2.3

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 2.0.3-7
- lib64'ize

* Tue Aug 06 2002 Elliot Lee <sopwith@redhat.com> 2.0.3-6
- Provide mx2 dep

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.0.3-4
- Make it require python >= 2.2, < 2.3

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.0.3-2
- Move to python 2.2

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.0.3-1
- 2.0.3

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.0.2-5
- Rebuild (and no, it wasn't broken. It just used /usr/bin/python
  as the version to build for)

* Mon Jan 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.2-4
- Remove pyver autodetection (it's broken!) and install header files

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Oct  1 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.0.2-2
- detect python version when building
- 64bit fix mxDateTime

* Fri Sep 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.0.2-1
- 2.0.2
- Build for Python 2.2

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Initial build. Needed for python DB API
