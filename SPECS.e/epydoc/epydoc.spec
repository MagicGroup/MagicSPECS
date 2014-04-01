%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

Summary: Automatic API documentation generation tool for Python
Summary(zh_CN.UTF-8): Python 下的自动 API 文档生成工具
Name: epydoc
Version: 3.0.1
Release: 13%{?dist}
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License: MIT
URL: http://epydoc.sourceforge.net/
Source0: http://dl.sf.net/epydoc/epydoc-%{version}.tar.gz
Source1: epydocgui.desktop
Patch0: epydoc-3.0.1-nohashbang.patch
Patch1: epydoc-3.0.1-giftopng.patch
Patch2: epydoc-3.0.1-new-docutils.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: tkinter
# Needed for some outputs, like --pdf (#522249)
Requires: tex(dvips)
Requires: tex(latex)
BuildRequires: python-devel
BuildRequires: desktop-file-utils
BuildArch: noarch

%description
Epydoc  is a tool for generating API documentation for Python modules,
based  on their docstrings. For an example of epydoc's output, see the
API  documentation for epydoc itself (html, pdf). A lightweight markup
language  called  epytext can be used to format docstrings, and to add
information  about  specific  fields,  such as parameters and instance
variables.    Epydoc    also   understands   docstrings   written   in
ReStructuredText, Javadoc, and plaintext.

%description -l zh_CN.UTF-8
Python 下的自动 API 文档生成工具。

%prep
%setup -q
%patch0 -p1 -b .nohashbang
%patch1 -p1 -b .giftopng
%patch2 -p1 -b .new-docutils


%build
%{__python} setup.py build


%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

desktop-file-install \
    --vendor="" \
    --dir=%{buildroot}%{_datadir}/applications \
    --mode=0644 \
    %{SOURCE1}

# Also install the man pages
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1/

# Prevent having *.pyc and *.pyo in _bindir
%{__mv} %{buildroot}%{_bindir}/apirst2html.py %{buildroot}%{_bindir}/apirst2html
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt doc/
%{_bindir}/apirst2html
%{_bindir}/epydoc
%{_bindir}/epydocgui
%{python_sitelib}/epydoc/
%{python_sitelib}/epydoc-*.egg-info
%{_datadir}/applications/epydocgui.desktop
%{_mandir}/man1/*.1*


%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.0.1-13
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0.1-12
- Requires: tex(dvips) tex(latex)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 13 2010 Lubomir Rintel <lkundrak@v3.sk> 3.0.1-7
- Fix crash with newer docutils (#578920)

* Tue Dec  8 2009 Matthias Saou <http://freshrpms.net/> 3.0.1-6
- Add texlive-dvips and texlive-latex requirements (#522249).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 3.0.1-3
- Include patch to use png instead of gif for generated images (#459857).

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.1-2
- Rebuild for Python 2.6

* Sat Mar 22 2008 Matthias Saou <http://freshrpms.net/> 3.0.1-1
- Update to 3.0.1.
- Update nohashbang patch.
- Include new apirst2html script, but remove .py extension to avoid .pyc/pyo.
- Include egg-info file.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 2.1-8
- Remove desktop file prefix and X-Fedora category.
- Include patch to remove #! python from files only meant to be included.

* Mon Dec 11 2006 Matthias Saou <http://freshrpms.net/> 2.1-7
- Rebuild against python 2.5.
- Remove no longer needed explicit python-abi requirement.
- Change python build requirement to python-devel, as it's needed now.

* Wed Sep  6 2006 Matthias Saou <http://freshrpms.net/> 2.1-6
- No longer ghost the .pyo files, as per new python guidelines (#205374).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 2.1-5
- FC6 rebuild.
- Add %%{?dist} tag.
- Update summary line.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Dec 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 2.1-3
- Change to noarch.
- Get Python site-packages dir from distutils, should fix x86_64 build.
- Require python-abi and tkinter.
- %%ghost'ify *.pyo.
- Fix man page permissions.
- Add menu entry for epydocgui.

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 2.1-2
- Bump release to provide Extras upgrade path.

* Thu Oct 21 2004 Matthias Saou <http://freshrpms.net/> 2.1-1
- Picked up and rebuilt.
- Added doc and man pages.

* Fri May 07 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 2.1-0.fdr.1: Initial package

