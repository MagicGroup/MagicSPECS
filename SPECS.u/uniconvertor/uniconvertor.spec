%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%global SVN 362

Name:           uniconvertor
Version:        2.0
Release:        0.9%{?SVN:.svn%{SVN}}%{?dist}
Summary:        Universal vector graphics translator
Summary(zh_CN.UTF-8): 通用的向量图形转换程序

Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        LGPLv2+ and GPLv2+ and MIT
URL:            http://sk1project.org/modules.php?name=Products&product=uniconvertor
# Script to reproduce given tarball from source0
Source1:        %{name}.get.tarball.svn
Source0:        %{name}-%{version}svn%{SVN}.tar.xz

BuildRequires:  python-devel, pycairo-devel, python-pillow-devel, lcms2-devel
BuildRequires:  potrace-devel
# For a public domain sRGB.icm
BuildRequires:  argyllcms
Requires:       python-imaging, python-reportlab, python-pillow, pycairo


%description
UniConvertor is a universal vector graphics translator.
It uses sK1 engine to convert one format to another.

%description -l zh_CN.UTF-8
通用的向量图形转换程序。

%prep
%setup -q
cp -a /usr/share/color/argyll/ref/sRGB.icm src/unittests/cms_tests/cms_data/sRGB.icm

%build
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/python2.7/Imaging" python setup.py build

%install
python setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%post
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%doc README LICENSE GPLv3.txt
%{_bindir}/%{name}
%{python_sitearch}/*
%{_datarootdir}/mime-info/sk1project.keys
%{_datarootdir}/mime-info/sk1project.mime
%{_datarootdir}/mime/packages/vnd.sk1project.pdxf-graphics.xml

%changelog
* Fri Oct 16 2015 Liu Di <liudidi@gmail.com> - 2.0-0.9.svn362
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.8.svn362
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Sep 27 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.7.svn362
- add (optimized) mime scriptlet

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.6.svn362
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.5.svn362
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 21 2014 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0-0.4.svn362
- Add pycairo require (bz#1079342).

* Sat Oct 19 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0-0.3.svn362
- New build to fix bz#1013652
- Add BR potrace-devel

* Tue Sep  3 2013 Tom Callaway <spot@fedoraproject.org> - 2.0-0.2.svn344
- fix tarball generation script to remove non-free sRGB.icm
- update to cleaned svn344 tarball
- use Public Domain sRGB.icm from argyllcms

* Sat Aug 24 2013 Pavel Alexeev <Pahan@Hubbitus.info> - 2.0-0.1.svn340
- First attempt packaging 2.0 version. Igor Novikov said in mail it is almost ready.
- New build with hope to fix compatability with python-pillow instead of PIL (by author mail)
- Add BR lcms2-devel
- Add script to get tarball from svn.
- Replace $RPM_BUILD_ROOT by %%{buildroot}
- Add BR pycairo-devel, python-pillow-devel
- Add require python-pillow
- Drop 1.x branch patches.
- Spec cleanup.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Andy Shevchenko <andy@smile.org.ua> - 1.1.4-1
- update to 1.1.4
- remove upstreamed patches
- adjust Fedora related patches

* Sat May 02 2009 Andy Shevchenko <andy@smile.org.ua> - 1.1.3-6
- Fix WMF saver

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Andy Shevchenko <andy@smile.org.ua> - 1.1.3-4
- cover code in __init__.py by function (#484301)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.3-3
- Rebuild for Python 2.6

* Sun Jul 27 2008 Andy Shevchenko <andy@smile.org.ua> 1.1.3-2
- update to 1.1.3
- new requirement python-reportlab

* Sun May 04 2008 Andy Shevchenko <andy@smile.org.ua> 1.1.2-2
- update to 1.1.2
- apply two useful patches from Debian

* Thu Mar 06 2008 Andy Shevchenko <andy@smile.org.ua> 1.1.1-2
- just fix Source0 URL

* Wed Feb 13 2008 Andy Shevchenko <andy@smile.org.ua> 1.1.1-1
- update to 1.1.1

* Sat Jan 12 2008 Andy Shevchenko <andy@smile.org.ua> 1.1.0-1
- update to 1.1.0

* Thu Nov 29 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.0-5
- fix conflict with netatalk: rename uniconv to uniconvertor (#405011)

* Thu Nov 22 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.0-4
- use python_sitearch and CFLAGS

* Thu Nov 22 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.0-3
- prepare to include to Fedora
  (https://bugzilla.redhat.com/show_bug.cgi?id=393971)

* Tue Nov 20 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.0-2
- adjust License: tag (thanks Tom 'spot' Callaway)

* Thu Nov 15 2007 Andy Shevchenko <andy@smile.org.ua> 1.0.0-1
- initial build

