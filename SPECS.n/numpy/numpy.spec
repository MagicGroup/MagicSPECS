%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

#uncomment next line for a release candidate or a beta
%global relc %{nil}

Name:           numpy
Version:        1.9.1
Release:        5%{?dist}
Epoch:          1
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
# Everything is BSD except for class SafeEval in numpy/lib/utils.py which is Python
License:        BSD and Python
URL:            http://www.numpy.org/
Source0:        http://downloads.sourceforge.net/numpy/%{name}-%{version}%{?relc}.tar.gz
# Upstream patch to fix xerbla linkage
# https://bugzilla.redhat.com/show_bug.cgi?id=1172834
Patch0:         https://github.com/numpy/numpy/pull/5392.patch

BuildRequires:  python2-devel lapack-devel python-setuptools gcc-gfortran atlas-devel python-nose
Requires:       python-nose
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
%endif
BuildRequires:  Cython

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       python-devel
Provides:       f2py = %{version}-%{release}
Obsoletes:      f2py <= 2.45.241_1927

%description f2py
This package includes a version of f2py that works properly with NumPy.

%if 0%{?with_python3}
%package -n python3-numpy
Summary:        A fast multidimensional array facility for Python

Group:          Development/Languages
License:        BSD
%description -n python3-numpy
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Group:          Development/Libraries
Requires:       python3-numpy = %{epoch}:%{version}-%{release}
Requires:       python3-devel
Provides:       python3-f2py = %{version}-%{release}
Obsoletes:      python3-f2py <= 2.45.241_1927

%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.
%endif # with_python3

%prep
%setup -q -n %{name}-%{version}%{?relc}
%patch0 -p1 -b .xerbla

# workaround for rhbz#849713
# http://mail.scipy.org/pipermail/numpy-discussion/2012-July/063530.html
rm numpy/distutils/command/__init__.py && touch numpy/distutils/command/__init__.py

# Atlas 3.10 library names
%if 0%{?fedora} >= 21
cat >> site.cfg <<EOF
[atlas]
library_dirs = %{_libdir}/atlas
atlas_libs = satlas
EOF
%endif

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%if 0%{?with_python3}
pushd %{py3dir}
env ATLAS=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py build
popd
%endif # with _python3

env ATLAS=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py build

%install
# first install python3 so the binaries are overwritten by the python2 ones
%if 0%{?with_python3}
pushd %{py3dir}
#%%{__python} setup.py install -O1 --skip-build --root %%{buildroot}
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python3} setup.py install --root %{buildroot}
pushd %{buildroot}%{_bindir} &> /dev/null
popd &> /dev/null

popd
%endif # with_python3

#%%{__python} setup.py install -O1 --skip-build --root %%{buildroot}
# skip-build currently broken, this works around it for now
env ATLAS=%{_libdir} FFTW=%{_libdir} BLAS=%{_libdir} \
    LAPACK=%{_libdir} CFLAGS="%{optflags}" \
    %{__python} setup.py install --root %{buildroot}
pushd %{buildroot}%{_bindir} &> /dev/null
# symlink for anyone who was using f2py.numpy
ln -s f2py f2py.numpy
popd &> /dev/null
install -D -p -m 0644 doc/f2py/f2py.1 %{buildroot}%{_mandir}/man1/f2py.1

#symlink for includes, BZ 185079
mkdir -p %{buildroot}/usr/include
ln -s %{python_sitearch}/%{name}/core/include/numpy/ %{buildroot}/usr/include/numpy


%check
pushd doc &> /dev/null
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%if 0%{?with_python3}
pushd doc &> /dev/null
# there is no python3-nose yet
PYTHONPATH="%{buildroot}%{python3_sitearch}" %{__python3} -c "import pkg_resources, numpy ; numpy.test()" \
%ifarch s390 s390x
|| :
%endif
# don't remove this comment
popd &> /dev/null

%endif # with_python3


%files
%doc LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/*.py*
%{python_sitearch}/%{name}/core
%{python_sitearch}/%{name}/distutils
%{python_sitearch}/%{name}/doc
%{python_sitearch}/%{name}/fft
%{python_sitearch}/%{name}/lib
%{python_sitearch}/%{name}/linalg
%{python_sitearch}/%{name}/ma
%{python_sitearch}/%{name}/random
%{python_sitearch}/%{name}/testing
%{python_sitearch}/%{name}/tests
%{python_sitearch}/%{name}/compat
%{python_sitearch}/%{name}/matrixlib
%{python_sitearch}/%{name}/polynomial
%{python_sitearch}/%{name}-*.egg-info
%{_includedir}/numpy

%files f2py
%doc doc/f2py/*.txt
%{_mandir}/man*/*
%{_bindir}/f2py
%{_bindir}/f2py.numpy
%{python_sitearch}/%{name}/f2py

%if 0%{?with_python3}
%files -n python3-numpy
%doc LICENSE.txt README.txt THANKS.txt DEV_README.txt COMPATIBILITY site.cfg.example
%{python3_sitearch}/%{name}/__pycache__
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}/*.py*
%{python3_sitearch}/%{name}/core
%{python3_sitearch}/%{name}/distutils
%{python3_sitearch}/%{name}/doc
%{python3_sitearch}/%{name}/fft
%{python3_sitearch}/%{name}/lib
%{python3_sitearch}/%{name}/linalg
%{python3_sitearch}/%{name}/ma
%{python3_sitearch}/%{name}/random
%{python3_sitearch}/%{name}/testing
%{python3_sitearch}/%{name}/tests
%{python3_sitearch}/%{name}/compat
%{python3_sitearch}/%{name}/matrixlib
%{python3_sitearch}/%{name}/polynomial
%{python3_sitearch}/%{name}-*.egg-info

%files -n python3-numpy-f2py
%{_bindir}/f2py3
%{python3_sitearch}/%{name}/f2py
%endif # with_python3


%changelog
* Wed Nov 11 2015 Liu Di <liudidi@gmail.com> - 1:1.9.1-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1:1.9.1-4
- 为 Magic 3.0 重建

* Sat Feb 28 2015 Liu Di <liudidi@gmail.com> - 1:1.9.1-3
- 为 Magic 3.0 重建

* Tue Jan 6 2015 Orion Poplawski <orion@nwra.com> - 1:1.9.1-2
- Add upstream patch to fix xerbla linkage (bug #1172834)

* Tue Nov 04 2014 Jon Ciesla <limburgher@gmail.com> - 1:1.9.1-1
- Update to 1.9.1, BZ 1160273.

* Sun Sep 7 2014 Orion Poplawski <orion@nwra.com> - 1:1.9.0-1
- Update to 1.9.0

* Wed Aug 27 2014 Orion Poplawski <orion@nwra.com> - 1:1.9.0-0.1.rc1
- Update to 1.9.0rc1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 10 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.2-1
- Update to 1.8.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 9 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.1-3
- Rebuild for Python 3.4

* Wed May 07 2014 Jaromir Capik <jcapik@redhat.com> - 1:1.8.1-2
- Fixing FTBFS on ppc64le (#1078354)

* Tue Mar 25 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.1-1
- Update to 1.8.1

* Tue Mar 4 2014 Orion Poplawski <orion@nwra.com> - 1:1.8.0-5
- Fix __pycache__ ownership (bug #1072467)

* Mon Feb 10 2014 Thomas Spura <tomspur@fedoraproject.org> - 1:1.8.0-4
- Fix CVE-2014-1858, CVE-2014-1859: #1062009, #1062359

* Mon Nov 25 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-3
- Ship doc module (bug #1034357)

* Wed Nov 6 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-2
- Move f2py documentation to f2py package (bug #1027394)

* Wed Oct 30 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-1
- Update to 1.8.0 final

* Mon Oct 14 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.7.rc2
- Update to 1.8.0rc2
- Create clean site.cfg
- Use serial atlas

* Mon Sep 23 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.6.b2
- Add [atlas] to site.cfg for new atlas library names

* Sun Sep 22 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.5.b2
- Update site.cfg for new atlas library names

* Sat Sep 21 2013 David Tardon <dtardon@redhat.com> - 1:1.8.0-0.4.b2
- rebuild for atlas 3.10

* Tue Sep 10 2013 Jon Ciesla <limburgher@gmail.com> - 1:1.8.0-0.3.b2
- Fix libdir path in site.cfg, BZ 1006242.

* Sun Sep 8 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.2.b2
- Update to 1.8.0b2

* Wed Sep 4 2013 Orion Poplawski <orion@nwra.com> - 1:1.8.0-0.1.b1
- Update to 1.8.0b1
- Drop f2py patch applied upstream

* Tue Aug 27 2013 Jon Ciesla <limburgher@gmail.com> - 1:1.7.1-5
- URL Fix, BZ 1001337

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Tomas Tomecek <ttomecek@redhat.com> - 1:1.7.1-3
- Fix rpmlint warnings
- Update License
- Apply patch: change shebang of f2py to use binary directly

* Sun Jun 2 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.1-2
- Specfile cleanup (bug #969854)

* Wed Apr 10 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.1-1
- Update to 1.7.1

* Sat Feb 9 2013 Orion Poplawski <orion@nwra.com> - 1:1.7.0-1
- Update to 1.7.0 final

* Sun Dec 30 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.5.rc1
- Update to 1.7.0rc1

* Thu Sep 20 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.4.b2
- Update to 1.7.0b2
- Drop patches applied upstream

* Wed Aug 22 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.3.b1
- Add patch from github pull 371 to fix python 3.3 pickle issue
- Remove cython .c source regeneration - fails now

* Wed Aug 22 2012 Orion Poplawski <orion@nwra.com> - 1:1.7.0-0.2.b1
- add workaround for rhbz#849713 (fixes FTBFS)

* Tue Aug 21 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.7.0-0.1.b1
- Update to 1.7.0b1
- Rebase python 3.3 patchs to current git master
- Drop patches applied upstream

* Sun Aug  5 2012 David Malcolm <dmalcolm@redhat.com> - 1:1.6.2-5
- rework patches for 3.3 to more directly reflect upstream's commits
- re-enable test suite on python 3
- forcibly regenerate Cython .c source to avoid import issues on Python 3.3

* Sun Aug  5 2012 Thomas Spura <tomspur@fedoraproject.org> - 1:1.6.2-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3
- needs unicode patch

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1:1.6.2-3
- remove rhel logic from with_python3 conditional

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 20 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.2-1
- Update to 1.6.2 final

* Sat May 12 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.2rc1-0.1
- Update to 1.6.2rc1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 7 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.1-1
- Update to 1.6.1

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> - 1:1.6.0-2
- Bump and rebuild for BZ 712251.

* Mon May 16 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-1
- Update to 1.6.0 final

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-0.2.b2
- Update to 1.6.0b2
- Drop import patch fixed upstream

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.6.0-0.1.b1
- Update to 1.6.0b1
- Build python3  module with python3
- Add patch from upstream to fix build time import error

* Wed Mar 30 2011 Orion Poplawski <orion@cora.nwra.com> - 1:1.5.1-1
- Update to 1.5.1 final

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Dan Horák <dan[at]danny.cz> - 1:1.5.1-0.3
- fix the AttributeError during tests
- fix build on s390(x)

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.1-0.2
- rebuild for newer python3

* Wed Oct 27 2010 Thomas Spura <tomspur@fedoraproject.org> - 1:1.5.1-0.1
- update to 1.5.1rc1
- add python3 subpackage
- some spec-cleanups

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-6
- actually add the patch this time

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-5
- fix segfault within %%check on 2.7 (patch 2)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 18 2010 Dan Horák <dan[at]danny.cz> 1.4.1-3
- ignore the "Ticket #1299 second test" failure on s390(x)

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-2
- source commit fix

* Thu Jun 24 2010 Jef Spaleta <jspaleta@fedoraprject.org> 1.4.1-1
- New upstream release. Include backported doublefree patch

* Mon Apr 26 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-8
- Moved distutils back to the main package, BZ 572820.

* Thu Apr 08 2010 Jon Ciesla <limb@jcomserv.net> 1.3.0-7
- Reverted to 1.3.0 after upstream pulled 1.4.0, BZ 579065.

* Tue Mar 02 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-5
- Linking /usr/include/numpy to .h files, BZ 185079.

* Tue Feb 16 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-4
- Re-enabling atlas BR, dropping lapack Requires.

* Wed Feb 10 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-3
- Since the previous didn't work, Requiring lapack.

* Tue Feb 09 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-2
- Temporarily dropping atlas BR to work around 562577.

* Fri Jan 22 2010 Jon Ciesla <limb@jcomserv.net> 1.4.0-1
- 1.4.0.
- Dropped ARM patch, ARM support added upstream.

* Tue Nov 17 2009 Jitesh Shah <jiteshs@marvell.com> - 1.3.0-6.fa1
- Add ARM support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-5
- Fixed atlas BR, BZ 505376.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-4
- EVR bump for pygame chainbuild.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-3
- Moved linalg, fft back to main package.

* Tue Apr 14 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-2
- Split out f2py into subpackage, thanks Peter Robinson pbrobinson@gmail.com.

* Tue Apr 07 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-1
- Update to latest upstream.
- Fixed Source0 URL.

* Thu Apr 02 2009 Jon Ciesla <limb@jcomserv.net> 1.3.0-0.rc1
- Update to latest upstream.

* Thu Mar 05 2009 Jon Ciesla <limb@jcomserv.net> 1.2.1-3
- Require python-devel, BZ 488464.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 19 2008 Jon Ciesla <limb@jcomserv.net> 1.2.1-1
- Update to 1.2.1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.0-2
- Rebuild for Python 2.6

* Tue Oct 07 2008 Jon Ciesla <limb@jcomserv.net> 1.2.0-1
- New upstream release, added python-nose BR. BZ 465999.
- Using atlas blas, not blas-devel. BZ 461472.

* Wed Aug 06 2008 Jon Ciesla <limb@jcomserv.net> 1.1.1-1
- New upstream release

* Thu May 29 2008 Jarod Wilson <jwilson@redhat.com> 1.1.0-1
- New upstream release

* Tue May 06 2008 Jarod Wilson <jwilson@redhat.com> 1.0.4-1
- New upstream release

* Mon Feb 11 2008 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-2
- Add python egg to %%files on f9+

* Wed Aug 22 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3.1-1
- New upstream release

* Wed Jun 06 2007 Jarod Wilson <jwilson@redhat.com> 1.0.3-1
- New upstream release

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-2
- Drop BR: atlas-devel, since it just provides binary-compat
  blas and lapack libs. Atlas can still be optionally used
  at runtime. (Note: this is all per the atlas maintainer).

* Mon May 14 2007 Jarod Wilson <jwilson@redhat.com> 1.0.2-1
- New upstream release

* Tue Apr 17 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-4
- Update gfortran patch to recognize latest gfortran f95 support
- Resolves rhbz#236444

* Fri Feb 23 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-3
- Fix up cpuinfo bug (#229753). Upstream bug/change:
  http://projects.scipy.org/scipy/scipy/ticket/349

* Thu Jan 04 2007 Jarod Wilson <jwilson@redhat.com> 1.0.1-2
- Per discussion w/Jose Matos, Obsolete/Provide f2py, as the
  stand-alone one is no longer supported/maintained upstream

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.0.1-1
- New upstream release

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.0-2
- Rebuild for python 2.5

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.0-1
- New upstream release

* Wed Sep 06 2006 Jarod Wilson <jwilson@redhat.com> 0.9.8-1
- New upstream release

* Wed Apr 26 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.6-1
- Upstream update

* Thu Feb 16 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.5-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-2
- Rebuild for Fedora Extras 5

* Thu Feb  2 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.9.4-1
- Initial RPM release
- Added gfortran patch from Neal Becker
