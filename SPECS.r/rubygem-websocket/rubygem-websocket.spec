# Generated from websocket-1.1.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name websocket

Name: rubygem-%{gem_name}
Version: 1.2.2
Release: 5%{?dist}
Summary: Universal Ruby library to handle WebSocket protocol
Group: Development/Languages
License: MIT
URL: http://github.com/imanel/websocket-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: comment-broken-tests.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: rubygem(rspec)
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Universal Ruby library to handle WebSocket protocol.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

%patch0 -p0

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd ./%{gem_instdir}
find spec -name *.rb | xargs sed -i '/its/ s/^/#/'
rspec -Ilib spec
popd	

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%doc %{gem_instdir}/README.md

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%{gem_instdir}/websocket.gemspec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.2-5
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Mo Morsi <mmorsi@redhat.com> - 1.2.2-3
- Update to comply with guidelines

* Fri May 01 2015 Mo Morsi <mmorsi@redhat.com> - 1.2.2-2
- Incorporate Fedora feedback

* Fri Apr 24 2015 Mo Morsi <mmorsi@redhat.com> - 1.2.2-1
- Update to latest version

* Sat Jan 11 2014 Nitesh Narayan Lal<niteshnarayan@fedoraproject.org> - 1.1.2-1
- Initial package
