%global major_ver 0.1

Name:           gnome-js-common
Version:        %{major_ver}.2
Release:        7%{?dist}
Summary:        Common modules for GNOME JavaScript interpreters

Group:          Development/Libraries
# LGPLv3 part still being clarified with upstream
License:        BSD and MIT and LGPLv3
URL:            http://ftp.gnome.org/pub/GNOME/sources/%{name}
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{major_ver}/%{name}-%{version}.tar.bz2
# http://git.gnome.org/browse/gnome-js-common/patch/?id=d6ba3133f44ec888af8d64c87822d1bff7c891fe
Patch0:		%{name}-0.1.2-license.patch

BuildArch:      noarch

BuildRequires:  intltool
#Requires:       

%description
This package contains some JavaScript modules for use by GNOME
JavaScript extensions, namely GJS and Seed.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .license


%build
# not using standard configure macro. Nothing is compiled,
# make libdir point to %%{_datadir}
./configure --prefix=%{_prefix} --libdir=%{_datadir}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%{_datadir}/gnome-js
%exclude %{_docdir}/gnome_js_common

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/gnome-js-common.pc



%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.1.2-7
- 为 Magic 3.0 重建

* Fri Nov 16 2012 Liu Di <liudidi@gmail.com> - 0.1.2-6
- 为 Magic 3.0 重建

* Tue Dec 06 2011 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 17 2010 Michel Salim <salimma@fedoraproject.org> - 0.1.2-3
- Drop buildroot
- Specify patch version manually; Emacs rpm-spec mode gets confused if this
  is done via macros

* Fri Jun 11 2010 Michel Alexandre Salim <michel@hypatia.localdomain> - 0.1.2-2
- Review feedback:
- Drop noarch patch; point libdir to %%{_datadir} instead
- Drop %%clean section; not needed on F-13+

* Mon Mar 29 2010 Michel Salim <salimma@fedoraproject.org> - 0.1.2-1
- Initial package

