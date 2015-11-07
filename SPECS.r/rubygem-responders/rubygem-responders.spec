%global gem_name responders

Name:           rubygem-%{gem_name}
Version:        2.1.0
Release:        5%{?dist}
Summary:        Set of Rails responders to dry up your application

Group:          Development/Languages
License:        MIT
URL:            http://github.com/plataformatec/responders
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone http://github.com/plataformatec/responders && cd responders
# git checkout v2.1.0
# tar -czf rubygem-responders-2.1.0-test.tgz test/
Source1:        %{name}-%{version}-test.tgz
# https://github.com/plataformatec/responders/commit/e4da9c86255e5e085b9ac683e1253c451a3163e2
Patch0:         %{gem_name}-tests.patch

BuildArch:      noarch
# to avoid jruby
BuildRequires:  ruby
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(activemodel) >= 4.2.1
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(mocha)
BuildRequires:  rubygem(rails)

%description
A set of Rails responders to dry up your application.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version} -a 1
%patch0 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
cp -pr test/ ./%{gem_instdir}
pushd .%{gem_instdir}
sed -i -e '\,bundler/setup,d' test/test_helper.rb
ruby -Ilib:test test/**/*_test.rb
rm -rf test/
popd


%files
%dir %{gem_instdir}/
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}/
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.0-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.0-3
- Patch to update tests with rails 4.2.1
- Workaround jruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.0-1
- Initial package
