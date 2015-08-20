%if 0%{?fedora}
%global with_python3 1
%endif
%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:           pygpgme
Version:        0.3
Release:        13%{?dist}
Summary:        Python module for working with OpenPGP messages

Group:          Development/Languages
License:        LGPLv2+
URL:            http://cheeseshop.python.org/pypi/pygpgme
# pygpgme is being developed for Ubuntu and built for Ubuntu out of
# launchpad's source control.  if we need to create a snapshot, here's how:
#
# Steps to create snapshot:
# bzr branch lp:pygpgme -r69
# cd pygpgme
# patch -p0 < ../pygpgme-examples.patch
# python setup.py sdist
# tarball is in dist/pygpgme-0.1.tar.gz
#Source0:        pygpgme-0.1.tar.gz
Source0:        http://cheeseshop.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source1:	https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
# 2013-08-22: Upstreamed 2013-05-14, upstream unresponsive:
# https://bugs.launchpad.net/pygpgme/+bug/1002421
# https://bugs.launchpad.net/pygpgme/+bug/1002421/+attachment/3676331/+files/gpgme-pubkey-hash-algo.patch
Patch0:         pygpgme-pubkey-hash-algo.patch
# 2013-08-22: Upstreamed 2013-06-19, upstream unresponsive:
# https://bugs.launchpad.net/pygpgme/+bug/1192545
# https://bugs.launchpad.net/pygpgme/+bug/1192545/+attachment/3707307/+files/pygpgme-no-encrypt-to.patch
Patch1:         pygpgme-no-encrypt-to.patch
BuildRequires:  python2-devel
BuildRequires:  gpgme-devel

%if 0%{?with_python3}
BuildRequires: python3-devel
%endif

%filter_provides_in %{python_sitearch}/gpgme/_gpgme.so
%filter_setup

%description
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.

%if 0%{?with_python3}
%package -n python3-pygpgme
Summary: Python3 module for working with OpenPGP messages
Group:   Development/Languages

%description -n python3-pygpgme
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.  This package installs the module for use with python3.
%endif

%prep
%setup -q
%patch0 -p0 -b .pubkey-hash-algo
%patch1 -p0 -b .no-encrypt-to

cp %{SOURCE1} .

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/gpgme/_gpgme.so

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT%{python3_sitearch}/gpgme/*.so
popd
%endif # with_python3

%clean
rm -rf $RPM_BUILD_ROOT

%check
### Can't run the tests unconditionally because they depend on importing a private key.
# gpg2 on which our gpgme library depends does not import private keys so this
# won't work.  The issue in the real world is not so big as we  don't
# manipulate private keys outside of a keyring that often.
# We'll run this and ignore errors so we can manually look for problems more easily
# Use the installed gpgme because it has the built compiled module
mv gpgme gpgme.bak
ln -s $RPM_BUILD_ROOT%{python_sitearch}/gpgme .
make check || :
find tests -name '*.pyc' -delete

%files
%defattr(-,root,root,-)
%doc README PKG-INFO examples tests
%{!?_licensedir:%global license %%doc}
%license lgpl-2.1.txt
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-pygpgme
%defattr(-,root,root,-)
%doc README PKG-INFO examples tests
%{!?_licensedir:%global license %%doc}
%license lgpl-2.1.txt
%{python3_sitearch}/*
%endif # with_python3

%changelog
* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 0.3-13
- 为 Magic 3.0 重建

* Sun Aug 10 2014 Liu Di <liudidi@gmail.com> - 0.3-12
- 为 Magic 3.0 重建

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 0.3-11
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Aug 22 2013 Till Maas <opensource@till.name> - 0.3-8
- Add patches for ENCRYPT_NO_ENCRYPT_TO, pubkey_algo and hash_algo (#975815)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Miloslav Trmač <mitr@redhat.com> - 0.3-5
- Disable -fstrict-aliasing (see http://www.python.org/dev/peps/pep-3123/ for
  rationale)
- Don't ship .pyc files from the test suite in %%doc, to avoid multilib
  conflicts

* Fri Nov 23 2012 Miloslav Trmač <mitr@redhat.com> - 0.3-4
- Don't build the python3 package on RHEL

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 0.3-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3-1
- New upstream release
- Build a python3 subpackage
- Run the test suite even though we ignore the output

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2-1
- Update for new upstream release.  Doesn't add any new code, just switches
  from a snapshot to a release and bumps version

* Fri Feb 11 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 22.20101027bzr69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild 

* Wed Oct 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 21.20101027bzr69
- New snapshot to fix BZ#647059: pygpgme error creating context on F14.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1-20.20090824bzr68
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Mar  4 2010 Miloslav Trmač <mitr@redhat.com> - 0.1-19.20090824bzr68
- Filter out bogus Provides: _gpgme.so
- Drop no longer required references to BuildRoot:
- s/%%define/%%global/g

* Wed Feb  3 2010 Miloslav Trmač <mitr@redhat.com> - 0.1-18.20090824bzr68
- Classify pygpgme-examples.patch as Source, not a Patch, to silence rpmlint

* Wed Oct 28 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-17.20090824bzr68
- Include tests and examples as documentation.

* Mon Aug 24 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-16.20090824bzr68
- Rebase to new upstream snapshot
- Patches merged upstream
- Fixes deprecation warnings on py2.6/py3.0
- Remove py2.3 patch -- only needed for EPEL-4

* Tue Jul 28 2009 Jesse Keating <jkeating@redhat.com> - 0.1-15.20090121bzr54
- Add a second patch from mitr for symmetric_encryption_support

* Tue Jul 28 2009 Jesse Keating <jkeating@redhat.com> - 0.1-14.20090121bzr54
- Patch from mitr for gpgme_ctx_set_engine_info

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-13.20090121bzr54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-12.20090121bzr54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-11.20090121bzr54
- Add patch to cvs.

* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-10.20090121bzr54
- Update to upstream snapshot.

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1-9
- Rebuild for Python 2.6

* Fri Feb 8 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-8
- Rebuild for new gcc.

* Thu Jan 3 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 0.1-7
- Include egg-info files.

* Fri May 18 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-6
- Rebuild to pick up enhancements from gcc on F-8.
- Update licensing to conform to new guidelines.

* Fri May 18 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-5
- Rebuild because of a bug in linking to an early version of the python-2.5
  package,

* Mon Oct 23 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-4
- Bump and rebuild for python 2.5 on devel.

* Mon Oct 23 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-3
- Add a patch to work under Python 2.3.
- Stop shipping the tests as they are useless to the end user.

* Fri Oct 13 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-2
- Change URL to cheeseshop

* Sun Oct 08 2006 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.1-1
- Initial build for Fedora Extras. 
