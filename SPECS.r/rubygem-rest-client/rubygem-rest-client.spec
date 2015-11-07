# Generated from rest-client-1.3.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rest-client

Name: rubygem-%{gem_name}
Version: 1.8.0
Release: 3%{?dist}
Summary: Simple HTTP and REST client for Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/rest-client/rest-client
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(http-cookie)
BuildRequires: rubygem(mime-types)
BuildRequires: rubygem(netrc)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(webmock)
BuildArch: noarch

%description
A simple HTTP and REST client for Ruby, inspired by the Sinatra microframework
style of specifying actions: get, put, post, delete.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
pushd .%{gem_instdir}
# Fix RSpec 3.x compatibility.
# https://github.com/rest-client/rest-client/pull/415
sed -i -r 's/^(\s*)(.*)(\.should) be_false/\1expect(\2).to be_falsey/' spec/unit/request_spec.rb
sed -i -r 's/^(\s*)(.*)(\.should) be_true/\1expect(\2).to be_truthy/' spec/unit/request{,2}_spec.rb

# Some tests fail without network connection."
rspec spec | grep "225 examples, 8 failures"
popd

%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{_bindir}/restclient
%exclude %{gem_instdir}/.*
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/AUTHORS
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/history.md
%{gem_instdir}/rest-client.gemspec
%{gem_instdir}/rest-client.windows.gemspec
%{gem_instdir}/spec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.8.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.8.0-2
- 为 Magic 3.0 重建

* Wed Aug 19 2015 Vít Ondruch <vondruch@redhat.com> - 1.8.0-1
- Update to rest-client 1.8.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.7-2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Sat Sep 22 2012 Tim Bielawa <tim@redhat.com> - 1.6.7-1
- Update to 1.6.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.1-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Michal Fojtik <mfojtik@redhat.com> - 1.6.1-1
- New version release

* Wed Mar 03 2010 Michal Fojtik <mfojtik@redhat.com> - 1.4.0-6
- New version release

* Wed Feb 17 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-5
- Added %%dir %%{geminstdir} into spec file

* Wed Feb 17 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-4
- Marked README.rdoc, history.md and spec/ as %%doc

* Tue Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-3
- Fixed licence (MIT)
- Fixed duplicated files in spec
- Replaced %%define with %%global

* Tue Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-2
- Fixed spec filename
- Added Ruby dependency

* Tue Feb 16 2010 Michal Fojtik <mfojtik@redhat.com> - 1.3.1-1
- Initial package
