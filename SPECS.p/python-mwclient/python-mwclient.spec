%global github_owner    mwclient
%global github_name     mwclient

Name:           python-mwclient
Version:	0.7.2
Release:	1%{?dist}
Summary:        Mwclient is a client to the MediaWiki API
Summary(zh_CN.UTF-8): 这是 MediaWiki 的客户端 API

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://sourceforge.net/apps/mediawiki/mwclient/index.php?title=Main_Page
Source0:        https://pypi.python.org/packages/source/m/mwclient/mwclient-%{version}.zip 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires:  python-devel
Requires:  python-simplejson

%description
Mwclient is a client to the MediaWiki API <http://mediawiki.org/wiki/API>
and allows access to almost all implemented API functions

%description -l zh_CN.UTF-8
这是 MediaWiki 的客户端 API。

%prep
%setup -q -n %{github_name}-%{version}


%build
%{__python2} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT


# cannot be run yet, need python-responses packaged
#check
#%{__python2} setup.py test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.rst 
%{python2_sitelib}/%{github_name}*

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 0.7.2-1
- 更新到 0.7.2

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
