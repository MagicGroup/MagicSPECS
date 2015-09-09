%global srcname paramiko

Name:          python-paramiko
Version:       1.15.2
Release:       4%{?dist}
Summary:       SSH2 protocol library for python
Summary(zh_CN.UTF-8): python 的 SSH2 协议库

Group:         Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# No version specified.
License:       LGPLv2+
URL:           https://github.com/paramiko/paramiko/
Source0:       http://pypi.python.org/packages/source/p/paramiko/paramiko-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: python-setuptools
BuildRequires: python-crypto >= 2.1
BuildRequires: python-ecdsa
BuildRequires: python-devel
Requires:      python-crypto >= 2.1
Requires:      python-ecdsa

%global paramiko_desc \
Paramiko (a combination of the esperanto words for "paranoid" and "friend") is\
a module for python 2.3 or greater that implements the SSH2 protocol for secure\
(encrypted and authenticated) connections to remote machines. Unlike SSL (aka\
TLS), the SSH2 protocol does not require heirarchical certificates signed by a\
powerful central authority. You may know SSH2 as the protocol that replaced\
telnet and rsh for secure access to remote shells, but the protocol also\
includes the ability to open arbitrary channels to remote services across an\
encrypted tunnel. (This is how sftp works, for example.)\

%description
%{paramiko_desc}

%description -l zh_CN.UTF-8
python 的 SSH2 协议库。

%package -n python3-%{srcname}
Summary:       SSH2 protocol library for python
Summary(zh_CN.UTF-8): python3 的 SSH2 协议库
BuildRequires: python3-setuptools
BuildRequires: python3-crypto >= 2.1
BuildRequires: python3-ecdsa
BuildRequires: python3-devel
Requires:      python3-crypto >= 2.1
Requires:      python3-ecdsa

%description -n python3-%{srcname}
%{paramiko_desc}

This is the python3 build.

%description -n python3-%{srcname} -l zh_CN.UTF-8
python3 的 SSH2 协议库。

%package doc
Summary:       Docs and demo for SSH2 protocol library for python
Summary(zh_CN.UTF-8): %{name} 的文档
Requires:      %{name} = %{version}-%{release}

%description doc
%{paramiko_desc}

This is the documentation and demos.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{srcname}-%{version}

chmod a-x demos/*
sed -i -e '/^#!/,1d' demos/*
rm -rf %{py3dir}
cp -a . %{py3dir}

%build
%{__python2} setup.py build

pushd %{py3dir}
  %{__python3} setup.py build
popd

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

pushd %{py3dir}
  %{__python3} setup.py install --skip-build --root %{buildroot}
popd
magic_rpm_clean.sh

%check
%{__python2} ./test.py --no-sftp --no-big-file

pushd %{py3dir}
  %{__python3} ./test.py --no-sftp --no-big-file
popd

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc PKG-INFO README
%{python2_sitelib}/*

%files -n python3-%{srcname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc PKG-INFO README
%{python3_sitelib}/*

%files doc
%doc docs/ demos/


%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.15.2-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.15.2-2
- Use %%license
- Move duplicated docs to single doc sub package
- Remove old F-15 conditionals

* Tue Dec 23 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.2-1
- Update to 1.15.2

* Mon Nov 24 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-5
- Add conditional to exclude EL since does not have py3

* Sat Nov 15 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-4
- py3dir creation should be in prep section

* Fri Nov 14 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-3
- Build each pkg in a clean dir

* Fri Nov 14 2014 Athmane Madjoudj <athmane@fedoraproject.org> 1.15.1-2
- Add support for python3
- Add BR -devel for python macros.

* Fri Oct 17 2014 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.15.1-1
- Update to 1.15.1

* Fri Jun 13 2014 Orion Poplawski <orion@cora.nwra.com> - 1.12.4-1
- Update to 1.12.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Orion Poplawski <orion@cora.nwra.com> - 1.12.2-1
- Update to 1.12.2

* Wed Jan 22 2014 Orion Poplawski <orion@cora.nwra.com> - 1.11.3-1
- Update to 1.11.3

* Mon Oct 21 2013 Orion Poplawski <orion@cora.nwra.com> - 1.11.0-1
- Update to 1.11.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Jeffrey Ollie <jeff@ocjtech.us> - 1.10.1-1
- Update to 1.10.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Jeffrey Ollie <jeff@ocjtech.us> - 1.9.0-1
- Update to 1.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.7.1-1
- v1.7.7.1 (George) 21may11
- -------------------------
-   * Make the verification phase of SFTP.put optional (Larry Wright)
-   * Patches to fix AIX support (anonymous)
-   * Patch from Michele Bertoldi to allow compression to be turned on in the
-     client constructor.
-   * Patch from Shad Sharma to raise an exception if the transport isn't active
-     when you try to open a new channel.
-   * Stop leaking file descriptors in the SSH agent (John Adams)
-   * More fixes for Windows address family support (Andrew Bennetts)
-   * Use Crypto.Random rather than Crypto.Util.RandomPool
-     (Gary van der Merwe, #271791)
-   * Support for openssl keys (tehfink)
-   * Fix multi-process support by calling Random.atfork (sugarc0de)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 4 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.6-3
- Patch to address deprecation warning from pycrypto
- Simplify build as shown in new python guidelines
- Enable test suite

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Nov  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.6-1
- v1.7.6 (Fanny) 1nov09
- ---------------------
-  * fixed bugs 411099 (sftp chdir isn't unicode-safe), 363163 & 411910 (more
-    IPv6 problems on windows), 413850 (race when server closes the channel),
-    426925 (support port numbers in host keys)

* Tue Oct 13 2009 Jeremy Katz <katzj@fedoraproject.org> - 1.7.5-2
- Fix race condition (#526341)

* Thu Jul 23 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.5-1
- v1.7.5 (Ernest) 19jul09
- -----------------------
-  * added support for ARC4 cipher and CTR block chaining (Denis Bernard)
-  * made transport threads daemonize, to fix python 2.6 atexit behavior
-  * support unicode hostnames, and IP6 addresses (Maxime Ripard, Shikhar
-    Bhushan)
-  * various small bug fixes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-4
- Add demos as documentation. BZ#485742

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.7.4-3
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.4-2
- fix license tag

* Sun Jul  6 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.4-1
- Update to 1.7.4

* Mon Mar 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.3-1
- Update to 1.7.3.

* Tue Jan 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.2-1
- Update to 1.7.2.
- Remove upstreamed patch.

* Mon Jan 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-3
- Update to latest Python packaging guidelines.
- Apply patch that fixes insecure use of RandomPool.

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-2
- Bump rev

* Thu Jul 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- Update to 1.7.1

* Sat Dec 09 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 1.6.4-1
- Update to 1.6.4
- Upstream is now shipping tarballs
- Bump for python 2.5 in devel

* Mon Oct  9 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-1
- Update to 1.6.2

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.6.1-3
- Rebuild for FC6

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.6.1-2
- Include, don't ghost .pyo files per new guidelines

* Tue Aug 08 2006 Shahms E. King <shahms@shahms.com> 1.6.1-1
- Update to new upstream version

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.6-1
- Update to new upstream version
- ghost the .pyo files

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-2
- Fix source line and rebuild

* Fri May 05 2006 Shahms E. King <shahms@shahms.com> 1.5.4-1
- Update to new upstream version

* Wed Apr 12 2006 Shahms E. King <shahms@shahms.com> 1.5.3-1
  - Initial package
