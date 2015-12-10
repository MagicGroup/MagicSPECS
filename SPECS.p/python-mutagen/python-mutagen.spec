%global realname mutagen

%bcond_without python3

Name:           python-%{realname}
Version:	1.31
Release:	3%{?dist}
Summary:        Mutagen is a Python module to handle audio meta-data
Summary(zh_CN.UTF-8): 处理音频元数据的 Python 模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        GPLv2
URL:            https://bitbucket.org/lazka/mutagen/overview
Source0:        https://bitbucket.org/lazka/mutagen/downloads/mutagen-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif

%description
Mutagen is a Python module to handle audio meta-data. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bit-streams.

%description -l zh_CN.UTF-8
处理音频元数据的 Python 模块。

%if %{with python3}
%package -n python3-%{realname}
Summary:        Mutagen is a Python module to handle audio meta-data
Summary(zh_CN.UTF-8): 处理音频元数据的 Python3 模块

%description -n python3-%{realname}
Mutagen is a Python module to handle audio meta-data. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bit-streams.
%description -n python3-%{realname} -l zh_CN.UTF-8
处理音频元数据的 Python3 模块。
%endif

%prep
%setup -q -n %{realname}-%{version}

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif
magic_rpm_clean.sh

%check
# Without this the testsuite fails with
# RuntimeError: This test suite needs a unicode locale encoding. Try setting LANG=C.UTF-8
# Hopefully all builders have this locale installed/configured
export LANG=en_US.UTF-8
%{__python} setup.py test

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py test
%endif

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%{_bindir}/m*
%{_mandir}/*/*
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*.egg-info

%if %{with python3}
%files -n python3-%{realname}
%doc COPYING NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%{python3_sitelib}/%{realname}
%{python3_sitelib}/%{realname}*.egg-info
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.31-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.31-2
- 更新到 1.31

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 1.30-2
- 为 Magic 3.0 重建

* Mon Aug 24 2015 Michele Baldessari <michele@acksyn.org> - 1.30-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Michele Baldessari <michele@acksyn.org> - 1.29-1
- New upstream release

* Sat Mar 07 2015 Michele Baldessari <michele@acksyn.org> - 1.28-1
- New upstream release (BZ#1199683)

* Sun Mar 01 2015 Michele Baldessari <michele@acksyn.org> - 1.27-2
- Add initial Python 3 support on Fedora

* Mon Dec 15 2014 Michele Baldessari <michele@acksyn.org> - 1.27-1
- New upstream release
- Only use macro style for buildroot

* Sun Nov 23 2014 Michele Baldessari <michele@acksyn.org> - 1.26-1
- Fixed homepage and source URL
- Set python2-devel as BR
- Fix documentation building and shipping
- Fix spelling errors in description

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Silas Sewell <silas@sewell.ch> - 1.20-1
- Update to 1.20

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.19-1
- Update to 1.19
- Add tests

* Thu Feb 18 2010 Silas Sewell <silas@sewell.ch> - 1.18-1
- Update to 1.18

* Thu Oct 22 2009 Silas Sewell <silas@sewell.ch> - 1.17-1
- Update to 1.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Silas Sewell <silas@sewell.ch> - 1.16-1
- Update to 1.16
- New project URLs

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.15-3
- Normalize spec

* Fri Apr 10 2009 Silas Sewell <silas@sewell.ch> - 1.15-2
- Make sed safer
- Add back in removed changelogs

* Sun Mar 29 2009 Silas Sewell <silas@sewell.ch> - 1.15-1
- Update to 1.15

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.13-3
- Rebuild for Python 2.6

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-2
- Add egg-info to package

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-1
- 1.13

* Sat Aug 25 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.12-1
- Update to 1.12
- License tag fix

* Sat Apr 28 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.11-1
- Update to 1.11

* Wed Jan 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.10.1-1
- Update to 1.10.1

* Wed Dec 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.9-1
- Bump to 1.9

* Tue Dec 12 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-2
- Python 2.5 rebuild

* Sun Oct 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-1
- Bump to 1.8

* Fri Sep 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-2
- .pyo files no longer ghosted

* Fri Aug 11 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-1
- Update upstream to 1.6

* Fri Jul 21 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-5
- Some fixes in preamble.
- Change name from mutagen to python-mutagen.
- Delete CFLAGS declaration.

* Thu Jul 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-4
- Add BuildArch: noarch to preamble.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-3
- Remove python-abi dependency.
- Prep section deletes first two lines in __init__.py file due to rpmlint error.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-2
- Clean at files section.
- Fix charset in TUTORIAL file.

* Fri Jul 14 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-1
- First build.
