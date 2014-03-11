%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygpgme
Version:        0.2
Release:        3%{?dist}
Summary:        Python module for working with OpenPGP messages

Group:          Development/Languages
License:        LGPLv2+
URL:            http://cheeseshop.python.org/pypi/pygpgme/0.1
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
# Patch to make generating a tarball (sdist) work.  Applied prior to creating
# the Source0.  Submitted upstream.
Source1:        pygpgme-examples.patch
# The examples files that weren't included in upstream's release:
Source2: encrypt.py
BuildRequires:  python2-devel
BuildRequires:  gpgme-devel

%filter_provides_in %{python_sitearch}/gpgme/_gpgme.so
%filter_setup

%description
PyGPGME is a Python module that lets you sign, verify, encrypt and decrypt
files using the OpenPGP format.  It is built on top of GNU Privacy Guard and
the GPGME library.

%prep
%setup -q

mkdir examples
cp -pr %{SOURCE2} examples/

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/gpgme/_gpgme.so
# No need to ship the tests
mv $RPM_BUILD_ROOT%{python_sitearch}/gpgme/tests/ .

%clean
rm -rf $RPM_BUILD_ROOT

### Can't enable the tests because they depend on importing a private key.
# gpg2 on which our gpgme library depends does not import private keys so this
# won't work.  The issue in the real world is not so big as we  don't
# manipulate private keys outside of a keyring that often.
#%check
# Use the installed gpgme because it has the built compiled module
#mv gpgme gpgme.bak
#ln -s $RPM_BUILD_ROOT%{python_sitearch}/gpgme .
#python test_all.py

%files
%defattr(-,root,root,-)
%doc README PKG-INFO examples tests
%{python_sitearch}/*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.2-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 0.2-1
- Update for new upstream release.  Doesn't add any new code, just switches
  from a snapshot to a release and bumps version

* Fri Feb 11 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 22.20101027bzr69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild 

* Tue Oct 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 21.20101027bzr69
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
