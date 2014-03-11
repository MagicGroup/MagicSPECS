%if (! 0%{?rhel}) || 0%{?rhel} > 6
%global with_python3 1
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}
%endif

# Enable building without html docs (e.g. in case no recent sphinx is
# available)
%global with_docs 1

Name:           waf
Version:        1.6.10
Release:        2%{?dist}
Summary:        A Python-based build system
Group:          Development/Tools
# The entire source code is BSD apart from pproc.py (taken from Python 2.5)
License:        BSD and Python
URL:            http://code.google.com/p/waf/
# Original tarfile can be found at
# http://waf.googlecode.com/files/waf-%%{version}.tar.bz2
# We remove:
# - /docs/book, as this is under CC-BY-NC-ND, which is not allowed in
#   Fedora
# - /waflib/extras/subprocess.py, is under a Python license and not
#   needed in Fedora
Source:         waf-%{version}.stripped.tar.bz2
# use _datadir instead of /usr/lib
Patch0:         waf-1.6.2-libdir.patch
Patch1:         waf-1.6.9-logo.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  python-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # with_python3
%if 0%{?with_docs}
%if 0%{?fedora > 13}
BuildRequires:  python-sphinx
%else
BuildRequires:  python-sphinx10
%endif
BuildRequires:  graphviz
BuildRequires:  ImageMagick
%endif # with_docs
%if "%{?python_version}" != ""
# Seems like automatic ABI dependency is not detected since the files are
# going to a non-standard location
Requires:       python(abi) = %{python_version}
%endif


# the demo suite contains a perl module, which draws in unwanted
# provides and requires
%global __requires_exclude_from %{_docdir}
%global __provides_exclude_from %{_docdir}
# for EPEL, we need the old filters
%global __perl_provides %{nil}
%global __perl_requires %{nil}


%description
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.


%if 0%{?with_python3}
%package -n %{name}-python3
Summary:        Python3 support for %{name}
%if "%{?python3_version}" != ""
Requires:       python(abi) = %{python3_version}
%endif

%description -n %{name}-python3
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the Python 3 version of %{name}.
%endif # with_python3


%if 0%{?with_docs}
%package -n %{name}-docs
Summary:        Documentation for %{name}

%description -n %{name}-docs
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the HTML documentation for %{name}.
%endif # with_docs


%prep
%setup -q
%patch0 -p0 -b .libdir
%patch1 -p1 -b .logo


%build
extras=
for f in waflib/extras/*.py ; do
  f=$(basename "$f" .py);
  if [ "$f" != "__init__" ]; then
    extras="${extras:+$extras,}$f" ;
  fi
done
./waf-light --make-waf --strip --tools="$extras"

%if 0%{?with_docs}
# build html docs
pushd docs/sphinx
%if ! 0%{?fedora > 13}
export SPHINX_BUILD=sphinx-1.0-build
%endif
../../waf configure build
popd
%endif # with_docs


%install
rm -rf %{buildroot}

# use waf so it unpacks itself
mkdir _temp ; pushd _temp
cp -av ../waf .
%{__python} ./waf >/dev/null 2>&1
pushd .waf-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf/{}
popd
%if 0%{?with_python3}
%{__python3} ./waf >/dev/null 2>&1
pushd .waf3-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf3/{}
popd
%endif # with_python3
popd

# install the frontend
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python_version}
%if 0%{?with_python3}
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python3_version}
%endif # with_python3
ln -s waf-%{python_version} %{buildroot}%{_bindir}/waf

# remove shebangs from and fix EOL for all scripts in wafadmin
find %{buildroot}%{_datadir}/ -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' -e 's|\r$||g' {} \;

# fix waf script shebang line
sed -i "1c#! %{__python}" %{buildroot}%{_bindir}/waf-%{python_version}
%if 0%{?with_python3}
sed -i "1c#! %{__python3}" %{buildroot}%{_bindir}/waf-%{python3_version}
%endif # with_python3

# remove x-bits from everything going to doc
find demos utils -type f -exec chmod 0644 {} \;

# remove hidden file
rm -f docs/sphinx/build/html/.buildinfo

%if 0%{?with_python3}
# do byte compilation
%py_byte_compile %{__python} %{buildroot}%{_datadir}/waf
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/waf3
%endif # with_python3


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README TODO ChangeLog demos
%{_bindir}/waf
%{_bindir}/waf-%{python_version}
%{_datadir}/waf


%if 0%{?with_python3}
%files -n %{name}-python3
%defattr(-,root,root,-)
%{_bindir}/waf-%{python3_version}
%{_datadir}/waf3
%endif # with_python3


%if 0%{?with_docs}
%files -n %{name}-docs
%defattr(-,root,root,-)
%doc docs/sphinx/build/html
%endif # with_docs


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6.10-2
- 为 Magic 3.0 重建

* Sun Dec 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.10-1
- Update to 1.6.10.
- Remove patch applied upstream.

* Sat Nov 26 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.9-1
- Update to 1.6.9.
- Patch to not use the logo (which has been removed) in the docs.

* Mon Oct  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.8-1
- Update to 1.6.8.
- Use rpm 4.9.X style provides/requires filtering.
- Move Python3 version to a subpackage.
- Move HTML documentation to a subpackage.

* Sat Jun 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.6-1
- Update to 1.6.6.
- Remove unused extras/subprocess.py.
- Small patch for syntax errors.

* Sun Apr 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.4-1
- Update to 1.6.4.

* Sat Apr  9 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.3-2
- Use python-sphinx10 where available.
- Turn off standard brp-python-bytecompile only when building the
  python3 subpackage.

* Sat Feb 19 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.3-1
- Update to 1.6.3.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-4
- Update libdir patch for py3k.
- Add patch to fix syntax error in extras/boost.py.
- Remove hidden file.

* Fri Jan 21 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-3
- Make waf compatible with python3, if available.

* Tue Jan 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-2
- Enable building without html docs.

* Sat Jan 15 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.6.2-1
- Update to 1.6.2.
- Generate and include html docs.
- Upstream removed the 'install' target, so we need to copy waflib
  manually.
- The bash completion file is not provided anymore.

* Fri Oct  1 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.19-1
- Update to 1.5.19.

* Fri Jul 30 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-3
- Require 'python(abi)' instead of 'python-abi', seems more common
  now.

* Fri Jul 30 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 11 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.18-1
- Update to 1.5.18.

* Mon May 24 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.17-1
- Update to 1.5.17.
- Add patch from issue 682 to install 3rd party tools.

* Mon Apr  5 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.15-1
- Update to 1.5.15.

* Sun Mar  7 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.14-1
- Update to 1.5.14.

* Wed Mar  3 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.13-1
- Update to 1.5.13.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.12-1
- Update to 1.5.12.

* Mon Jan 18 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.11-1
- Update to 1.5.11.
- Use %%global instead of %%define.

* Mon Nov 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.10-1
- Update to 1.5.10.

* Mon Aug 31 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.9-1
- Update to 1.5.9.
- Rebase libdir patch.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.8-1
- Update to 1.5.8.

* Tue May  5 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.6-1
- Update to 1.5.6.

* Mon Apr 20 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.5-1
- Update to 1.5.5.

* Tue Apr  7 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.4-1
- Update to 1.5.4.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.3-1
- Update to 1.5.3, which contains various enhancements and bugfixes,
  see http://waf.googlecode.com/svn/trunk/ChangeLog for a list of
  changes.

* Fri Jan 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-2
- Remove the documentation again, as it is under CC-BY-NC-ND. Also
  remove it from the tarfile.

* Fri Jan 16 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-1
- Update to 1.5.2.
- Generate html documentation (though without highlighting).

* Fri Dec 19 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.1-1
- Update to 1.5.1.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4.4-2
- Rebuild for Python 2.6

* Sun Aug 31 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-1
- Update to 1.4.4:
  - python 2.3 compatibility was restored
  - task randomization was removed
  - the vala tool was updated

* Sat Jun 28 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.3-1
- Update to 1.4.3.
- Remove fcntl patch (fixed upstream).
- Prefix has to be set in a configure step now.
- Pack the bash completion file.

* Mon May 26 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.2-2
- Patch: stdout might not be a terminal.

* Sat May 17 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.2-1
- Update to 1.4.2.
- Remove shebang lines from files in wafadmin after installation, not
  before, otherwise install will re-add them.

* Sun May  4 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.1-1
- Update to upstream version 1.4.1.

* Sat Apr 19 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.0-1
- Update to upstream version 1.4.0.

* Wed Apr  9 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-6
- Upstream patch to fix latex dependency scanning: trunk rev 2340.

* Sun Feb 10 2008 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-5
- Update to 1.3.2.
- Remove version and revision information from path to waf cache.

* Fri Feb  1 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-4
- Upstream patch to fix check_tool('gnome'): trunk rev 2219

* Mon Jan 28 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-3
- Fix python-abi requirement so it can be parsed before python is installed
- rpmlint tidying-up

* Fri Jan 25 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-2
- Merge in changes from Thomas Mochny <thomas.moschny@gmx.de>:
  * WAF cache moved from /usr/lib to /usr/share
  * Remove shebangs from scripts not meant from users, rather than
    making them executable
  * Include tools and demos

* Sun Jan 20 2008 Michel Salim <michel.sylvan@gmail.com> - 1.3.1-1
- Initial Fedora package

