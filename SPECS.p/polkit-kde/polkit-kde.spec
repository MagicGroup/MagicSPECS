Name:           polkit-kde
Version:        0.99.0
Release:        5%{?dist}
Summary:        PolicyKit integration for KDE Desktop

Group:          Applications/System
License:        GPLv2+
URL:            http://www.kde.org/

Source0:        ftp://ftp.kde.org/pub/kde/stable/apps/KDE4.x/admin/polkit-kde-agent-1-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstream patches
Patch05: 0005-Bring-the-auth-dialog-to-the-front-when-it-is-shown..patch
Patch16: 0016-Autorestart-when-we-crash.-This-way-a-polkit-kde-1-c.patch
Patch17: 0017-Of-course-we-can-only-set-KCrash-flags-after-KCmdLin.patch
Patch19: 0019-Remove-unused-Remember-authorization-checkboxes.patch
Patch20: 0020-CCMAIL-echidnaman-kubuntu.org.patch

BuildRequires:  kdelibs4-devel
BuildRequires:  polkit-qt-devel >= 0.99.0
BuildRequires:  cmake
BuildRequires:  gettext

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

Provides: PolicyKit-authentication-agent
Provides: polkit-kde-1 = %{version}-%{release}

Obsoletes: PolicyKit-kde < 4.5

%description
Provides Policy Kit Authentication Agent that nicely fits to KDE.

%prep
%setup -q -n polkit-kde-agent-1-%{version}

%patch05 -p1 -b .0005
%patch16 -p1 -b .0016
%patch17 -p1 -b .0017
%patch19 -p1 -b .0019
%patch20 -p1 -b .0020


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang polkit-kde-authentication-agent-1


%clean
rm -rf %{buildroot}


%files -f polkit-kde-authentication-agent-1.lang
%defattr(-,root,root,-)
%doc COPYING
%{_kde4_libexecdir}/polkit-kde-authentication-agent-1
%{kde4_datadir}/autostart/polkit-kde-authentication-agent-1.desktop
%{_kde4_appsdir}/policykit1-kde/policykit1-kde.notifyrc


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.99.0-5
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-3
- patch to bring polkit auth dialog to front
- patch restart polkit-kde on crash 
- patch to remove unimplimented 'remember authorization' checkbox

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.99.0-1
- Update to 0.99.0

* Thu Nov 25 2010 Radek Novacek <rnovacek@redhat.com> 0.98.1-1
- Update to polkit-kde-0.98.1

* Thu Nov 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-7
- rebuild (polkit-qt) 

* Wed Aug 04 2010 Radek Novacek <rnovacek@redhat.com> - 0.95.1-6
- Fixed FTBFS with GCC-4.5

* Wed Aug 04 2010 Radek Novacek <rnovacek@redhat.com> - 0.95.1-5
- Add patch for showing "password for root" when root user is authenticating
- Related: #618543

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-4
- FTBFS polkit-kde-0.95.1-3.fc13: ImplicitDSOLinking (#564809)

* Wed Jan 06 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-3
- Again provides PolicyKit-authentication-agent

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-2
- Added Gettext BR

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-1
- Update to official release
- Provides polkit-kde-1

* Mon Nov 30 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.2.20091125svn
- Adds desktop file
- Adds obsoletes

* Wed Nov 25 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.1.20091125svn
- Initial package
