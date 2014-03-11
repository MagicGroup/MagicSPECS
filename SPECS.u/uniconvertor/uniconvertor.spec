%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           uniconvertor
Version:        1.1.4
Release:        7%{?dist}
Summary:        Universal vector graphics translator

Group:          Applications/Multimedia
License:        LGPLv2+ and GPLv2+ and MIT
URL:            http://sk1project.org/modules.php?name=Products&product=uniconvertor
Source0:        http://sk1project.org/downloads/uniconvertor/v%{version}/%{name}-%{version}.tar.gz
# Upstream notified via forum: http://sk1project.org/forum/topic.php?forum=2&topic=19
Patch0:         UniConvertor-1.1.0-simplify.patch
# Upstream notified via forum: http://sk1project.org/forum/topic.php?forum=2&topic=11
Patch1:         UniConvertor-1.1.1-rename-in-help.patch
Patch2:         UniConvertor-1.1.1-use-exec.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
Requires:       python-imaging
Requires:       python-reportlab


%description
UniConvertor is a universal vector graphics translator.
It uses sK1 engine to convert one format to another.


%prep
%setup -q -n UniConvertor-%{version}
%patch0 -p1 -b .simplify
%patch1 -p1 -b .rename-in-help
%patch2 -p1 -b .use-exec

# Prepare for inclusion into documentation part
install -p -m644 src/COPYRIGHTS COPYRIGHTS
install -p -m644 src/GNU_GPL_v2 GNU_GPL_v2
install -p -m644 src/GNU_LGPL_v2 GNU_LGPL_v2


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 

# Fix permissions
chmod a+x $RPM_BUILD_ROOT%{python_sitearch}/uniconvertor/__init__.py
chmod g-w $RPM_BUILD_ROOT%{python_sitearch}/uniconvertor/app/modules/*.so

# Don't duplicate documentation
rm -f $RPM_BUILD_ROOT%{python_sitearch}/uniconvertor/{COPYRIGHTS,GNU_GPL_v2,GNU_LGPL_v2}

# Satisfy rpmlint claim on debuginfo subpackage
chmod 644 src/modules/*/*.{c,h}

# Rename uniconv script due to conflicts with netatalk
# (https://bugzilla.redhat.com/show_bug.cgi?id=405011)
# Upstream notified via forum:
#   http://sk1project.org/forum/topic.php?forum=2&topic=11
#   http://sk1project.org/forum/topic.php?forum=2&topic=33
mv $RPM_BUILD_ROOT%{_bindir}/uniconv $RPM_BUILD_ROOT%{_bindir}/uniconvertor
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README
%doc COPYRIGHTS GNU_GPL_v2 GNU_LGPL_v2
%{_bindir}/uniconvertor
%{python_sitearch}/*


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.4-7
- 为 Magic 3.0 重建

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

