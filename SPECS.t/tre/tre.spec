%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name: tre
Version: 0.8.0
Release: 8%{?dist}
License: BSD
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Source0: http://laurikari.net/tre/%{name}-%{version}.tar.bz2
Patch0: %{name}-chicken.patch
# make internal tests of agrep work with just-built shared library
Patch1: %{name}-tests.patch
Summary: POSIX compatible regexp library with approximate matching
Summary(zh_CN.UTF-8): 带有近似匹配的 POSIX 兼容的正则表达式库
URL: http://laurikari.net/tre/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel

%description
TRE is a lightweight, robust, and efficient POSIX compatible regexp
matching library with some exciting features such as approximate
matching.
%description -l zh_CN.UTF-8
带有近似匹配的 POSIX 兼容的正则表达式库。

%package devel
Requires: tre = %{version}-%{release}
Summary: Development files for use with the tre package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description devel
This package contains header files and static libraries for use when
building applications which use the TRE library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n python-%{name}
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Summary: Python bindings for the tre library
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定

%description -n python-%{name}
This package contains the python bindings for the TRE library.

%description -n python-%{name} -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%package -n agrep
Summary: Approximate grep utility
Summary(zh_CN.UTF-8): 近似匹配 grep 工具
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本

%description -n agrep
The agrep tool is similar to the commonly used grep utility, but agrep
can be used to search for approximate matches.

The agrep tool searches text input for lines (or records separated by
strings matching arbitrary regexps) that contain an approximate, or
fuzzy, match to a specified regexp, and prints the matching lines.
Limits can be set on how many errors of each kind are allowed, or
only the best matching lines can be output.

Unlike other agrep implementations, TRE agrep allows full POSIX
regexps of any length, any number of errors, and non-uniform costs.

%description -n agrep -l zh_CN.UTF-8
近似匹配 grep 工具。

%prep
%setup -q
# hack to fix python bindings build
ln -s lib tre
%patch0 -p1 -b .chicken
%patch1 -p1 -b .tests

%build
%configure --disable-static --disable-rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}
pushd python
%{__python} setup.py build
popd

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
pushd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
rm $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang %{name} || :

%check
# revert rpath removal for building internal test programs
sed -i 's|^runpath_var=DIE_RPATH_DIE|runpath_var=LD_RUN_PATH|g' libtool
%{__make} check

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL LICENSE NEWS README THANKS TODO
%doc doc/*.html doc/*.css
%attr(755,root,root) %{_libdir}/libtre.so.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtre.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files -n python-%{name}
%defattr(644,root,root,755)
%{python_sitearch}/tre.so
%{python_sitearch}/*.egg-info

%files -n agrep
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/agrep
%{_mandir}/man1/agrep.1*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.8.0-8
- 为 Magic 3.0 重建

* Sun Oct 04 2015 Liu Di <liudidi@gmail.com> - 0.8.0-7
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.8.0-6
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for glibc bug#747377

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Sep 20 2009 Dominik Mierzejewski <rpm@greysector.net> 0.8.0-1
- updated to 0.8.0 (ABI change)

* Sat Aug 22 2009 Dominik Mierzejewski <rpm@greysector.net> 0.7.6-2
- added missing defattr for python subpackage
- dropped conditionals for Fedora <10
- used alternative method for rpath removal
- fixed internal testsuite to run with just-built shared library
- dropped unnecessary build dependencies

* Tue Jul 28 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.7.6-1
- new version 0.7.6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.7.5-6
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.5-5
- Autorebuild for GCC 4.3

* Tue Jan 01 2008 Dominik Mierzejewski <rpm@greysector.net> 0.7.5-4
- fix build in rawhide (include python egg-info file)

* Wed Oct 31 2007 Dominik Mierzejewski <rpm@greysector.net> 0.7.5-3
- include python bindings (bug #355241)
- fix chicken-and-egg problem when building python bindings

* Wed Aug 29 2007 Dominik Mierzejewski <rpm@greysector.net> 0.7.5-2
- rebuild for BuildID
- update license tag

* Mon Jan 29 2007 Dominik Mierzejewski <rpm@greysector.net> 0.7.5-1
- update to 0.7.5
- remove redundant BRs
- add %%check

* Thu Sep 14 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-6
- remove ExcludeArch, the bug is in crm114

* Tue Aug 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-5
- mass rebuild

* Fri Aug 04 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-4
- bump release to fix CVS tag

* Thu Aug 03 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-3
- per FE guidelines, ExcludeArch only those problematic arches

* Wed Aug 02 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-2
- fixed rpmlint warnings
- ExclusiveArch: %%{ix86} until amd64 crash is fixed and somebody
  tests ppc(32)

* Wed Jul 26 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.4-1
- 0.7.4
- disable evil rpath
- added necessary BRs
- license changed to LGPL

* Sun Feb 19 2006 Dominik Mierzejewski <rpm@greysector.net> 0.7.2-1
- \E bug patch
- FE compliance

* Sun Nov 21 2004 Ville Laurikari <vl@iki.fi>
- added agrep man page

* Sun Mar 21 2004 Ville Laurikari <vl@iki.fi>
- added %%doc doc

* Wed Feb 25 2004 Ville Laurikari <vl@iki.fi>
- removed the .la file from devel package

* Mon Dec 22 2003 Ville Laurikari <vl@iki.fi>
- added %%post/%%postun ldconfig scriplets.

* Fri Oct 03 2003 Ville Laurikari <vl@iki.fi>
- included in the TRE source tree as `tre.spec.in'.

* Tue Sep 30 2003 Matthew Berg <mberg@synacor.com>
- tagged release 1
- initial build
