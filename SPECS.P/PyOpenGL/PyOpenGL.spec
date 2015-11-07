Name:           PyOpenGL
Version: 3.1.0
Release: 2%{?dist}
Summary:        Python bindings for OpenGL
Summary(zh_CN.UTF-8): OpenGL 的 Python 绑定
License:        BSD
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://pyopengl.sourceforge.net/
# It was reported in https://bugzilla.redhat.com/show_bug.cgi?id=760366
# that there are some binary blobs in the upstream archive. 
# I'm removing them prior to upload, so the check sums of the uploaded
# and upstream packages will not match. However I'm not changig the 
# source URL since I hope it will be fixed in a next release.
# Upstream bug: https://sourceforge.net/tracker/?func=detail&aid=3451797&group_id=5988&atid=105988
Source0:        https://pypi.python.org/packages/source/P/PyOpenGL/PyOpenGL-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python2-devel 
BuildRequires:  python-setuptools-devel
BuildArch:      noarch
Requires:       numpy python-setuptools freeglut
# in some other repositories this is named python-opengl
Provides:       python-opengl = %{version}-%{release}
Obsoletes:      python-opengl < %{version}-%{release}

%description
PyOpenGL is the cross platform Python binding to OpenGL and related APIs. It
includes support for OpenGL v1.1, GLU, GLUT v3.7, GLE 3 and WGL 4. It also
includes support for dozens of extensions (where supported in the underlying
implementation).

PyOpenGL is interoperable with a large number of external GUI libraries
for Python including (Tkinter, wxPython, FxPy, PyGame, and Qt). 

%description -l zh_CN.UTF-8
OpenGL 的 Python 绑定。

%package Tk
Summary:        %{name} OpenGL Tk widget
Summary(zh_CN.UTF-8): %{name} 的 Tk 部件
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name} = %{version}-%{release}, tkinter

%description Tk
%{name} Togl (Tk OpenGL widget) 1.6 support.

%description Tk -l zh_CN.UTF-8
%{name} 的 Tk 部件。

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root="$RPM_BUILD_ROOT" \
  --prefix="%{_prefix}"
#chmod -x %{buildroot}%{python_sitelib}/%{name}-%{version}-py?.?.egg-info
magic_rpm_clean.sh

%files
%defattr(-,root,root,-)
%doc license.txt
%{python_sitelib}/*OpenGL*
%exclude %{python_sitelib}/OpenGL/Tk

%files Tk
%defattr(-,root,root,-)
%{python_sitelib}/OpenGL/Tk

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.1.0-2
- 为 Magic 3.0 重建

* Mon Apr 13 2015 Liu Di <liudidi@gmail.com> - 3.1.0-1
- 更新到 3.1.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Nikolay Vladimirov <nikolay@vladimiroff.com> - 3.0.1-3
- Upload new archive with removed binary blobs - RHB #760366

* Sat Apr 16 2011 Nikolay Vladimirov <nikolay@vladimiroff.com> - 3.0.1-2
- Fix date in previous changelog entry
- specfile fixes

* Fri Apr 15 2011 Nikolay Vladimirov <nikolay@vladimiroff.com> - 3.0.1-1
- New upstream release
- Fix BZ # 635496 - PyOpenGL crashes on every program
- Update the shebang patch to work on the latest version
- Upstream restored license.txt to their distribution

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 30 2009 Jesse Keating <jkeating@redhat.com> - 3.0.0-2
- Rebuild for Fedora 12 mass rebuild

* Tue Jun 9 2009 Nikolay Vladimirov <nikolay@vladimiroff.com> - 3.0.0-1
- Updated to 3.0 stable
- Changed requires from python-numeric to numpy for BZ #504681
- upstream removed full license text in license.txt
- other minor spec fixes

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.12.b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 2 2009 Nikolay Vladimirov <nikolay@vladimiroff.com> - 3.0.0-0.11.b8
- New upstream 3.0.0b8 (b7 was skipped by upstream)
- performance, bug-fix and packaging release. 
- Use macro for "python"
- remove "--single-version-externally-managed" option for setup.py
- *.egg-info is no longer a folder, it's a file now 
- Tests are no longer installed by setup.py
- Obsolete 'doc' subpackage (no longer distributed "documentation" folder)
- license.txt is also no longer provided by upstream. Using one from b6
- Removed Requires for libGL and libGLU ( should be pulled for freeglut)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.0-0.10.b6
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.0-0.9.b6
- Rebuild for Python 2.6

* Mon Sep 22 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> 3.0.0-0.8.b6
- New upstream release 3.0.0b6

* Mon Jul 28 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> 3.0.0-0.7.b5
- New upstream release 3.0.0b5

* Fri Jul 18 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> 3.0.0-0.6.b4
- New upstream release 3.0.0b4

* Mon Dec 31 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-0.5.b1
- New upstream release 3.0.0b1

* Thu Aug 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-0.4.a6
- Change BuildRequires python-setuptools to python-setuptools-devel for
  the python-setuptools package split

* Fri Apr 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-0.3.a6
- Add missing freeglut, libGL and libGLU requires (bz 236159)

* Thu Mar 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-0.2.a6
- Remove tests from the package (bz 234121)
- Add -Tk subpackage (bz 234121)
- Remove shebang from files with shebang instead of chmod +x (bz 234121)
- Better description

* Sat Mar 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-0.1.a6
- Initial Fedora Extras package
