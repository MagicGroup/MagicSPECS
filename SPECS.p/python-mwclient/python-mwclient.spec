%{!?pyver:%global pyver %(%{__python} -c "import sys ; print sys.version[:3]")}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib:%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           python-mwclient
Version:        0.6.5
Release:        4%{?dist}
Summary:        Mwclient is a client to the MediaWiki API

Group:          System Environment/Libraries
License:        MIT
URL:            http://sourceforge.net/apps/mediawiki/mwclient/index.php?title=Main_Page
Source0:        http://downloads.sourceforge.net/mwclient/mwclient-%{version}.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires:  python-devel
Requires:  python-simplejson

%description
Mwclient is a client to the MediaWiki API <http://mediawiki.org/wiki/API>
and allows access to almost all implemented API functions

%prep
%setup -q -n mwclient


%build
# intentionally left blank


%install
rm -rf $RPM_BUILD_ROOT
install -d -m755 %{buildroot}%{python_sitelib}/mwclient/
install -pm 0644 *.py %{buildroot}%{python_sitelib}/mwclient/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.txt REFERENCE.txt RELEASE-NOTES.txt
%{python_sitelib}/mwclient/


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Robert Scheck <robert@fedoraproject.org> - 0.6.5-1
- Upgrade to 0.6.5 (#714302)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Sep 22 2009 Steven M. Parrish <smparrish@gmail.com> - 0.6.3-3
- Fix patch

* Sun Sep 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-2
- upstream wmf patch
- %%doc README.txt
- use %%global (instead of %%define)

* Tue Sep 15 2009  Steven M. Parrish <smparrish@gmail.com> - 0.6.3-1
- Initial build
