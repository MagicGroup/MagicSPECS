# Just a reminder to remove this when these conditions can no longer occur.
%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname docutils

Name:           python-%{srcname}
Version:        0.10
Release:        0.7.20120824svn7502%{?dist}
Summary:        System for processing plaintext documentation

Group:          Development/Languages
# See COPYING.txt for information
License:        Public Domain and BSD and Python and GPLv3+
URL:            http://docutils.sourceforge.net
#Source0:        http://downloads.sourceforge.net/docutils/%{srcname}-%{version}.tar.gz
# Sometimes we need snapshots.  Instructions below:
# svn co -r 7502 https://docutils.svn.sourceforge.net/svnroot/docutils/trunk/docutils
# cd docutils
# python setup.py sdist
# The tarball is in dist/docutils-VERSION.tar.gz
Source0:        %{srcname}-%{version}.tar.gz
# Submitted upstream: https://sourceforge.net/tracker/index.php?func=detail&aid=3560841&group_id=38414&atid=422030
Patch0: docutils-__import__-tests.patch
Patch1: docutils-__import__-fixes2.patch

# Disable some tests known to fail with Python 3.3
# Bug reports filed upstream as:
#   https://sourceforge.net/tracker/?func=detail&aid=3555164&group_id=38414&atid=422030
# and:
#   http://sourceforge.net/tracker/?func=detail&aid=3561133&group_id=38414&atid=422030
# Unicode test is failing because of a python3.3b2 bug:
# ImportError(b'str').__str__() returns bytes rather than str
# http://bugs.python.org/issue15778
Patch100: disable-failing-tests.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:       noarch

BuildRequires:  python2-devel
BuildRequires: python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python-tools
%endif

Requires: python-imaging
Provides: docutils = %{version}-%{release}
Obsoletes: docutils < %{version}-%{release}

%description
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        System for processing plaintext documentation for python3
Group:          Development/Languages
# This module is optional and not yet available for python3
#Requires: python3-imaging

%description -n python3-%{srcname}
The Docutils project specifies a plaintext markup language, reStructuredText,
which is easy to read and quick to write.  The project includes a python
library to parse rST files and transform them into other useful formats such
as HTML, XML, and TeX as well as commandline tools that give the enduser
access to this functionality.

Currently, the library supports parsing rST that is in standalone files and
PEPs (Python Enhancement Proposals).  Work is underway to parse rST from
Python inline documentation modules and packages.

This package contains the module, ported to run under python3.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p0
%patch1 -p0
%patch100 -p1 -b .disable-failing-tests

# Remove shebang from library files
for file in docutils/utils/{code_analyzer.py,punctuation_chars.py,error_reporting.py} docutils/utils/math/{latex2mathml.py,math2html.py} docutils/writers/xetex/__init__.py; do
sed -i -e '/#! *\/usr\/bin\/.*/{1D}' $file
done

iconv -f ISO88592 -t UTF8 tools/editors/emacs/IDEAS.rst > tmp
mv tmp tools/editors/emacs/IDEAS.rst

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}

CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3


%install
rm -rf %{buildroot}

# Must do the python3 install first because the scripts in /usr/bin are
# overwritten by setup.py install (and we want the python2 version to be the
# default for now).
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}

# docutils setup.py runs 2to3 on a copy of the tests and puts it in sitelib.
rm -rf %{buildroot}%{python3_sitelib}/test

popd

rm -rf %{buildroot}%{_bindir}/*
%endif # with_python3

%{__python} setup.py install --skip-build --root %{buildroot}

for file in %{buildroot}/%{_bindir}/*.py; do
    mv $file `dirname $file`/`basename $file .py`
done

# We want the licenses but don't need this build file
rm -f licenses/docutils.conf

%check
python test/alltests.py

%if 0%{?with_python3}
pushd %{py3dir}
python3 test3/alltests.py
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt 
%doc THANKS.txt licenses docs tools/editors
%{_bindir}/*
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%defattr(-,root,root,-)
%doc BUGS.txt COPYING.txt FAQ.txt HISTORY.txt README.txt RELEASE-NOTES.txt 
%doc THANKS.txt licenses docs tools/editors
%{python3_sitelib}/*
%endif

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.10-0.7.20120824svn7502
- 为 Magic 3.0 重建

* Sat Aug 25 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-0.6.20120824svn7502
- Further fix of places in the code that use__import__

* Fri Aug 24 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-0.5.20120824svn7502
- Rebase to new snapshot with some fixes integrated
- Reenable one test that I can't replicate the failure with.

* Fri Aug 24 2012 David Malcolm <dmalcolm@redhat.com> - 0.10-0.4.20120730svn7490
- fix/disable failing tests with python 3.3

* Tue Aug 14 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-0.3.20120730svn7490
- PyXML patch from upstream
- Fix ability to disable python3 builds

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.10-0.2.20120730svn7490
- remove rhel logic from with_python3 conditional

* Mon Jul 30 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.10-0.1.20120730svn7490
- Update to snapshot that's supposed to take care of the date directive unicode
  problem in a different way
- Patch to fix PyXML conflict without using rpm conflicts

* Fri Jul 20 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9.1-1
- New update from upstream
- Fixes for previous patches incorporated there
- roman.py has been moved into a docutils submodule
- docutils doesn't work with PyXML.  before I poke around for the bug in PyXML,
  seeing if we're going to go through with deprecating it or if we can sanitize
  our python stdlib's handling of it.
- Fix for traceback in https://bugzilla.redhat.com/show_bug.cgi?id=786867

* Mon Jan 30 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.1-2
- Fix a unicode traceback https://bugzilla.redhat.com/show_bug.cgi?id=785622

* Thu Jan 5 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8.1-1
- Update to new upstream that has properly licensed files and a few bugfixes
- Add a patch to fix tracebacks when wrong values are given to CLI apps

* Wed Jul 20 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8-2
- Replace the Apache licensed files with BSD licensed versions from upstream

* Tue Jul 12 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8-1
- Upgrade to 0.8 final.
- Remove the two remaining Apache licensed files until their license is fixed.
- Patch regressions that we had already submitted upstream -- resubmit

* Tue May 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.8-0.1.20110517svn7036
- Ship a snapshot of 0.8 so that we can build on python-3.2.1
- Unfortunately, 3.2.1 isn't out yet either.  So also apply a fix for building
  with 3.2.0 that we'll need to remove later.
- The new docutils.math module is licensed Apache.  Update the license to reflect this

* Wed Mar 16 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7-5
- Fix building with python-3.2 via a workaround.  Sent upstream awaiting
  feedback or a better fix.  Built in rawhide.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 1 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7-3
- Fix scripts so they're the python2 versions not the python3 versions

* Thu Dec 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7-2
- Build for python3

* Sun Aug 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7-1
- Update for 0.7 release

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jan 19 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6-1
- Update for 0.6 release.
- Switch from setuptools installed egg-info to distutils egg-info.  Note that
  this works because we're also changing docutils version.  To do this between
  0.5-4 and 0.5-5, for instance, we'd need to have %%preun scriptlet to get rid
  of the egg-info directory.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5-2
- Rebuild for Python 2.6

* Wed Aug 6 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.5-1
- New upstream version.

* Mon Mar 3 2008 Toshio Kuratomi <toshio@fedoraproject.org> 0.4-8
- Use regular Requires syntax for python-imaging as missingok is just wrong.

* Thu Sep 27 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-7
- Build egg info.

* Mon Aug 13 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-6
- Last version had both the old and new rst.el.  Try again with only
  the new one.

* Sun Aug 12 2007 Toshio Kuratomi <a.badger@gmail.com> 0.4-5
- Make License tag conform to the new Licensing Policy.
- Fix the rst emacs mode (RH BZ 250100)

* Sat Dec 09 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-4
- Bump and rebuild for python 2.5 in devel.

* Tue Aug 29 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-3
- Bump for FC6 rebuild.
- Remove python byte compilation as this is handled automatically in FC4+.
- No longer %%ghost .pyo files.
  
* Thu Feb 16 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-2
- Bump and rebuild for FC5.
  
* Sun Jan 15 2006 Toshio Kuratomi <toshio-tiki-lounge.com> 0.4-1
- Update to 0.4.
- Scripted the listing of files in the python module.
- Add a missingok requirement on python-imaging as docutils can make use of
  it when converting to formats that have images.
  
* Tue Jun 7 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.9-1
- Update to version 0.3.9.
- Use a dist tag as there aren't any differences between supported fc
  releases (FC3, FC4, devel.)

* Thu May 12 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.7-7
- Bump version and rebuild to sync across architectures.

* Sun Mar 20 2005 Toshio Kuratomi <toshio-tiki-lounge.com> 0.3.7-6
- Rebuild for FC4t1

* Sat Mar 12 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0.3.7-5
- Add GPL as a license (mschwendt)
- Use versioned Obsoletes and Provides (mschwendt)

* Fri Mar 04 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-4
- Rename to python-docutils per the new packaging guidelines.

* Wed Jan 12 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.3
- Really install roman.py and build roman.py[co].  Needed to make sure I have
  docutils installed to test that it builds roman.py fine in that case.

* Tue Jan 11 2005 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.2
- Special case roman.py to always install.  This is the behaviour we want
  unless something else provides it.  Will need to watch out for this in
  future Core and Extras packages, but the auto detection code makes it
  possible that builds will not be reproducible if roman.py were installed
  from another package.... Lesser of two evils here.
- Provide python-docutils in case that package were preinstalled from
  another repository.
  
* Fri Dec 31 2004 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.7-0.fdr.1
- Update to 0.3.7
- Rename from python-docutils to docutils.
- Make roman.py optionally a part of the files list.  In FC2, this will be
  included.  In FC3, this won't.
- BuildConflict with self since the docutils build detects the presence
  of roman.py and doesn't reinstall itself.
  
* Mon Aug 9 2004 Toshio Kuratomi <toshio.tiki-lounge.com> 0:0.3.5-0.fdr.1
- Update to 0.3.5.
- Update spec style to latest fedora-rpmdevtools.
- Merge everything into a single package.  There isn't very much space
  advantage to having separate packages in a package this small and in
  this case, the documentation on using docutils as a library is also a
  good example of how to write in ReSructuredText.

* Sat Jan 10 2004 Michel Alexandre Salim <salimma[AT]users.sf.net> 0:0.3-0.fdr.1
- Initial RPM release.
