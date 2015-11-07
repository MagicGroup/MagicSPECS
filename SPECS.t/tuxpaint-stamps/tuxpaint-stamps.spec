Name:           tuxpaint-stamps
Version:	2014.08.23
Release:	2%{?dist}
Summary:        Extra stamp files for tuxpaint
Summary(zh_CN.UTF-8): tuxpaint 的额外 stamp 文件
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License:        GPL+ and GFDL and CC-BY-SA and Public Domain
URL:            http://www.tuxpaint.org/
Source0:        http://download.sourceforge.net/tuxpaint/tuxpaint-stamps-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python gettext
Requires:       tuxpaint

%description
This package is a collection of 'rubber stamps' for Tux Paint's "Stamp" tool.

%description -l zh_CN.UTF-8
tuxpaint 的额外 stamp 文件。

%prep
%setup -q

%build
(cd po && chmod u+x createpo.sh && ./createpo.sh)
(cd po && ./createtxt.sh)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/tuxpaint/stamps
make install-all PREFIX=$RPM_BUILD_ROOT%{_prefix}

pushd po
for file in *.po ; do
    loc=`echo $file | sed -e 's/tuxpaint-stamps-\(.*\).po/\1/'`
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$loc/LC_MESSAGES
    msgfmt -o $RPM_BUILD_ROOT%{_datadir}/locale/$loc/LC_MESSAGES/tuxpaint-stamps.mo $file
done
popd

# License is bad on this file, Creative Commons Sampling Plus 1.0 is non-free.
rm -rf $RPM_BUILD_ROOT%{_datadir}/tuxpaint/stamps/vehicles/emergency/firetruck.ogg

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc docs/*.txt
%lang(el) %doc docs/el
%lang(es) %doc docs/es
%lang(fr) %doc docs/fr
%lang(hu) %doc docs/hu
%defattr(0644,root,root,0755)
%{_datadir}/tuxpaint/stamps/*

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2014.08.23-2
- 为 Magic 3.0 重建

* Mon Oct 05 2015 Liu Di <liudidi@gmail.com> - 2014.08.23-1
- 更新到 2014.08.23

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009.06.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Jon Ciesla <limb@jcomserv.net> - 2009.06.28-1
- New upstream, fix FTBFS BZ 631086.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008.06.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008.06.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2008.06.30-1
- fix license tag
- update to 2008.06.30.

* Sat Jul 07 2007 Steven Pritchard <steve@kspei.com> 2007.07.01-1
- Update to 2007.07.01.

* Tue Oct 24 2006 Steven Pritchard <steve@kspei.com> 2006.10.21-1
- Update to 2006.10.21.
- Remove a little extra whitespace in the spec.
- Just include docs/*.txt.
- Use version macro in Source0 URL.
- Use "install-all" target.

* Mon Aug 28 2006 Wart <wart at kobold dot org> 2005.11.25-1
- Initial Fedora Extras package
