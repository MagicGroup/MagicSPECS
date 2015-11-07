%global with_python3 1
# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%{!?python3_version: %global python3_version %(%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])")}

# Enable building without html docs (e.g. in case no recent sphinx is
# available)
%global with_docs 1

# For pre-releases
%undefine prerel

Name:           waf
Version:	1.8.16
Release:	2%{?dist}
Summary:        A Python-based build system
Summary(zh_CN.UTF-8): 基于 Pyhton 的编译构建系统
Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
# The entire source code is BSD apart from pproc.py (taken from Python 2.5)
License:        BSD and Python
URL:            https://github.com/waf-project/waf
# Original tarfile can be found at
# https://waf.io/waf-%%{version}.tar.bz2 or
# http://www.freehackers.org/%7Etnagy/release/waf-%%{version}.tar.bz2
# We remove:
# - docs/book, licensed CC BY-NC-ND
# - Waf logos, licensed CC BY-NC
Source:         https://waf.io/waf-%{version}.tar.bz2
Patch0:         waf-1.8.11-libdir.patch
Patch1:         waf-1.6.9-logo.patch
Patch2:         waf-1.8.11-sphinx-no-W.patch

BuildArch:      noarch

BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # with_python3
%if 0%{?with_docs}
BuildRequires:  python-sphinx
BuildRequires:  graphviz
BuildRequires:  ImageMagick
%endif # with_docs
%if "%{?python2_version}" != ""
# Seems like automatic ABI dependency is not detected since the files are
# going to a non-standard location
Requires:       python(abi) = %{python2_version}
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

%description -l zh_CN.UTF-8
基于 Python 的配置、编译和安装程序框架。是类似 autotools, scons,
cmake 或 ant 的同类软件。

%if 0%{?with_python3}
%package -n %{name}-python3
Summary:        Python3 support for %{name}
Summary(zh_CN.UTF-8): %{name} 的 Python3 版本
%if "%{?python3_version}" != ""
Requires:       python(abi) = %{python3_version}
%endif

%description -n %{name}-python3
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the Python 3 version of %{name}.
%description -n %{name}-python3 -l zh_CN.UTF-8
基于 Python 的配置、编译和安装程序框架。是类似 autotools, scons,
cmake 或 ant 的同类软件。
这是 Python3 版本。
%endif # with_python3


%if 0%{?with_docs}
%package -n %{name}-doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
# obsolete the previous docs subpackage - guideline specifies -doc
# since: Fedora 18, RHEL 7 (mark the provides/obsoletes RHEL only after
# we no longer need to provide upgrade paths from affected Fedora releases)
Provides:       %{name}-docs = %{version}-%{release}
Obsoletes:      %{name}-docs < 1.6.11-2

%description -n %{name}-doc
Waf is a Python-based framework for configuring, compiling and
installing applications. It is a replacement for other tools such as
Autotools, Scons, CMake or Ant.

This package contains the HTML documentation for %{name}.
%endif # with_docs


%prep
%setup -q
# also search for waflib in /usr/share/waf
%patch0 -p1
# do not try to use the (removed) waf logos
%patch1 -p1
# do not add -W when running sphinx-build
%patch2 -p1


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
../../waf -v configure build
popd
%endif # with_docs


%install
# use waf so it unpacks itself
mkdir _temp ; pushd _temp
cp -av ../waf .
%{__python2} ./waf >/dev/null 2>&1
pushd .waf-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf/{}
popd
%if 0%{?with_python3}
# use waf so it unpacks itself
%{__python3} ./waf
pushd .waf3-%{version}-*
find . -name '*.py' -printf '%%P\0' |
  xargs -0 -I{} install -m 0644 -p -D {} %{buildroot}%{_datadir}/waf3/{}
popd
%endif # with_python3
popd

# install the frontend
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python2_version}
ln -s waf-%{python2_version} %{buildroot}%{_bindir}/waf-2
%if 0%{?with_python3}
install -m 0755 -p -D waf-light %{buildroot}%{_bindir}/waf-%{python3_version}
ln -s waf-%{python3_version} %{buildroot}%{_bindir}/waf-3
%endif # with_python3
ln -s waf-%{python2_version} %{buildroot}%{_bindir}/waf

# remove shebangs from and fix EOL for all scripts in wafadmin
find %{buildroot}%{_datadir}/ -name '*.py' \
     -exec sed -i -e '1{/^#!/d}' -e 's|\r$||g' {} \;

# fix waf script shebang line
sed -i "1c#! %{__python2}" %{buildroot}%{_bindir}/waf-%{python2_version}
%if 0%{?with_python3}
sed -i "1c#! %{__python3}" %{buildroot}%{_bindir}/waf-%{python3_version}
%endif # with_python3

# remove x-bits from everything going to doc
find demos utils -type f -exec chmod 0644 {} \;

# remove hidden file
rm -f docs/sphinx/build/html/.buildinfo

%if 0%{?with_python3}
# do byte compilation
%py_byte_compile %{__python2} %{buildroot}%{_datadir}/waf
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/waf3
%endif # with_python3
magic_rpm_clean.sh

%files
%doc README TODO ChangeLog demos
%{_bindir}/waf
%{_bindir}/waf-%{python2_version}
%{_bindir}/waf-2
%{_datadir}/waf


%if 0%{?with_python3}
%files -n %{name}-python3
%doc README TODO ChangeLog demos
%{_bindir}/waf-%{python3_version}
%{_bindir}/waf-3
%{_datadir}/waf3
%endif # with_python3


%if 0%{?with_docs}
%files -n %{name}-doc
%doc docs/sphinx/build/html
%endif # with_docs


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.8.16-2
- 更新到 1.8.16

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 1.8.15-1
- 更新到 1.8.15

* Sun Oct 11 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.14-1
- Update to 1.8.14.
- Include waf-2 and waf-3 symlinks, respectively.
- Add basic doc files to the python3 subpackage.

* Sat Jul 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.12-1
- Update to 1.8.12.

* Mon Jun 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.11-2
- Patch to remove -W from sphinx-build call, in order to build with
  older sphinx.
- Rebase libdir patch.

* Mon Jun 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.11-1
- Update to 1.8.11.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.9-1
- Update to 1.8.9.
- Update upstream URL.

* Sun Apr 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-2
- Project moved to github.

* Sun Apr 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.8-1
- Update to 1.8.8.
- Apply updated Python packaging guidelines.

* Sun Mar  1 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.7-1
- Update to 1.8.7.

* Sun Feb 22 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.6-1
- Update to 1.8.6.

* Thu Dec 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.5-1
- Update to 1.8.5.

* Sat Nov 22 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.4-1
- Update to 1.8.4.

* Sun Oct 12 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.2-1
- Update to 1.8.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.16-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.7.16-1.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 21 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.16-1
- Update to 1.7.16.
- Update download URL.

* Sat Jan 25 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.15-1
- Update to 1.7.15.
- Modernize spec file.

* Tue Jan  7 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.14-1
- Update to 1.7.14.

* Tue Sep 10 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.13-1
- Update to 1.7.13.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.11-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.11-1
- Update to 1.7.11.

* Fri Mar 22 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.10-1
- Update to 1.7.10.

* Sat Mar  9 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.9-2
- Add fix for FTBFS bug rhbz#914566.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.9-1
- Update to 1.7.9.

* Fri Dec 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.8-1
- Update to 1.7.8.

* Sun Dec 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.7-1
- Update to 1.7.7.

* Tue Nov 20 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.6-1
- Update to 1.7.6.

* Tue Oct  2 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.5-1
- Update to 1.7.5.

* Wed Sep 26 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.4-1
- Update to 1.7.4.

* Mon Aug  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.2-1
- Update to 1.7.2.

* Sat Aug  4 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.1-1
- Update to 1.7.1.
- Remove rhel logic from with_python3 conditional.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.7.0-1.2
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-1
- Update to 1.7.0.

* Sat Jun 16 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.2.pre5
- Update to 1.7.0pre5.

* Thu Jun  7 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.1.pre4
- Update to 1.7.0pre4.

* Thu Jun  7 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-0.2.pre3
- Add patch for waf issue #1171.
- Spec file fixes.

* Thu Jun  7 2012 Michel Salim <salimma@fedoraproject.org> - 1.7.0-0.1.pre3
- Update to 1.7.0pre3
- Spec clean-up
- Rename -docs subpackage to -doc, per guidelines

* Mon Feb  6 2012 Michel Salim <salimma@fedoraproject.org> - 1.6.11-1
- Update to 1.6.11
- Build in verbose mode

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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

