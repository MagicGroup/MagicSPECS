%global with_python3  1
%global oname   exif-py

Summary:        Python module to extract EXIF information
Summary(zh_CN.UTF-8): 提取 EXIF 信息的 Python 模块
Name:           python-exif
Version:	2.1.2
Release:	3%{?dist}
License:        BSD
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            https://github.com/ianare/exif-py
Source0:        https://github.com/ianare/%{oname}/archive/%{version}/%{oname}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%endif

%description
Python Library to extract EXIF information in digital camera image files.

%description -l zh_CN.UTF-8
提取 EXIF 信息的 Python 模块。

%if 0%{?with_python3}
%package -n    python3-exif
Summary:       Python 3 module to extract EXIF information
Summary(zh_CN.UTF-8): 提取 EXIF 信息的 Python3 模块
Group:         Development/Tools
Group(zh_CN.UTF-8): 开发/工具

%description -n python3-exif
Python Library to extract EXIF information in digital camera image files.

This is the Python 3 version of python-exif.
%description -n python3-exif -l zh_CN.UTF-8
提取 EXIF 信息的 Python3 模块。
%endif

%prep
%setup -q -n %{oname}-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/EXIF.py %{buildroot}%{_bindir}/python3-EXIF.py
ln -s python3-EXIF.py %{buildroot}%{_bindir}/python3-EXIF
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
ln -s EXIF.py %{buildroot}%{_bindir}/EXIF
magic_rpm_clean.sh

%files
%doc ChangeLog.rst LICENSE.txt README.rst
%{_bindir}/EXIF
%{_bindir}/EXIF.py
%{python_sitelib}/ExifRead-*-*.egg-info
%{python_sitelib}/exifread

%if 0%{?with_python3}
%files -n python3-exif
%doc ChangeLog.rst LICENSE.txt README.rst
%{_bindir}/python3-EXIF
%{_bindir}/python3-EXIF.py
%{python3_sitelib}/exifread
%{python3_sitelib}/ExifRead-*-py*.egg-info
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.1.2-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.1.2-2
- 更新到 2.1.2

* Wed Sep 02 2015 Liu Di <liudidi@gmail.com> - 2.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Terje Rosten <terje.rosten@ntnu.no> - 2.1.1-1
- 2.1.1

* Mon Apr 13 2015 Terje Rosten <terje.rosten@ntnu.no> - 2.0.2-1
- 2.0.2
- Add python3 sub package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Terje Rosten <terje.rosten@ntnu.no> - 1.4.2-1
- 1.4.2
- Fix github source url

* Tue Oct 22 2013 Terje Rosten <terje.rosten@ntnu.no> - 1.4.1-1
- 1.4.1

* Tue Aug 13 2013 Terje Rosten <terje.rosten@ntnu.no> - 1.3.3-1
- 1.3.3, (fixing bz #996583)
- Project has moved to github

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Terje Rosten <terjeros@phys.ntnu.no> - 1.1.0-1
- 1.1.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.8-2
- Rebuild for Python 2.6

* Fri Aug 15 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.8-1
- 1.0.8

* Mon Mar  3 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-4
- Fix script (bz #435758)

* Mon Feb 11 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-3
- Add script and changes.txt

* Sat Jan 19 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-2
- Improve setup.py

* Thu Jan  3 2008 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.7-1
- 1.0.7
- Include egg info

* Mon Nov 19 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.5-1
- 1.0.5

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-3
- Tagging...

* Mon Aug 06 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-2
- Fix typo in url
- Add python-devel to buildreq
- Add license to setup.py
- Strip code from %%doc file
- Fix typo in sitelib macro

* Sat Aug 04 2007 Terje Rosten <terjeros@phys.ntnu.no> - 1.0.2-1
- Initial build

