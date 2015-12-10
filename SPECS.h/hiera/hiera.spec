%if 0%{?el5}%{?el6}%{?fc16}
%{!?ruby_vendorlibdir: %global ruby_vendorlibdir /usr/lib/ruby/site_ruby/1.8}
%endif

#rspec seems broken(?) in epel5 and6, todo.
%if 0%{?el5}%{?el6}
%global with_checks 0
%else
%global with_checks 1
%endif

Name:           hiera
Version:	3.0.1
Release:        3%{?dist}
Summary:        A simple hierarchical database supporting plugin data sources
Summary(zh_CN.UTF-8): 一个简单的分层数据库支持插件数据源

Group:          System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
License:        ASL 2.0
URL:            http://projects.puppetlabs.com/projects/%{name}/
Source0:        http://downloads.puppetlabs.com/hiera/%{name}-%{version}.tar.gz
# We use a copy of misreleased 'newer' version of 1.0.0
# http://projects.puppetlabs.com/issues/16621
Source1:        hiera.yaml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if 0%{?with_checks}
BuildRequires:  rubygem(mocha)
%endif
BuildRequires:  ruby-devel
%if 0%{?el5}%{?el6}%{?fc16}
Requires:       ruby(abi) = 1.8
%else
%if 0%{?fedora} >= 19
Requires:       ruby(release)
%else
Requires:       ruby(abi) = 1.9.1
%endif
%endif

%description
A simple hierarchical database supporting plugin data sources.

%description -l zh_CN.UTF-8
一个简单的分层数据库支持插件数据源。

%prep
%setup -q
cp -p %{SOURCE1} hiera.yaml

%build
# Nothing to build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{ruby_vendorlibdir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_bindir}
cp -pr lib/hiera %{buildroot}%{ruby_vendorlibdir} 
cp -pr lib/hiera.rb %{buildroot}%{ruby_vendorlibdir} 
install -p -m0755 bin/hiera %{buildroot}%{_bindir}
install -p -m0644 hiera.yaml %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_var}/lib/hiera

%check
%if 0%{?with_checks}
ruby spec/spec_helper.rb
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/hiera
%{ruby_vendorlibdir}/hiera.rb
%{ruby_vendorlibdir}/hiera
%dir %{_var}/lib/hiera
%config(noreplace) %{_sysconfdir}/hiera.yaml
%doc COPYING README.md LICENSE


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 3.0.1-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.0.1-2
- 更新到 3.0.1

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 1.3.2-1
- 更新到 1.3.2

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 1 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-3
- Correct ruby(abi) requirement.

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-2
- Remove _isa tag for f18 from ruby-devel?

* Thu Sep 27 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-1
- Update to 1.0.0
- Add LICENSE file
- Add /var/lib/hiera as default data path.

* Wed May 30 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2.rc3
- Update to 1.0.0rc3 and drop puppet functions.

* Wed May 16 2012 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-0.2rc2
- Adapt to fedora guidelines.

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc2
- 1.0.0rc2 release

* Mon May 14 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 1.0.0-0.1rc1
- 1.0.0rc1 release

* Thu May 03 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 0.3.0.28-1
- Initial Hiera Packaging. Upstream version 0.3.0.28

