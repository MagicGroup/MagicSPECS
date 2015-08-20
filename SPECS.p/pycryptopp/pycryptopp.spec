Name:           pycryptopp
Version:        0.6.0.1206569328141510525648634803928199668821045408958
Release:        5%{?dist}
Summary:        Python wrappers for the Crypto++ library
Summary(zh_CN.UTF-8): Crypto++ 库的 Python 接口

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言

# we don't use the embedded cryptopp library
# but link against the one in Fedora
# 
# all the files we distribute in the binary rpm
# are GPLv2+ or TGPPL
#
# see copyright for details
License:        GPLv2+

URL:     https://tahoe-lafs.org/trac/pycryptopp
Source0: http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  python-devel, cryptopp-devel, python-setuptools

%description
PyCryptopp is a set of Python wrappers for a few
of the best crypto algorithms from the Crypto++ library
(including SHA-256, AES, RSA signatures and Elliptic Curve DSA signatures).

%description -l zh_CN.UTF-8
Crypto++ 库的 Python 接口。

%prep
%setup -q

rm -rf darcsver-*.egg
rm -rf setuptools_darcs-*.egg

%build
CFLAGS="%{optflags}" %{__python} setup.py build --disable-embedded-cryptopp


%install
%{__python} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_docdir}/%{name}/

# This file isn't needed.  It's used to mark the embedded crytopp as having
# come from pycrypto.  We're not installing the embedded version.
rm -rf %{buildroot}/%{_prefix}/cryptopp/extraversion.h
magic_rpm_clean.sh

%check
CFLAGS="%{optflags}" %{__python} setup.py test

# tests are done, remove them
rm -rf %{buildroot}%{python_sitearch}/%{name}/test/
rm -rf %{buildroot}%{python_sitearch}/%{name}/testvectors/

%files
%defattr(-,root,root,-)
%doc COPYING.GPL COPYING.TGPPL.html README.rst ChangeLog copyright
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}-%{version}-*.egg-info

%changelog
* Wed Aug 12 2015 Liu Di <liudidi@gmail.com> - 0.6.0.1206569328141510525648634803928199668821045408958-5
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.1206569328141510525648634803928199668821045408958-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.1206569328141510525648634803928199668821045408958-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.1206569328141510525648634803928199668821045408958-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 01 2012 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.6.0.1206569328141510525648634803928199668821045408958-1
- Upstream released new version
- Drop unneeded patch

* Sun Jan 22 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 0.5.29-3
- Update URL field to new upstream website

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.29-1
- Upstream released new version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.5.25-2
- Rebuilt for gcc bug 634757

* Tue Jul 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.25-1
- Update release at upstream's request.  The source code looks reasonably safe

* Tue Jul 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.19-4
- Bumping release so we can rebuild this in the py27 rebuild tag

* Tue Jul 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> 0.5.19-3
- Remove the bundled modules
- Patch so we build without hte bundled modules

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 24 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.19-1
- Upstream released new version

* Mon Dec 21 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.17-5
- Rebuild for new cryptopp

* Mon Nov 16 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.17-4
- Initial import into devel

* Wed Nov 11 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.17-2
- Review fixes (#521719)

* Thu Sep 24 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.17-1
- Upstream released new version

* Mon Sep 14 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.15-3
- Review cleanup (#521719)

* Wed Sep 09 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.15-2
- Fix segfaults (upstream change #669)

* Tue Sep 08 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.5.15-1
- Initial import

