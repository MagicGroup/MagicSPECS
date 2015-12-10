%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygame
Version:        1.9.1
Release:        14%{?dist}
Summary:        Python modules for writing games
Summary(zh_CN.UTF-8): 编写游戏的 Python 模块

Group:          Development/Languages
Group(zh_CN.UTF-8): 开发/语言
License:        LGPLv2+
URL:            http://www.pygame.org
#Patch0:         %{name}-1.8.1-config.patch
Patch0:         %{name}-1.9.1-config.patch
# porttime is part of libportmidi.so, there's no libporttime in Fedora
Patch1:         pygame-1.9.1-porttime.patch
Patch2:         pygame-1.9.1-no-test-install.patch
# patch backported from upstream repository, V4L has been remove in linux-2.6.38
# http://svn.seul.org/viewcvs/viewvc.cgi?view=rev&root=PyGame&revision=3077
Patch3:         pygame-remove-v4l.patch
Patch4:         pygame-png-leak.patch
Source0:        http://pygame.org/ftp/%{name}-%{version}release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel numpy
BuildRequires:  SDL_ttf-devel SDL_image-devel SDL_mixer-devel
BuildRequires:  SDL-devel
BuildRequires:  libpng-devel libjpeg-devel libX11-devel
BuildRequires:  portmidi-devel
Requires:       numpy gnu-free-sans-fonts

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
Pygame is highly portable and runs on nearly every platform and
operating system.

%description -l zh_CN.UTF-8
编写游戏的 Python 模块。

%package devel
Summary:        Files needed for developing programs which use pygame
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       SDL_ttf-devel SDL_mixer-devel
Requires:       python-devel

%description devel
This package contains headers required to build applications that use
pygame.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -qn %{name}-%{version}release

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# rpmlint fixes
find examples/ -type f -print0 | xargs -0 chmod -x 
find docs/ -type f -print0 | xargs -0 chmod -x
find src/ -type f -name '*.h' -print0 | xargs -0 chmod -x
chmod -x README.txt WHATSNEW

iconv -f iso8859-1 -t utf-8 WHATSNEW > WHATSNEW.conv && mv -f WHATSNEW.conv WHATSNEW
iconv -f iso8859-1 -t utf-8 README.txt > README.txt.conv && mv -f README.txt.conv README.txt


# These files must be provided by pygame-nonfree(-devel) packages on a
# repository that does not have restrictions on providing non-free software
rm -f src/ffmovie.[ch]


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#use system font.
rm -f $RPM_BUILD_ROOT%{python_sitearch}/%{name}/freesansbold.ttf
ln -s /usr/share/fonts/gnu-free/FreeSansBold.ttf $RPM_BUILD_ROOT%{python_sitearch}/%{name}/freesansbold.ttf

# Fix permissions
chmod 755 $RPM_BUILD_ROOT%{python_sitearch}/%{name}/*.so
magic_rpm_clean.sh

%check
# base_test fails in mock, unable to find soundcard
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/base_test.py || :
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/image_test.py
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/rect_test.py
 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/ README.txt WHATSNEW
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}*

%files devel
%defattr(-,root,root,-)
%doc examples/
%dir %{_includedir}/python*/%{name}
%{_includedir}/python*/%{name}/*.h


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.9.1-14
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.9.1-13
- 为 Magic 3.0 重建

* Wed Aug 12 2015 Liu Di <liudidi@gmail.com> - 1.9.1-12
- 为 Magic 3.0 重建

* Tue Dec 04 2012 Jan Kaluza <jkaluza@redhat.com> - 1.9.1-11
- fix #881545 - fix memory leak when saving png images

* Mon Jul 30 2012 Jon Ciesla <limburgher@gmail.com> - 1.9.1-10
- Use system font, BZ 477444.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.9.1-7
- Rebuild for new libpng

* Thu Jun 23 2011 Jan Kaluza <jkaluza@redhat.com> - 1.9.1-6
- Removed V4L support because V4L has been deprecated from the Linux
  kernel as of 2.6.38

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 16 2010 Jan Kaluza <jkaluza@redhat.com> - 1.9.1-4
- fix #607753 - Do not install tests

* Thu Aug 12 2010 Jan Kaluza <jkaluza@redhat.com> - 1.9.1-3
- fix #585526 - add MIDI support

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Oct 08 2009 Jon Ciesla <limb@jcomserv.net> - 1.9.1-1
- New upstream release, BZ 526365.
- Updated config_unix patch for 1.9.1.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> - 1.8.1-6
- Dropped f2py deps, unneeded now that numpy is fixed: BZ 496277.

* Fri Apr 17 2009 Jon Ciesla <limb@jcomserv.net> - 1.8.1-5
- Add dep for numpy-f2py to fix broken games, BZ 496218.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.8.1-3
- Rebuild for Python 2.6

* Wed Sep 17 2008 Robin Norwood <robin.norwood@gmail.com> 1.8.1-2
- Bump release to trump F9 version.

* Tue Aug 26 2008 Robin Norwood <robin.norwood@gmail.com> 1.8.1-1
- Update to new upstream version.
- rpmlint fixes

* Mon Aug 25 2008 Robin Norwood <robin.norwood@gmail.com> 1.8.0-3
- Rebase config patch for 1.8.0
- Need to specify BR: SDL-devel

* Mon Aug 25 2008 Robin Norwood <robin.norwood@gmail.com> 1.8.0-2
- Change from requiring python-numeric to numpy
- rhbz#457074

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 1.8.0-1
- Upstream sync
- Remove Obsolets/Provides (been around since FC-4)
- Remove no longer needed 64bit patch
- Remove %%{version} macro from Patch0 definition
- Add png, jpeg, and X11 libraries to BuildRequires
- Simplify %%files section
- Fix up some rpmlint warnings

* Thu Feb 21 2008 Christopher Stone <chris.stone@gmail.com> 1.7.1-16
- Add egginfo file to %%files
- Update %%license
- Fix permissions on .so files

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.7.1-15
- Autorebuild for GCC 4.3

* Tue May 15 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-14
- Add one more bit to 64-bit patch

* Sat May 12 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-13
- Apply 64-bit patch for python 2.5 (bz #239899)
- Some minor spec file cleanups

* Mon Apr 23 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-12
- Revert back to version 1.7.1-9

* Mon Dec 11 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-11
- Remove all Obsolete/Provides
- Remove Requires on all devel packages

* Sun Dec 10 2006 Christopher Stone <chris.stone@gmail.som> 1.7.1-10
- Remove macosx examples
- Move header files into main package
- Move examples into examples subpackage
- python(abi) = 0:2.5

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-9
- No longer %%ghost pyo files. Bug #205396

* Sat Sep 02 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-8
- FC6 Rebuild

* Wed Jun 28 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-7.fc6.1
- Rebuild bump

* Wed May 03 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-7
- Fix Obsolete/Provides of python-pygame-doc

* Wed Apr 26 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-6
- Bump release for new build on devel

* Wed Apr 26 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-5
- Add Obsolete/Provides tags for python-pygame-docs
- Add Obsolete/Provides tags for python-pygame-devel to devel package
- Hopefully this fixes Bugzilla bug #189991

* Fri Apr 21 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-4
- Add Requires to -devel package
- Remove ffmovie.h from -devel package since it requires smpeg-devel

* Fri Apr 21 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-3
- Obsolete linva python-pygame package
- Added Provides for python-pygame
- Fix equal sign in devel requires

* Thu Apr 20 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-2
- Added a patch to clean up some warnings on 64 bit compiles

* Tue Apr 18 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-1
- Initial RPM release
