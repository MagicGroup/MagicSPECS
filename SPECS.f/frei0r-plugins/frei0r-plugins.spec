Name:           frei0r-plugins
Version:        1.3
Release:        6%{?dist}
Summary:        Frei0r - a minimalistic plugin API for video effects
Summary(zh_CN.UTF-8): Frei0r - 一个最简单的视频特效插件 API

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        GPLv2+
URL:            http://www.piksel.org/frei0r
Source0:        http://propirate.net/frei0r/frei0r-plugins-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gavl-devel >= 0.2.3
BuildRequires:  opencv-devel >= 1.0.0
     

%description
It is a minimalistic plugin API for video sources and filters. The behaviour of
the effects can be controlled from the host by simple parameters. The intent is
to solve the recurring reimplementation or adaptation issue of standard effect

%description -l zh_CN.UTF-8
一个最简单的视频特效插件 API。

%package -n     frei0r-devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description -n frei0r-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n frei0r-%{version}


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

#Remove installed doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_libdir}/frei0r-1/*.so

%files -n frei0r-devel
%defattr(-,root,root,-)
%{_includedir}/frei0r.h
%{_libdir}/pkgconfig/frei0r.pc

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 1.3-6
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.3-5
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.3-4
- 为 Magic 3.0 重建

* Sat Nov 24 2012 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建

* Fri Nov 25 2011 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Fri May 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3-1
- Update to 1.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-2
- Rebuild for OpenCV 2.2

* Fri Nov 26 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Sat Jun 26 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.22-5
- Rebuilt for opencv

* Sat Feb 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.22-4
- Rebuild for opencv SO version change

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 kwizart < kwizart at gmail.com > - 1.1.22-2
- Rebuild for opencv

* Tue Mar 24 2009 kwizart < kwizart at gmail.com > - 1.1.22-1
- Update to 1.1.22
- Prevent timestamp change when installing

* Tue Jul 22 2008 kwizart < kwizart at gmail.com > - 1.1.21-2
- Add gcc43 patches

* Sat Jun  7 2008 kwizart < kwizart at gmail.com > - 1.1.21-1
- Initial spec file for Fedora.

