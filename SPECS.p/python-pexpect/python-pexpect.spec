%global with_python3 1

%global modname pexpect
#global relcand rc3

Summary:	Unicode-aware Pure Python Expect-like module
Summary(zh_CN.UTF-8): 支持 Unicode 的类 Expect 纯 Python 模块
Name:		python-pexpect
Version:	4.0.1
Release:	2%{?dist}
License:	MIT
Group:		Development/Languages
Group(zh_CN.UTF-8): 开发/语言
URL:		https://github.com/pexpect/pexpect
Source0:	https://pypi.python.org/packages/source/p/pexpect/pexpect-%{version}.tar.gz

Patch0:         0001-Stop-asyncio-listening-to-pty-once-we-ve-found-what-.patch
Patch1:         0001-disable-max-canon-tests-retain-file-contents.patch
Patch2:         0002-2-new-tools-display-fpathconf.maxcanon-.py.patch


BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	python2-devel python-nose ed
%if 0%{?with_python3}
BuildRequires:	python3-devel python3-nose
Provides:	pexpect = %{version}-%{release}
Obsoletes:	pexpect <= 3.3-20
%endif # if with_python3

%description
Pexpect is a pure Python module for spawning child applications; controlling
them; and responding to expected patterns in their output. Pexpect works like
Don Libes' Expect. Pexpect allows your script to spawn a child application and
control it as if a human were typing commands.

Pexpect can be used for automating interactive applications such as ssh, ftp,
passwd, telnet, etc. It can be used to automate setup scripts for duplicating
software package installations on different servers. And it can be used for
automated software testing. Pexpect is in the spirit of Don Libes' Expect, but
Pexpect is pure Python. Unlike other Expect-like modules for Python, Pexpect
does not require TCL or Expect nor does it require C extensions to be
compiled.  It should work on any platform that supports the standard Python
pty module.

%description -l zh_CN.UTF-8
支持 Unicode 的类 Expect 纯 Python 模块。

%package -n python2-pexpect
Summary:	Unicode-aware Pure Python Expect-like module for Python 2
BuildRequires:	python2-devel
BuildRequires:  python2-pytest python-ptyprocess
Requires:       python-ptyprocess
Provides:	pexpect = %{version}-%{release}
Obsoletes:	pexpect <= 2.3-20
Provides:       python-pexpect = %{version}-%{release}
Obsoletes:      python-pexpect <= 3.3-20
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-pexpect
Pexpect is a pure Python module for spawning child applications; controlling
them; and responding to expected patterns in their output. Pexpect works like
Don Libes' Expect. Pexpect allows your script to spawn a child application and
control it as if a human were typing commands. This package contains the
python2 version of this module.

Pexpect can be used for automating interactive applications such as ssh, ftp,
passwd, telnet, etc. It can be used to automate setup scripts for duplicating
software package installations on different servers. And it can be used for
automated software testing. Pexpect is in the spirit of Don Libes' Expect, but
Pexpect is pure Python. Unlike other Expect-like modules for Python, Pexpect
does not require TCL or Expect nor does it require C extensions to be
compiled.  It should work on any platform that supports the standard Python
pty module.

%if 0%{?with_python3}
%package -n python3-pexpect
Summary:	Unicode-aware Pure Python Expect-like module for Python 3
Summary(zh_CN.UTF-8): 支持 Unicode 的类 Expect 纯 Python3 模块
Group:		Development/Languages
Group(zh_CN.UTF-8): 开发/语言

%description -n python3-pexpect
Pexpect is a pure Python module for spawning child applications; controlling
them; and responding to expected patterns in their output. Pexpect works like
Don Libes' Expect. Pexpect allows your script to spawn a child application and
control it as if a human were typing commands. This package contains the
python3 version of this module.

Pexpect can be used for automating interactive applications such as ssh, ftp,
passwd, telnet, etc. It can be used to automate setup scripts for duplicating
software package installations on different servers. And it can be used for
automated software testing. Pexpect is in the spirit of Don Libes' Expect, but
Pexpect is pure Python. Unlike other Expect-like modules for Python, Pexpect
does not require TCL or Expect nor does it require C extensions to be
compiled.  It should work on any platform that supports the standard Python
pty module.
%description -n python3-pexpect -l zh_CN.UTF-8
支持 Unicode 的类 Expect 纯 Python 模块。
%endif # with_python3

%prep
%autosetup -n %{modname}-%{version} -S git
chmod +x ./tools/*
#sed -i "s/0.1/10.0/g" tests/test_misc.py

rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%py2_build

pushd %{py3dir}
  %py3_build
popd

%install
%py2_install
rm -rf ${buildroot}%{python2_sitelib}/setuptools/tests
# Correct some permissions
find examples -type f -exec chmod a-x \{\} \;
rm -f %{buildroot}%{python2_sitelib}/%{modname}/async.py

pushd %{py3dir}
  %py3_install
  # Correct some permissions
  find examples -type f -exec chmod a-x \{\} \;
  rm -rf %{buildroot}%{python3_sitelib}/pexpect/tests
popd

%check
export PYTHONIOENCODING=UTF-8
export LC_ALL="en_US.UTF-8"

%{__python2} ./tools/display-sighandlers.py
%{__python2} ./tools/display-terminalinfo.py
PYTHONPATH=`pwd` %{__python2} ./tools/display-maxcanon.py
py.test-2 --verbose

pushd %{py3dir}
  %{__python3} ./tools/display-sighandlers.py
  %{__python3} ./tools/display-terminalinfo.py
  PYTHONPATH=`pwd` %{__python3} ./tools/display-maxcanon.py
  py.test-3 --verbose
popd

%files -n python2-%{modname}
%license LICENSE
%doc doc examples
%{python2_sitelib}/%{modname}*

%files -n python3-%{modname}
%license LICENSE
%doc doc examples
%{python3_sitelib}/%{modname}*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 4.0.1-2
- 更新到 4.0.1

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 3.3-1
- 更新到 3.3

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 3.1-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 08 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 3.1-1
- Update to 3.1

* Tue Nov 12 2013 Thomas Spura <tomspur@fedoraproject.org> - 3.0-1
- update to 3.0

* Wed Oct 30 2013 Thomas Spura <tomspur@fedoraproject.org> - 3.0-0.1
- new upstream is github/pexpect/pexpect
- update to rc3
- build on noarch again
- consistently use %%{buildroot} everywhere
- be more explicit in %%files
- remove CFLAGS

* Thu Sep 05 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-11
- Fix the name of the arm architecture in ExcludeArch

* Thu Sep 05 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-10
- Remove noarch because of arm build problems (bug #999174)

* Tue Aug 20 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-9
- Exclude the arm architecture (bug #999174)

* Tue Aug 20 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-8
- Bump the obsoletes version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-5
- Exclude test scripts from the files list

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-4
- Moved unit tests to a check section

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-3
- Added unit tests and fixed metadata fields

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-2
- Added versions to the obsoletes and provides fields

* Tue Nov 20 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.1-1
- Updated to version 2.5.1 (pexpect-u fork) and added support for Python 3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 2.3-3
- Rebuild for gcc 4.4 and rpm 4.6

* Fri Dec  5 2008 Jeremy Katz <katzj@redhat.com> - 2.3-2
- Rebuild for python 2.6

* Tue Jan 08 2008 Robert Scheck <robert@fedoraproject.org> 2.3-1
- Upgrade to 2.3
- Updated the source URL to match with the guidelines

* Wed Aug 29 2007 Robert Scheck <robert@fedoraproject.org> 2.1-5
- Rebuilt (and some minor spec file tweaks)

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-4
- Bump and rebuild because I forgot to cvs up before the last build.

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-3
- Bump and rebuild for python 2.5 on devel.
- Add BR: python-devel as it provides a header necessary for python modules
  on python 2.5.

* Fri Sep 01 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-2
- Remove pyver define as it's not needed with the automatic python(abi).
- Stop ghosting .pyos.
- Let automatic python compilation take care of creating pyos.
- Rebuild for FC6.

* Mon Jul 17 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.1-1
- Update to 2.1.

* Thu Feb 16 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.0-2
- Bump and rebuild for FC5.
- Convert from python-abi to python(abi) requires.

* Thu Nov 17 2005 Toshio Kuratomi <toshio@tiki-lounge.com> - 2.0-1
- Update to 2.0.

* Sat Sep 3 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.99999b-2
- Add LICENSE File.
- Make noarch.
- Remove executable permissions from the modules copied to examples.

* Fri Sep  2 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.99999b
- Update to version 0.99999b.
- Add dist tag.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 03 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 0.999-2
- Use python_sitelib macro to resolve build issues on x86_64.
- %%ghost *.pyo
- Install ANSI.py, screen.py, and FSM.py into the examples.  These are intended
  to suplement pexpect eventually but they are currently much less robust and
  not installed to by default.  But they are needed by some examples.
- Use __python macro in build/install for consistency.
- Add --skip-build to the invocation of setup.py in install.

* Mon May 31 2004 Panu Matilainen <pmatilai@welho.com> 0.999-0.fdr.1
- get rid of distrel munging, buildsys does that...
- update to 0.999
- update doc and example tarballs
- fix build on python <> 2.2
- use -O1 in install to generate .pyo files instead of manually creating the files
- require python-abi = pyver to get dependencies right

* Sun Jul 27 2003 Panu Matilainen <pmatilai@welho.com> 0.98-0.fdr.3
- own .pyo files too as suggested by Ville (#517)

* Sat Jul 26 2003 Panu Matilainen <pmatilai@welho.com> 0.98-0.fdr.2
- fixes by Ville (bug #517) applied

* Sat Jul 26 2003 Panu Matilainen <pmatilai@welho.com>
- Initial Fedora packaging

